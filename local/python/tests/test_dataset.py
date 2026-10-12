import pytest

from poc import dataset


def test_tpch_generator_preserves_eight_tables_and_decimal_amounts(tmp_path):
    generate = getattr(dataset, "generate", None)
    assert callable(generate), "TPC-H 생성기가 필요합니다."
    manifest = generate(tmp_path, 0.001)
    assert set(manifest["tables"]) == {"region", "nation", "supplier", "customer", "part", "partsupp", "orders", "lineitem"}
    assert manifest["tables"]["orders"]["count"] == 1500
    assert manifest["tables"]["region"]["count"] == 5
    assert dict(manifest["tables"]["lineitem"]["columns"])["l_extendedprice"] == "DECIMAL(15,2)"
    assert generate(tmp_path, 0.001) == manifest


def test_postgres_import_is_idempotent_and_catalog_is_real(postgres_db, tmp_path):
    import psycopg
    loader = getattr(dataset, "load_dataset", None)
    catalog_reader = getattr(dataset, "read_catalog", None)
    assert callable(loader) and callable(catalog_reader), "PostgreSQL 적재와 카탈로그 구현이 필요합니다."
    manifest = dataset.generate(tmp_path, 0.01)
    admin, reader, role = postgres_db
    loader(admin, tmp_path, role)
    loader(admin, tmp_path, role)
    with psycopg.connect(reader) as db:
        assert db.execute("SELECT count(*) FROM tpch.orders").fetchone()[0] == 15000
        with pytest.raises(psycopg.errors.ReadOnlySqlTransaction):
            db.execute("DELETE FROM tpch.orders")
        db.rollback()
        db.execute("SET TRANSACTION READ WRITE")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            db.execute("DELETE FROM tpch.orders")
    catalog = catalog_reader(reader)
    assert len(catalog["tables"]) == 8
    assert catalog["date_range"]["start"].startswith("1992")
    assert "STANDARD" in catalog["product_groups"]
    assert len(catalog["schema_version"]) == 64
