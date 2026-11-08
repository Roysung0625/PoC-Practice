"""Read-only top-ten checks for the Japanese GardenWorld catalog."""
import json
from product_registration.intelligence import RegistrationIntelligence
from product_registration.store import RegistrationStore


CASES = [
    ("ラベンダー苗", "name", "ラベンダー"),
    ("水やり用のジョウロ", "name", "ジョウロ"),
    ("有機肥料", "name", "有機肥料"),
    ("伸びた枝を切りそろえるための道具", "usage", "剪定ばさみ"),
    ("日差しを遮ってテラスに日陰を作るもの", "usage", "日よけシェード"),
]


def main():
    service, store = RegistrationIntelligence(), RegistrationStore()
    results = []
    for query, field, wanted in CASES:
        found = service.search({field: query}, store)
        rank = next((n for n, row in enumerate(found, 1) if wanted in row["name"]), None)
        results.append({"query": query, "wanted": wanted, "rank": rank, "returned": len(found)})
    print(json.dumps({"hit_at_10": sum(r["rank"] is not None for r in results),
                      "cases": len(results), "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
