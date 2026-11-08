-- Run once as the database administrator, via setup.py. No ERP tables are altered.
-- The API login may execute only this schema's fixed-scope functions.
CREATE SCHEMA poc_registration AUTHORIZATION poc_registration_owner;
REVOKE ALL ON SCHEMA poc_registration FROM PUBLIC;
GRANT USAGE ON SCHEMA adempiere TO poc_registration_owner;
GRANT SELECT ON adempiere.ad_client, adempiere.ad_org, adempiere.ad_user,
  adempiere.m_product, adempiere.m_product_category, adempiere.c_uom,
  adempiere.c_taxcategory, adempiere.ad_sequence TO poc_registration_owner;
GRANT REFERENCES ON adempiere.m_product TO poc_registration_owner;
-- Row locks require UPDATE privilege, which is held only by the NOLOGIN function owner.
GRANT UPDATE ON adempiere.ad_client, adempiere.ad_org, adempiere.ad_user,
  adempiere.m_product_category, adempiere.c_uom, adempiere.c_taxcategory TO poc_registration_owner;
GRANT UPDATE(currentnext) ON adempiere.ad_sequence TO poc_registration_owner;
GRANT INSERT(m_product_id,ad_client_id,ad_org_id,createdby,updatedby,value,name,
  description,c_uom_id,m_product_category_id,c_taxcategory_id,producttype,
  group2,weight,unitsperpack,m_product_uu) ON adempiere.m_product TO poc_registration_owner;
GRANT INSERT(m_product_category_id,ad_client_id,ad_org_id,createdby,updatedby,
  value,name,plannedmargin,m_product_category_uu) ON adempiere.m_product_category TO poc_registration_owner;
GRANT INSERT(c_uom_id,ad_client_id,ad_org_id,createdby,updatedby,x12de355,
  name,uomsymbol,stdprecision,costingprecision,c_uom_uu) ON adempiere.c_uom TO poc_registration_owner;
GRANT INSERT(c_taxcategory_id,ad_client_id,ad_org_id,createdby,updatedby,
  name,c_taxcategory_uu) ON adempiere.c_taxcategory TO poc_registration_owner;

SET ROLE poc_registration_owner;
CREATE TABLE poc_registration.registration_request (
  request_id uuid PRIMARY KEY,
  payload_sha256 text NOT NULL CHECK (payload_sha256 ~ '^[a-f0-9]{64}$'),
  rule_version text NOT NULL CHECK (length(rule_version) BETWEEN 1 AND 1024),
  product_id numeric(10,0) NOT NULL UNIQUE REFERENCES adempiere.m_product(m_product_id),
  draft jsonb NOT NULL CHECK (jsonb_typeof(draft)='object'),
  created_masters jsonb NOT NULL DEFAULT '{}',
  actor_id numeric(10,0) NOT NULL DEFAULT 101 CHECK (actor_id=101),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE poc_registration.registration_audit (
  audit_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  request_id uuid NOT NULL UNIQUE REFERENCES poc_registration.registration_request(request_id),
  product_id numeric(10,0) NOT NULL REFERENCES adempiere.m_product(m_product_id),
  rule_version text NOT NULL,
  payload_sha256 text NOT NULL,
  event text NOT NULL DEFAULT 'product_registered' CHECK (event='product_registered'),
  actor_id numeric(10,0) NOT NULL DEFAULT 101 CHECK (actor_id=101),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE poc_registration.indexing_job (
  product_id numeric(10,0) PRIMARY KEY REFERENCES adempiere.m_product(m_product_id),
  request_id uuid NOT NULL UNIQUE REFERENCES poc_registration.registration_request(request_id),
  status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','indexed')),
  attempts integer NOT NULL DEFAULT 0 CHECK (attempts>=0),
  last_error text CHECK (last_error ~ '^[A-Z][A-Z0-9_]{0,63}$'),
  lease_token uuid,
  lease_until timestamptz,
  indexed_at timestamptz,
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- A reader can verify new-row provenance without reading drafts or acquiring write rights.
CREATE VIEW poc_registration.registered_product_provenance WITH (security_barrier=true) AS
  SELECT q.product_id,p.m_product_uu AS product_uuid,q.created_at
  FROM poc_registration.registration_request q
  JOIN poc_registration.registration_audit a ON a.request_id=q.request_id AND a.product_id=q.product_id
    AND a.payload_sha256=q.payload_sha256 AND a.rule_version=q.rule_version
  JOIN poc_registration.indexing_job j ON j.product_id=q.product_id AND j.request_id=q.request_id
  JOIN adempiere.m_product p ON p.m_product_id=q.product_id
  WHERE p.ad_client_id=11 AND p.ad_org_id=11 AND p.createdby=101 AND p.m_product_uu IS NOT NULL
    AND p.value=q.draft->>'code' AND q.actor_id=101 AND a.actor_id=101;

CREATE FUNCTION poc_registration.guard() RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
BEGIN
  PERFORM 1 FROM adempiere.ad_client WHERE ad_client_id=11 AND name='GardenWorld' AND isactive='Y' FOR SHARE;
  IF NOT FOUND THEN RAISE EXCEPTION 'REGISTRATION_POLICY_INVALID'; END IF;
  PERFORM 1 FROM adempiere.ad_org WHERE ad_org_id=11 AND ad_client_id=11 AND isactive='Y' FOR SHARE;
  IF NOT FOUND THEN RAISE EXCEPTION 'REGISTRATION_POLICY_INVALID'; END IF;
  PERFORM 1 FROM adempiere.ad_user WHERE ad_user_id=101 AND ad_client_id=11 AND ad_org_id IN (0,11) AND isactive='Y' FOR SHARE;
  IF NOT FOUND THEN RAISE EXCEPTION 'REGISTRATION_POLICY_INVALID'; END IF;
END $$;

CREATE FUNCTION poc_registration.masters() RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
  SELECT jsonb_build_object(
    'category',coalesce((SELECT jsonb_agg(jsonb_build_object('id',m_product_category_id,'name',name) ORDER BY name,m_product_category_id)
      FROM adempiere.m_product_category WHERE isactive='Y' AND ((ad_client_id=0 AND ad_org_id=0) OR (ad_client_id=11 AND ad_org_id IN(0,11)))),'[]'::jsonb),
    'uom',coalesce((SELECT jsonb_agg(jsonb_build_object('id',c_uom_id,'name',name) ORDER BY name,c_uom_id)
      FROM adempiere.c_uom WHERE isactive='Y' AND ((ad_client_id=0 AND ad_org_id=0) OR (ad_client_id=11 AND ad_org_id IN(0,11)))),'[]'::jsonb),
    'tax',coalesce((SELECT jsonb_agg(jsonb_build_object('id',c_taxcategory_id,'name',name) ORDER BY name,c_taxcategory_id)
      FROM adempiere.c_taxcategory WHERE isactive='Y' AND ((ad_client_id=0 AND ad_org_id=0) OR (ad_client_id=11 AND ad_org_id IN(0,11)))),'[]'::jsonb))
$$;

CREATE FUNCTION poc_registration.check_draft(d jsonb) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
DECLARE issues jsonb := '[]'; f text; v jsonb; t text; idcol text; n integer;
BEGIN
  PERFORM poc_registration.guard();
  IF jsonb_typeof(d) IS DISTINCT FROM 'object' THEN
    RETURN jsonb_build_array(jsonb_build_object('field','draft','rule_id','INPUT-01','message','商品入力は JSON オブジェクトにしてください。'));
  END IF;
  IF (d->>'code') IS NULL OR (d->>'code') !~ '^GW-[A-Z0-9]{4,12}$' THEN
    issues := issues || jsonb_build_array(jsonb_build_object('field','code','rule_id','CODE-01','message','GW- に続く英大文字・数字4〜12桁を入力してください。'));
  ELSIF EXISTS(SELECT 1 FROM adempiere.m_product WHERE ad_client_id=11 AND value=d->>'code') THEN
    issues := issues || jsonb_build_array(jsonb_build_object('field','code','rule_id','CODE-01','message','この商品コードは既に使用されています。'));
  END IF;
  IF jsonb_typeof(d->'name') IS DISTINCT FROM 'string' OR length(btrim(d->>'name')) NOT BETWEEN 1 AND 255 THEN
    issues := issues || jsonb_build_array(jsonb_build_object('field','name','rule_id','INPUT-01','message','商品名は1〜255文字で入力してください。'));
  END IF;
  FOREACH f IN ARRAY ARRAY['description','usage'] LOOP
    IF d ? f AND d->f <> 'null'::jsonb AND (jsonb_typeof(d->f)<>'string' OR length(d->>f)>255) THEN
      issues := issues || jsonb_build_array(jsonb_build_object('field',f,'rule_id','INPUT-01','message','255文字以内で入力してください。'));
    END IF;
  END LOOP;
  IF d ? 'weight' AND d->'weight'<>'null'::jsonb THEN
    IF jsonb_typeof(d->'weight') NOT IN ('number','string') OR (d->>'weight') !~ '^[0-9]+([.][0-9]+)?$' THEN
      issues := issues || jsonb_build_array(jsonb_build_object('field','weight','rule_id','WGT-01','message','重量は正の数を入力し、不明な場合は空欄にしてください。'));
    ELSIF (d->>'weight')::numeric<=0 OR (d->>'weight')::numeric>1000000000 THEN
      issues := issues || jsonb_build_array(jsonb_build_object('field','weight','rule_id','WGT-01','message','重量の範囲を確認してください。'));
    END IF;
  END IF;
  IF d ? 'pack' AND ((d->>'pack') IS NULL OR jsonb_typeof(d->'pack')<>'number' OR (d->>'pack') !~ '^[0-9]{1,10}$') THEN
    issues := issues || jsonb_build_array(jsonb_build_object('field','pack','rule_id','PKG-01','message','梱包数量は正の整数にしてください。'));
  ELSIF d ? 'pack' AND (d->>'pack')::numeric<1 THEN
    issues := issues || jsonb_build_array(jsonb_build_object('field','pack','rule_id','PKG-01','message','梱包数量は1以上にしてください。'));
  END IF;
  FOREACH f IN ARRAY ARRAY['category','uom','tax'] LOOP
    t := CASE f WHEN 'category' THEN 'm_product_category' WHEN 'uom' THEN 'c_uom' ELSE 'c_taxcategory' END;
    idcol := t || '_id'; v := d->f;
    IF jsonb_typeof(v)='number' AND v::text ~ '^[0-9]{1,10}$' THEN
      EXECUTE format('SELECT count(*) FROM (SELECT 1 FROM adempiere.%I WHERE %I=$1 AND isactive=''Y'' AND ((ad_client_id=0 AND ad_org_id=0) OR (ad_client_id=11 AND ad_org_id IN(0,11))) FOR SHARE) s',t,idcol) INTO n USING v::text::numeric;
      IF n<>1 THEN
        issues := issues || jsonb_build_array(jsonb_build_object('field',f,'rule_id','REF-01','message','このテナントで使用できる有効なマスタを選択してください。'));
      END IF;
    ELSIF jsonb_typeof(v)='object' AND jsonb_typeof(v->'new')='object' THEN
      v := v->'new';
      IF jsonb_typeof(v->'name') IS DISTINCT FROM 'string' OR length(btrim(v->>'name')) NOT BETWEEN 1 AND 60 THEN
        issues := issues || jsonb_build_array(jsonb_build_object('field',f||'.new.name','rule_id','REF-01','message','新規マスタ名は1〜60文字で入力してください。'));
      ELSE
        EXECUTE format('SELECT count(*) FROM adempiere.%I WHERE ad_client_id=11 AND name=$1',t) INTO n USING v->>'name';
        IF n>0 THEN issues := issues || jsonb_build_array(jsonb_build_object('field',f||'.new.name','rule_id','REF-01','message','同名のマスタがあります。既存の項目を選択してください。')); END IF;
      END IF;
      IF f IN('category','uom') THEN
        IF jsonb_typeof(v->'code') IS DISTINCT FROM 'string' OR length(btrim(v->>'code')) NOT BETWEEN 1 AND (CASE f WHEN 'uom' THEN 4 ELSE 40 END) THEN
          issues := issues || jsonb_build_array(jsonb_build_object('field',f||'.new.code','rule_id','REF-01','message','新規マスタのコードを確認してください。'));
        ELSE
          EXECUTE format('SELECT count(*) FROM adempiere.%I WHERE ad_client_id=11 AND %I=$1',t,CASE f WHEN 'uom' THEN 'x12de355' ELSE 'value' END) INTO n USING v->>'code';
          IF n>0 THEN issues := issues || jsonb_build_array(jsonb_build_object('field',f||'.new.code','rule_id','REF-01','message','同じコードのマスタがあります。既存の項目を選択してください。')); END IF;
        END IF;
      END IF;
      IF f='uom' AND v ? 'symbol' AND (jsonb_typeof(v->'symbol')<>'string' OR length(v->>'symbol')>10) THEN
        issues := issues || jsonb_build_array(jsonb_build_object('field','uom.new.symbol','rule_id','REF-01','message','単位記号は10文字以内で入力してください。'));
      END IF;
    ELSE
      issues := issues || jsonb_build_array(jsonb_build_object('field',f,'rule_id','REF-01','message','既存のマスタ ID または新規マスタを選択してください。'));
    END IF;
  END LOOP;
  RETURN issues;
END $$;

CREATE FUNCTION poc_registration.allocate_id(t text) RETURNS numeric
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
DECLARE s record; top numeric; first_id numeric;
BEGIN
  IF t NOT IN('m_product','m_product_category','c_uom','c_taxcategory') THEN RAISE EXCEPTION 'REGISTRATION_SEQUENCE_INVALID'; END IF;
  SELECT ad_sequence_id,currentnext,incrementno INTO STRICT s FROM adempiere.ad_sequence WHERE lower(name)=t AND istableid='Y' FOR UPDATE;
  IF s.incrementno<>1 OR s.currentnext IS NULL THEN RAISE EXCEPTION 'REGISTRATION_SEQUENCE_INVALID'; END IF;
  EXECUTE format('SELECT coalesce(max(%I),0) FROM adempiere.%I',t||'_id',t) INTO top;
  first_id := greatest(s.currentnext,top+1);
  IF first_id<1 OR first_id>=9999999999 THEN RAISE EXCEPTION 'REGISTRATION_SEQUENCE_INVALID'; END IF;
  UPDATE adempiere.ad_sequence SET currentnext=first_id+1 WHERE ad_sequence_id=s.ad_sequence_id;
  RETURN first_id;
EXCEPTION WHEN no_data_found OR too_many_rows THEN RAISE EXCEPTION 'REGISTRATION_SEQUENCE_INVALID';
END $$;

CREATE FUNCTION poc_registration.registration_status(r uuid) RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
  SELECT jsonb_build_object('product_id',q.product_id,'code',q.draft->>'code','index_status',j.status)
    FROM poc_registration.registration_request q JOIN poc_registration.indexing_job j USING(product_id) WHERE q.request_id=r
$$;

CREATE FUNCTION poc_registration.begin_registration(r uuid,h text,ver text) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
DECLARE old poc_registration.registration_request;
BEGIN
  -- Serialize registrations in this tiny local app; also interlock the legacy fixed seed batch.
  PERFORM pg_advisory_xact_lock(720031109);
  SELECT * INTO old FROM poc_registration.registration_request WHERE request_id=r;
  IF FOUND THEN
    IF old.payload_sha256<>h OR old.rule_version<>ver THEN RAISE EXCEPTION 'IDEMPOTENCY_CONFLICT'; END IF;
    RETURN poc_registration.registration_status(r);
  END IF;
  PERFORM poc_registration.guard();
  RETURN NULL;
END $$;

CREATE FUNCTION poc_registration.finish_registration(r uuid,h text,ver text,d jsonb) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
DECLARE replay jsonb; issues jsonb; created jsonb:='{}'; category_id numeric; uom_id numeric; tax_id numeric; product_id numeric; v jsonb;
BEGIN
  replay := poc_registration.begin_registration(r,h,ver);
  IF replay IS NOT NULL THEN RETURN replay; END IF;
  issues := poc_registration.check_draft(d);
  IF jsonb_array_length(issues)>0 THEN RAISE EXCEPTION 'REGISTRATION_INVALID'; END IF;
  IF jsonb_typeof(d->'category')='number' THEN category_id:=(d->>'category')::numeric;
  ELSE
    v:=d->'category'->'new'; category_id:=poc_registration.allocate_id('m_product_category');
    INSERT INTO adempiere.m_product_category(m_product_category_id,ad_client_id,ad_org_id,createdby,updatedby,value,name,plannedmargin,m_product_category_uu)
      VALUES(category_id,11,11,101,101,v->>'code',v->>'name',0,gen_random_uuid());
    created:=created||jsonb_build_object('category',category_id);
  END IF;
  IF jsonb_typeof(d->'uom')='number' THEN uom_id:=(d->>'uom')::numeric;
  ELSE
    v:=d->'uom'->'new'; uom_id:=poc_registration.allocate_id('c_uom');
    INSERT INTO adempiere.c_uom(c_uom_id,ad_client_id,ad_org_id,createdby,updatedby,x12de355,name,uomsymbol,stdprecision,costingprecision,c_uom_uu)
      VALUES(uom_id,11,11,101,101,v->>'code',v->>'name',v->>'symbol',0,4,gen_random_uuid());
    created:=created||jsonb_build_object('uom',uom_id);
  END IF;
  IF jsonb_typeof(d->'tax')='number' THEN tax_id:=(d->>'tax')::numeric;
  ELSE
    v:=d->'tax'->'new'; tax_id:=poc_registration.allocate_id('c_taxcategory');
    INSERT INTO adempiere.c_taxcategory(c_taxcategory_id,ad_client_id,ad_org_id,createdby,updatedby,name,c_taxcategory_uu)
      VALUES(tax_id,11,11,101,101,v->>'name',gen_random_uuid());
    created:=created||jsonb_build_object('tax',tax_id);
  END IF;
  product_id:=poc_registration.allocate_id('m_product');
  INSERT INTO adempiere.m_product(m_product_id,ad_client_id,ad_org_id,createdby,updatedby,value,name,description,
    c_uom_id,m_product_category_id,c_taxcategory_id,producttype,group2,weight,unitsperpack,m_product_uu)
    VALUES(product_id,11,11,101,101,d->>'code',d->>'name',d->>'description',uom_id,category_id,tax_id,'I',d->>'usage',
      (d->>'weight')::numeric,coalesce((d->>'pack')::numeric,1),gen_random_uuid());
  INSERT INTO poc_registration.registration_request(request_id,payload_sha256,rule_version,product_id,draft,created_masters)
    VALUES(r,h,ver,product_id,d,created);
  INSERT INTO poc_registration.registration_audit(request_id,product_id,rule_version,payload_sha256) VALUES(r,product_id,ver,h);
  INSERT INTO poc_registration.indexing_job(product_id,request_id) VALUES(product_id,r);
  SET CONSTRAINTS ALL IMMEDIATE;
  RETURN poc_registration.registration_status(r);
END $$;

CREATE FUNCTION poc_registration.eligible(ids numeric[] DEFAULT NULL) RETURNS jsonb
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
  SELECT coalesce(jsonb_agg(jsonb_build_object('id',p.m_product_id,'code',p.value,'name',p.name,'description',p.description,
    'category',p.m_product_category_id,'uom',p.c_uom_id,'tax',p.c_taxcategory_id,
    'category_name',c.name,'uom_name',u.name,'tax_name',t.name,'usage',p.group2,'weight',p.weight,'pack',p.unitsperpack) ORDER BY p.m_product_id),'[]'::jsonb)
  FROM adempiere.m_product p
  JOIN adempiere.m_product_category c ON c.m_product_category_id=p.m_product_category_id
  JOIN adempiere.c_uom u ON u.c_uom_id=p.c_uom_id
  JOIN adempiere.c_taxcategory t ON t.c_taxcategory_id=p.c_taxcategory_id
  WHERE p.ad_client_id=11 AND p.ad_org_id IN(0,11) AND p.isactive='Y' AND p.producttype='I'
    AND p.issummary='N' AND coalesce(p.discontinued,'N')<>'Y' AND (ids IS NULL OR p.m_product_id=ANY(ids))
    AND c.isactive='Y' AND ((c.ad_client_id=0 AND c.ad_org_id=0) OR (c.ad_client_id=11 AND c.ad_org_id IN(0,11)))
    AND u.isactive='Y' AND ((u.ad_client_id=0 AND u.ad_org_id=0) OR (u.ad_client_id=11 AND u.ad_org_id IN(0,11)))
    AND t.isactive='Y' AND ((t.ad_client_id=0 AND t.ad_org_id=0) OR (t.ad_client_id=11 AND t.ad_org_id IN(0,11)))
$$;

CREATE FUNCTION poc_registration.claim_indexing(n integer) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
DECLARE result jsonb;
BEGIN
  WITH candidates AS (SELECT product_id FROM poc_registration.indexing_job
    WHERE status='pending' AND (lease_until IS NULL OR lease_until<clock_timestamp())
    ORDER BY updated_at,product_id LIMIT greatest(1,least(n,1000)) FOR UPDATE SKIP LOCKED),
  claimed AS (UPDATE poc_registration.indexing_job j SET attempts=j.attempts+1,lease_token=gen_random_uuid(),
    lease_until=clock_timestamp()+interval '2 minutes',updated_at=clock_timestamp()
    FROM candidates c WHERE j.product_id=c.product_id RETURNING j.product_id,j.attempts,j.lease_token)
  SELECT coalesce(jsonb_agg(to_jsonb(claimed)),'[]'::jsonb) INTO result FROM claimed;
  RETURN result;
END $$;

CREATE FUNCTION poc_registration.finish_indexing(p numeric,token uuid,error_code text) RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,poc_registration AS $$
BEGIN
  UPDATE poc_registration.indexing_job SET status=CASE WHEN error_code IS NULL THEN 'indexed' ELSE 'pending' END,
    last_error=error_code,indexed_at=CASE WHEN error_code IS NULL THEN clock_timestamp() ELSE indexed_at END,
    lease_token=NULL,lease_until=NULL,updated_at=clock_timestamp()
    WHERE product_id=p AND status='pending' AND ((token IS NOT NULL AND lease_token=token) OR (token IS NULL AND lease_token IS NULL));
  RETURN FOUND;
END $$;

REVOKE ALL ON ALL TABLES IN SCHEMA poc_registration FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA poc_registration FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA poc_registration FROM PUBLIC;
GRANT USAGE ON SCHEMA poc_registration TO poc_registration_api;
GRANT EXECUTE ON FUNCTION poc_registration.masters(),poc_registration.check_draft(jsonb),
  poc_registration.registration_status(uuid),poc_registration.begin_registration(uuid,text,text),
  poc_registration.finish_registration(uuid,text,text,jsonb),poc_registration.eligible(numeric[]),
  poc_registration.claim_indexing(integer),poc_registration.finish_indexing(numeric,uuid,text) TO poc_registration_api;
RESET ROLE;
