from vitruvius.review_routing import select_for_second_pass, route_adjudication


def _t1(decision, confidence, suggested_type=None):
    return {
        "candidate": {"from": "a", "type": "governs", "to": "b"},
        "review": {
            "decision": decision, "confidence": confidence,
            "reason": "r", "suggested_type": suggested_type,
        },
    }


# ---------- entry criteria (select_for_second_pass) ----------

def test_skips_high_confidence_keep():
    assert select_for_second_pass([_t1("keep", 0.95)]) == []


def test_skips_high_confidence_reject():
    assert select_for_second_pass([_t1("reject", 0.95)]) == []


def test_routes_all_review_further():
    items = [_t1("review_further", 0.5), _t1("review_further", 0.95)]
    assert len(select_for_second_pass(items)) == 2


def test_routes_low_confidence_keep():
    assert len(select_for_second_pass([_t1("keep", 0.85)])) == 1


def test_routes_low_confidence_reject():
    assert len(select_for_second_pass([_t1("reject", 0.85)])) == 1


def test_routes_predicate_disagreement():
    items = [_t1("keep", 0.99, suggested_type="affects")]
    assert len(select_for_second_pass(items)) == 1


# ---------- post-Tier-2 routing (route_adjudication) ----------

def _pair(t1_decision, t1_conf, t2_decision, t2_conf):
    return {
        "tier_one": {"decision": t1_decision, "confidence": t1_conf},
        "tier_two": {"decision": t2_decision, "confidence": t2_conf} if t2_decision else None,
    }


def test_t1_keep_high_skipped():
    assert route_adjudication(_pair("keep", 0.95, None, None)) == "auto_promote"


def test_t1_keep_low_t2_keep_high():
    assert route_adjudication(_pair("keep", 0.85, "keep", 0.95)) == "auto_promote"


def test_t1_keep_low_t2_keep_low():
    assert route_adjudication(_pair("keep", 0.85, "keep", 0.85)) == "human_review"


def test_t1_keep_low_t2_reject():
    assert route_adjudication(_pair("keep", 0.85, "reject", 0.95)) == "human_review"


def test_t1_reject_low_t2_reject_high():
    assert route_adjudication(_pair("reject", 0.85, "reject", 0.95)) == "suppress"


def test_t1_reject_low_t2_keep():
    assert route_adjudication(_pair("reject", 0.85, "keep", 0.95)) == "human_review"


def test_t1_review_further_t2_keep_high():
    assert route_adjudication(_pair("review_further", 0.5, "keep", 0.95)) == "human_review"


def test_t1_review_further_t2_reject_high():
    assert route_adjudication(_pair("review_further", 0.5, "reject", 0.95)) == "suppress"


def test_t2_missing_defaults_to_human_review():
    # Low-confidence Tier 1 with no Tier 2 input → human review
    assert route_adjudication(_pair("keep", 0.85, None, None)) == "human_review"
