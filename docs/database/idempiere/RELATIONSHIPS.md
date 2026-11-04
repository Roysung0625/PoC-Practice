# 외래키 흐름 읽기

[시작 안내](README.md) · [전체 테이블 일람](TABLE_INDEX.md)

물리 FK는 **3,807개**입니다. 각 관계를 자식 문서의 나가는 FK 표와 부모 문서의 들어오는 FK 표 양쪽에서 볼 수 있습니다. 자기참조 67개, 복합 FK 1개입니다.

## 방향과 해석

`자식 테이블(FK 열) → 부모 테이블(참조 열)`로 읽습니다. 예를 들어 `c_orderline.c_order_id → c_order.c_order_id`는 주문 상세가 주문 헤더를 참조한다는 뜻입니다. 물리 FK는 업무 발생 순서가 아니며, 자식 FK에 UNIQUE 제약이 있는지에 따라 대응 건수가 달라지므로 무조건 1:N으로 읽지 않습니다.

테이블별 Mermaid 그림은 주변 FK 최대 10개를 보여주는 요약입니다. **각 테이블 문서의 나가는·들어오는 FK 표는 생략 없는 전체 목록**입니다. 모든 자식·부모 테이블명은 해당 Markdown 문서로 연결됩니다.

## 복합 외래키

[`ad_registration`](ad/ad_registration.md)의 `(ad_system_id, ad_client_id)`는 [`ad_system`](ad/ad_system.md)의 `(ad_system_id, ad_client_id)`를 함께 참조합니다. 한 열만으로 조인하면 FK와 다른 의미가 됩니다.

```sql
-- 읽기 예시: 열의 순서를 유지하고 모든 대응을 함께 사용합니다.
SELECT child.ad_system_id, child.ad_client_id
FROM adempiere.ad_registration AS child
JOIN adempiere.ad_system AS parent
  ON child.ad_system_id = parent.ad_system_id
 AND child.ad_client_id = parent.ad_client_id;
```

## 빠뜨리면 안 되는 관계

- 자기참조는 같은 문서의 양쪽 표에 표시합니다. 전역 FK 개수를 셀 때는 제약조건 한 개로 계산합니다.
- `record_id` 같은 동적 참조나 애플리케이션 사전의 참조 설정은 물리 FK가 아닐 수 있습니다. 이 문서에는 실제 `pg_constraint`에 존재하는 FK만 넣었습니다.
- NULL 허용은 열 목록에서 확인합니다. FK가 있다는 사실만으로 필수 입력이라고 가정하지 않습니다.
- CASCADE·SET NULL 등은 **삭제/갱신 시 DB 제약 동작**을 설명합니다. 이 프로젝트의 SQL 조회 계정은 읽기 전용입니다.
- 부모의 총액을 상세와 조인한 후 그대로 합산하지 않습니다. 주문·청구·입출금은 서로 다른 지표입니다.
