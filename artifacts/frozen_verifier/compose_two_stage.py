from __future__ import annotations
from typing import Any


class CompositionError(ValueError):
    pass


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise CompositionError(msg)


def validate_scope(
    result: dict[str, Any],
    supplied_ids: set[str],
) -> None:

    require(
        isinstance(result, dict),
        "scope result must be object",
    )

    required = {
        "eligibility",
        "claimed_component",
        "evidence_segment_ids",
        "scope_wording_id",
        "target_action_bridge",
        "defining_qualifier_status",
        "explanation",
    }

    require(
        set(result) == required,
        "scope result fields changed",
    )

    require(
        result["eligibility"]
        in {"ELIGIBLE", "NOT_ELIGIBLE"},
        "bad eligibility",
    )

    require(
        result["scope_wording_id"]
        == "target_wording",
        "bad scope wording id",
    )

    require(
        isinstance(
            result["claimed_component"],
            str,
        )
        and result["claimed_component"].strip(),
        "empty claimed component",
    )

    require(
        isinstance(result["explanation"], str)
        and result["explanation"].strip(),
        "empty explanation",
    )

    ids = result["evidence_segment_ids"]

    require(
        isinstance(ids, list),
        "evidence IDs must be list",
    )

    require(
        all(
            isinstance(x, str)
            and x in supplied_ids
            for x in ids
        ),
        "unknown evidence ID",
    )

    bridge = result["target_action_bridge"]
    qual = result["defining_qualifier_status"]

    require(
        bridge
        in {
            "DIRECT",
            "ENABLING",
            "ABSENT",
        },
        "bad bridge",
    )

    require(
        qual
        in {
            "SATISFIED",
            "NOT_APPLICABLE",
            "ABSENT",
        },
        "bad qualifier status",
    )

    if result["eligibility"] == "ELIGIBLE":

        require(
            bridge
            in {
                "DIRECT",
                "ENABLING",
            },
            "ELIGIBLE requires DIRECT or ENABLING bridge",
        )

        require(
            qual
            in {
                "SATISFIED",
                "NOT_APPLICABLE",
            },
            "ELIGIBLE qualifier inconsistency",
        )

        require(
            len(ids) > 0,
            "ELIGIBLE requires evidence",
        )

def validate_depth(
    result: dict[str, Any],
    supplied_ids: set[str],
) -> None:

    require(
        isinstance(result, dict),
        "depth result must be object",
    )

    required = {
        "judgment",
        "contribution",
        "claimed_component",
        "role_in_project",
        "realization_depth",
        "target_specificity",
        "material_gap",
        "causal_immediacy",
        "operative_action_alignment",
        "evidence_segment_ids",
        "scope_wording_id",
        "explanation",
        "outcome_limitations",
    }

    require(
        set(result) == required,
        "depth result fields changed",
    )

    require(
        result["judgment"]
        == "DEFER_TO_COMPOSER",
        "judgment must defer to composer",
    )

    require(
        result["contribution"]
        == "DEFER_TO_COMPOSER",
        "contribution must defer to composer",
    )

    require(
        result["scope_wording_id"]
        == "target_wording",
        "bad scope wording id",
    )

    require(
        isinstance(
            result["claimed_component"],
            str,
        )
        and result["claimed_component"].strip(),
        "empty claimed component",
    )

    require(
        result["role_in_project"]
        in {
            "CORE_OR_MAJOR",
            "SECONDARY",
        },
        "bad role",
    )

    require(
        result["realization_depth"]
        in {
            "PERFORMS_OR_INSTANTIATES_COMPONENT",
            "SUBSTANTIAL_TARGET_SPECIFIC_CAPACITY",
            "LIMITED_OR_NARROW_ENABLER",
        },
        "bad realization depth",
    )

    require(
        result["target_specificity"]
        in {
            "HIGH",
            "MODERATE",
        },
        "bad target specificity",
    )

    require(
        result["material_gap"]
        in {
            "NONE_OR_SCALE_ONLY",
            "MATERIAL_NONBLOCKING",
        },
        "bad material gap",
    )

    require(
        result["causal_immediacy"]
        in {
            "IMMEDIATE_TARGET_MECHANISM",
            "UPSTREAM_ENABLER",
        },
        "bad causal immediacy",
    )

    require(
        result["operative_action_alignment"]
        in {
            "GOVERNING_ACTION_MATCH",
            "CONSTITUENT_MECHANISM_ONLY",
        },
        "bad operative action alignment",
    )

    ids = result["evidence_segment_ids"]

    require(
        isinstance(ids, list)
        and len(ids) > 0,
        "depth requires evidence IDs",
    )

    require(
        all(
            isinstance(x, str)
            and x in supplied_ids
            for x in ids
        ),
        "unknown evidence ID",
    )

    require(
        isinstance(result["explanation"], str)
        and result["explanation"].strip(),
        "empty explanation",
    )

    require(
        isinstance(
            result["outcome_limitations"],
            list,
        )
        and all(
            isinstance(x, str)
            for x in result[
                "outcome_limitations"
            ]
        ),
        "bad limitations",
    )


def compose_strength(
    depth_result: dict[str, Any],
) -> str:

    strong = (
        depth_result["role_in_project"]
        == "CORE_OR_MAJOR"
        and depth_result[
            "operative_action_alignment"
        ] == "GOVERNING_ACTION_MATCH"
        and depth_result[
            "realization_depth"
        ]
        in {
            "PERFORMS_OR_INSTANTIATES_COMPONENT",
            "SUBSTANTIAL_TARGET_SPECIFIC_CAPACITY",
        }
    )

    if strong:
        return "STRONG"

    return "WEAK"

def compose_contribution(
    depth_result: dict[str, Any],
) -> str:

    if (
        depth_result["causal_immediacy"]
        == "IMMEDIATE_TARGET_MECHANISM"
    ):
        return "DIRECT"

    return "INDIRECT"


def compose(
    request_id: str,
    scope_result: dict[str, Any] | None,
    scope_valid: bool,
    depth_result: dict[str, Any] | None,
    depth_valid: bool,
    supplied_ids: set[str],
) -> dict[str, Any]:

    if (
        not scope_valid
        or scope_result is None
    ):

        return {
            "request_id": request_id,
            "final_contract_valid": False,
            "final_result": None,
            "error":
                "invalid_scope_gate",
        }

    try:
        validate_scope(
            scope_result,
            supplied_ids,
        )

    except Exception as exc:

        return {
            "request_id": request_id,
            "final_contract_valid": False,
            "final_result": None,
            "error":
                "scope_validation:"
                + str(exc),
        }

    if (
        scope_result["eligibility"]
        == "NOT_ELIGIBLE"
    ):

        return {
            "request_id":
                request_id,

            "final_contract_valid":
                True,

            "final_result": {
                "judgment":
                    "UNSUPPORTED",

                "contribution":
                    None,

                "claimed_component":
                    scope_result[
                        "claimed_component"
                    ],

                "evidence_segment_ids":
                    scope_result[
                        "evidence_segment_ids"
                    ],

                "scope_wording_id":
                    "target_wording",

                "explanation":
                    scope_result[
                        "explanation"
                    ],

                "outcome_limitations":
                    [],
            },

            "error":
                None,
        }

    if (
        not depth_valid
        or depth_result is None
    ):

        return {
            "request_id":
                request_id,

            "final_contract_valid":
                False,

            "final_result":
                None,

            "error":
                "invalid_required_depth_grader",
        }

    try:

        validate_depth(
            depth_result,
            supplied_ids,
        )

    except Exception as exc:

        return {
            "request_id":
                request_id,

            "final_contract_valid":
                False,

            "final_result":
                None,

            "error":
                "depth_validation:"
                + str(exc),
        }

    final_result = {

        "judgment":
            compose_strength(
                depth_result
            ),

        "contribution":
            compose_contribution(
                depth_result
            ),

        "claimed_component":
            depth_result[
                "claimed_component"
            ],

        "evidence_segment_ids":
            depth_result[
                "evidence_segment_ids"
            ],

        "scope_wording_id":
            "target_wording",

        "explanation":
            depth_result[
                "explanation"
            ],

        "outcome_limitations":
            depth_result[
                "outcome_limitations"
            ],
    }

    return {
        "request_id":
            request_id,

        "final_contract_valid":
            True,

        "final_result":
            final_result,

        "error":
            None,
    }
