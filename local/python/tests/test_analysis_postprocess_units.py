"""Independent host checks for renderer provenance and unverified measure units."""

import copy
import hashlib
import json
from pathlib import Path

import pytest

from poc.analysis_postprocess import checked_insights, facts_for, verify_manifest
from poc.config import PocError


RESULT_ID = "45815b76-95b4-4c1a-a0c2-409ab73d3200"


@pytest.fixture
def compound():
    result = {"status":"succeeded", "columns":["producttype","issold","currency","product_count"],
              "rows":[["I","N","USD",5],["I","Y","USD",5],["I","N","KRW",4]], "row_count":3,"truncated":False}
    chart = {"type":"bar","x":"producttype","y":"product_count","label_columns":["producttype","issold"],
             "currency_column":"currency","value_unit":"건","x_label":"상품 유형 / 판매 여부","y_label":"건수"}
    manifest = {"result_id":RESULT_ID,"currency":"USD","unit":"건","font":"Malgun Gothic","font_file":"malgun.ttf",
        "font_sha256":hashlib.sha256(Path("C:/Windows/Fonts/malgun.ttf").read_bytes()).hexdigest(),
        "legend":"건수 (건)","y_label":"건수 (건)","x_label":chart["x_label"],"minus_sign":"-","row_count":2,
        "layout":{"orientation":"horizontal","label_wrap_width":120,"label_font_size":9,"horizontal_axis_label":"건수 (건)","vertical_axis_label":"구분"},
        "label_columns":chart["label_columns"].copy(),"series":[]}
    for index, row in enumerate(result["rows"][:2]):
        manifest["series"].append({"row_index":index,"label_columns":chart["label_columns"].copy(),"label_values":row[:2],
            "label":json.dumps(dict(zip(chart["label_columns"],row[:2])),ensure_ascii=False,separators=(', ', ': ')),
            "display_label":json.dumps(dict(zip(chart["label_columns"],row[:2])),ensure_ascii=False,separators=(', ', ': ')),
            "value":row[3],"decimal_value":str(row[3]),"rendered_value":float(row[3]),"unit":"건"})
    return result,chart,manifest


def test_host_accepts_exact_compound_labels_with_repeated_x_and_equal_y(compound):
    result, chart, manifest = compound
    assert manifest["series"][0]["label"] != manifest["series"][1]["label"]
    assert manifest["series"][0]["value"] == manifest["series"][1]["value"]
    verify_manifest(manifest,result,chart,RESULT_ID)


@pytest.mark.parametrize("mutate", [
    lambda m:m.pop("layout"),
    lambda m:m["layout"].update(orientation="vertical"),
    lambda m:m["layout"].update(label_wrap_width=100),
    lambda m:m["layout"].update(label_font_size=7),
    lambda m:m["layout"].update(horizontal_axis_label="USD"),
    lambda m:m["layout"].update(vertical_axis_label="수량"),
    lambda m:m["series"][0].update(display_label="I / N"),
    lambda m:m["series"][0].pop("display_label"),
])
def test_host_checks_actual_horizontal_axes_and_full_display_label_against_original(compound, mutate):
    result, chart, manifest = compound
    mutate(manifest)
    with pytest.raises(PocError, match="CHART_MANIFEST_MISMATCH"):
        verify_manifest(manifest,result,chart,RESULT_ID)


@pytest.mark.parametrize("mutate", [
    lambda m:m["series"][0].update(label='I'),
    lambda m:m.update(label_columns=["issold","producttype"]),
    lambda m:m["series"][0].update(label_columns=["issold","producttype"]),
    lambda m:m["series"][0].update(label_values=["I","Y"]),
    lambda m:m["series"][0].pop("label_values"),
    lambda m:m["series"][0].pop("label_columns"),
    lambda m:m["series"][0].update(row_index=1),
    lambda m:m["series"].reverse(),
    lambda m:m["series"].pop(),
    lambda m:m["series"][0].update(row_index=-1),
    lambda m:m["series"][0].update(row_index=0.0),
    lambda m:m["series"][0].update(row_index=False),
], ids=["flattened_label","manifest_columns","series_columns","raw_values","missing_values","missing_columns","wrong_index","reordered_rows","missing_row","negative_index","float_index","bool_index"])
def test_host_rejects_compound_provenance_tampering(compound,mutate):
    result,chart,manifest=compound
    mutate(manifest)
    with pytest.raises(PocError) as error:
        verify_manifest(manifest,result,chart,RESULT_ID)
    assert error.value.code=="CHART_MANIFEST_MISMATCH"


def test_host_rejects_duplicate_full_label_even_when_row_indices_are_intact(compound):
    result,chart,manifest=compound
    result["rows"][1][1]="N"
    manifest["series"][1]["label_values"]=["I","N"]
    manifest["series"][1]["label"]=manifest["series"][0]["label"]
    with pytest.raises(PocError):
        verify_manifest(manifest,result,chart,RESULT_ID)


def test_host_rejects_bool_substitution_for_numeric_label_value(compound):
    result,chart,manifest=compound
    result["rows"][0][1]=1
    manifest["series"][0]["label_values"]=["I",1]
    manifest["series"][0]["label"]=json.dumps({"producttype":"I","issold":1},separators=(', ', ': '))
    manifest["series"][0]["display_label"]=manifest["series"][0]["label"]
    verify_manifest(manifest,result,chart,RESULT_ID)
    manifest["series"][0]["label_values"]=["I",True]
    with pytest.raises(PocError):
        verify_manifest(manifest,result,chart,RESULT_ID)


def test_host_rejects_bool_substitution_for_original_measure(compound):
    result,chart,manifest=compound
    result["rows"][0][3]=1
    manifest["series"][0].update(value=1,decimal_value="1",rendered_value=1.0)
    verify_manifest(manifest,result,chart,RESULT_ID)
    manifest["series"][0]["value"]=True
    with pytest.raises(PocError):
        verify_manifest(manifest,result,chart,RESULT_ID)


def test_host_rejects_bool_substitution_for_scalar_numeric_label(compound):
    result,chart,manifest=compound
    chart["label_columns"]=["producttype"]
    manifest["label_columns"]=["producttype"]
    manifest.pop("layout")
    for index,item in enumerate(manifest["series"]):
        result["rows"][index][0]=index+1
        item.update(label=index+1,label_columns=["producttype"],label_values=[index+1])
    verify_manifest(manifest,result,chart,RESULT_ID)
    manifest["series"][0]["label"]=True
    with pytest.raises(PocError):
        verify_manifest(manifest,result,chart,RESULT_ID)


@pytest.mark.parametrize("unknown_unit",["수량 단위 미검증","단위 미검증"])
def test_unverified_units_expose_only_row_count_not_extrema(compound,unknown_unit):
    result,chart,_=compound
    chart["value_unit"]=unknown_unit
    snapshot=copy.deepcopy(result)
    stats,facts,limitations=facts_for(result,chart)
    assert result==snapshot
    assert stats=={"row_count":3,"groups":[]}
    assert facts==["조회 결과는 3행입니다."]
    assert any("단위를 확정하지 못해" in text for text in limitations)
    accepted=checked_insights({"observations":facts,"follow_up_questions":[]},facts,limitations,"test_host_checked")
    assert accepted["observations"]==facts
    with pytest.raises(PocError) as error:
        checked_insights({"observations":["USD의 product_count 최솟값은 5건, 최댓값은 5건입니다."]},facts,limitations,"test_host_checked")
    assert error.value.code=="INSIGHT_EVIDENCE_MISMATCH"


def test_verified_count_still_gets_per_currency_statistics(compound):
    result,chart,_=compound
    stats,facts,limitations=facts_for(result,chart)
    assert [(g["currency_partition"],g["unit"],g["minimum"],g["maximum"]) for g in stats["groups"]]==[("KRW","건","4","4"),("USD","건","5","5")]
    assert len(facts)==3
    assert not any("단위를 확정하지 못해" in text for text in limitations)


@pytest.mark.parametrize("unsafe", [
    "매출이 999달러인 이유는 무엇인가요?", "２０２６년과 비교할까요?",
    "마케팅 때문에 증가했나요?", "원인을 분석할까요?", "증가로 인해 바뀌었나요?",
    "What caused the increase?", "Did it increase BECAUSE of marketing?",
    "Was the change due to marketing?", "x" * 401, "", "  \t", None, 12, {}, [],
])
def test_optional_unsafe_questions_are_excluded_without_losing_verified_observations(unsafe):
    facts = ["조회 결과는 1행입니다."]
    limitations = ["인과관계를 확인하지 않았습니다."]
    value = {"observations": facts[:], "follow_up_questions": [
        "거래처별로 나누어 볼까요?", unsafe, "월별로 비교할까요?"],
        "limitations": ["모델이 만든 한계 문장"]}
    snapshot = copy.deepcopy(value)
    accepted = checked_insights(value, facts, limitations, "host_checked")
    assert accepted["observations"] == facts
    assert accepted["follow_up_questions"] == ["거래처별로 나누어 볼까요?", "월별로 비교할까요?"]
    assert accepted["limitations"][:-1] == limitations
    assert "제외했습니다" in accepted["limitations"][-1]
    assert accepted["provenance"] == "host_checked"
    assert value == snapshot
    assert limitations == ["인과관계를 확인하지 않았습니다."]


@pytest.mark.parametrize("questions", [None, "월별로 비교할까요?", {}, 7, True])
def test_malformed_optional_question_container_is_omitted_with_notice(questions):
    facts = ["조회 결과는 1행입니다."]
    accepted = checked_insights({"observations": facts, "follow_up_questions": questions}, facts, [], "test")
    assert accepted["follow_up_questions"] == []
    assert len(accepted["limitations"]) == 1
    assert "제외했습니다" in accepted["limitations"][0]


def test_optional_questions_keep_first_four_valid_items_and_report_exclusion():
    facts = ["조회 결과는 1행입니다."]
    valid = [f"{dimension}별로 비교할까요?" for dimension in ["거래처", "월", "상품", "조직", "통화"]]
    accepted = checked_insights({"observations": facts, "follow_up_questions": ["999?", *valid]}, facts, [], "test")
    assert accepted["follow_up_questions"] == valid[:4]
    assert len(accepted["limitations"]) == 1


@pytest.mark.parametrize("questions", [[], ["월별로 비교할까요?"], ["가", "나", "다", "라"]])
def test_valid_optional_questions_need_no_exclusion_notice(questions):
    facts = ["조회 결과는 1행입니다."]
    accepted = checked_insights({"observations": facts, "follow_up_questions": questions}, facts, [], "test")
    assert accepted["follow_up_questions"] == questions
    assert accepted["limitations"] == []
    assert checked_insights({"observations": facts}, facts, [], "test")["limitations"] == []


@pytest.mark.parametrize("observations", [None, [], "조회 결과는 1행입니다.",
    ["매출은 999입니다."], ["마케팅 때문에 매출이 증가했습니다."],
    ["조회 결과는 1행입니다.", "매출은 999입니다."], [None], [{}]])
def test_optional_question_filter_never_rescues_unverified_observations(observations):
    with pytest.raises(PocError) as error:
        checked_insights({"observations": observations, "follow_up_questions": ["999?", "월별로 비교할까요?"]},
                         ["조회 결과는 1행입니다."], [], "test")
    assert error.value.code == "INSIGHT_EVIDENCE_MISMATCH"


@pytest.mark.parametrize("value", [None, [], "invalid", 1])
def test_malformed_insight_response_is_a_structured_evidence_failure(value):
    with pytest.raises(PocError) as error:
        checked_insights(value, ["조회 결과는 1행입니다."], [], "test")
    assert error.value.code == "INSIGHT_EVIDENCE_MISMATCH"
