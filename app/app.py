from __future__ import annotations

from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="CORDIS → SDG Target Mapper",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


ROOT = Path(__file__).resolve().parents[1]

MAPPING_PATH = (
    ROOT
    / "data"
    / "cordis_sdg_mapping.csv"
)

PROJECT_PATH = (
    ROOT
    / "data"
    / "project_mapping_summary.csv"
)

UNCERTAIN_PATH = (
    ROOT
    / "data"
    / "uncertain_system_cases.csv"
)

EXCEL_PATH = (
    ROOT
    / "data"
    / "CORDIS_SDG_Final_Mapping.xlsx"
)

QC_PATH = (
    ROOT
    / "artifacts"
    / "quality_report.json"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    .hero {
        padding: 1.7rem 1.8rem;
        border: 1px solid rgba(120,120,120,0.25);
        border-radius: 18px;
        margin-bottom: 1.4rem;
    }

    .hero h1 {
        margin-bottom: 0.25rem;
        font-size: 2.35rem;
    }

    .hero p {
        margin-bottom: 0;
        font-size: 1.05rem;
        opacity: 0.82;
    }

    .section-note {
        padding: 0.85rem 1rem;
        border-left: 4px solid #808080;
        background: rgba(128,128,128,0.08);
        border-radius: 6px;
        margin-bottom: 1rem;
    }

    .target-title {
        font-size: 1.05rem;
        font-weight: 700;
    }

    .small-muted {
        opacity: 0.72;
        font-size: 0.9rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(120,120,120,0.23);
        padding: 0.8rem 1rem;
        border-radius: 14px;
    }

    div[data-testid="stExpander"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_data():

    mapping = pd.read_csv(
        MAPPING_PATH
    )

    projects = pd.read_csv(
        PROJECT_PATH
    )

    uncertain = pd.read_csv(
        UNCERTAIN_PATH
    )

    qc = pd.read_json(
        QC_PATH,
        typ="series",
    )

    mapping["project_id"] = (
        mapping["project_id"]
        .astype(str)
    )

    projects["project_id"] = (
        projects["project_id"]
        .astype(str)
    )

    uncertain["project_id"] = (
        uncertain["project_id"]
        .astype(str)
    )

    mapping["sdg_goal"] = (
        pd.to_numeric(
            mapping["sdg_goal"],
            errors="coerce",
        )
        .astype("Int64")
    )

    return (
        mapping,
        projects,
        uncertain,
        qc,
    )


mapping, projects, uncertain, qc = load_data()


# ============================================================
# SHARED HELPERS
# ============================================================

def csv_bytes(frame):

    return frame.to_csv(
        index=False
    ).encode(
        "utf-8"
    )


def project_display(row):

    acronym = str(
        row.get(
            "acronym",
            "",
        )
        or ""
    ).strip()

    title = str(
        row.get(
            "title",
            "",
        )
        or ""
    ).strip()

    pid = str(
        row[
            "project_id"
        ]
    )

    if acronym and acronym.lower() != "nan":
        return (
            f"{acronym} — "
            f"{title} [{pid}]"
        )

    return (
        f"{title} [{pid}]"
    )


def mapping_order(frame):

    if frame.empty:
        return frame

    ordered = frame.copy()

    ordered["_confidence_order"] = (
        ordered[
            "confidence_level"
        ].map({
            "HIGH": 0,
            "MEDIUM": 1,
        }).fillna(9)
    )

    ordered = ordered.sort_values(
        [
            "_confidence_order",
            "retrieval_rank",
            "target_code",
        ]
    )

    return ordered.drop(
        columns=[
            "_confidence_order"
        ]
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>CORDIS → UN SDG Target Mapper</h1>
        <p>
            Explainable mapping of European research projects to
            precise UN Sustainable Development Goal targets.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title(
    "CORDIS → SDG"
)

st.sidebar.caption(
    "Explainable exact-target mapping"
)

page = st.sidebar.radio(
    "Explore",
    [
        "Overview",
        "Project Explorer",
        "Mapping Explorer",
        "SDG Explorer",
        "Method & Validation",
        "Downloads",
    ],
)

st.sidebar.divider()

st.sidebar.markdown(
    "**Final production dataset**"
)

st.sidebar.write(
    "150 projects"
)

st.sidebar.write(
    "231 supported mappings"
)

st.sidebar.write(
    "100 mapped projects"
)

st.sidebar.caption(
    "Frozen production outputs — no live LLM calls."
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header(
        "Final mapping overview"
    )

    st.markdown(
        """
        <div class="section-note">
        The system does not force every project into an SDG.
        A mapping is published only when the verifier finds sufficient
        evidence for an exact SDG target.
        </div>
        """,
        unsafe_allow_html=True,
    )


    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Projects analysed",
        f"{len(projects):,}",
    )

    c2.metric(
        "Candidate relationships",
        "1,500",
    )

    c3.metric(
        "Supported mappings",
        f"{len(mapping):,}",
    )


    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Projects mapped",
        int(
            (
                projects[
                    "n_supported_mappings"
                ]
                > 0
            ).sum()
        ),
    )

    c5.metric(
        "HIGH confidence",
        int(
            (
                mapping[
                    "confidence_level"
                ]
                == "HIGH"
            ).sum()
        ),
    )

    c6.metric(
        "DIRECT contributions",
        int(
            (
                mapping[
                    "contribution_type"
                ]
                == "DIRECT"
            ).sum()
        ),
    )


    st.divider()

    left, right = st.columns(
        [1.45, 1]
    )


    with left:

        st.subheader(
            "Mappings by SDG Goal"
        )

        goal_counts = (
            mapping[
                "sdg_goal"
            ]
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
        )

        goal_frame = pd.DataFrame({
            "SDG Goal":
                goal_counts.index.astype(str),

            "Supported mappings":
                goal_counts.values,
        }).set_index(
            "SDG Goal"
        )

        st.bar_chart(
            goal_frame
        )


    with right:

        st.subheader(
            "Confidence"
        )

        confidence_counts = (
            mapping[
                "confidence_level"
            ]
            .value_counts()
            .reindex(
                [
                    "HIGH",
                    "MEDIUM",
                ]
            )
            .fillna(0)
        )

        st.bar_chart(
            confidence_counts
        )

        st.caption(
            "HIGH = STRONG verifier judgment; "
            "MEDIUM = WEAK verifier judgment. "
            "These are categorical labels, not probabilities."
        )


    left, right = st.columns(
        [1, 1]
    )


    with left:

        st.subheader(
            "Contribution type"
        )

        contribution_counts = (
            mapping[
                "contribution_type"
            ]
            .value_counts()
            .reindex(
                [
                    "DIRECT",
                    "INDIRECT",
                ]
            )
            .fillna(0)
        )

        st.bar_chart(
            contribution_counts
        )


    with right:

        st.subheader(
            "Mapping coverage"
        )

        mapped_projects = int(
            (
                projects[
                    "n_supported_mappings"
                ]
                > 0
            ).sum()
        )

        coverage = pd.Series({
            "Mapped":
                mapped_projects,

            "No supported target":
                len(projects)
                - mapped_projects,
        })

        st.bar_chart(
            coverage
        )


    st.subheader(
        "Most frequently supported exact targets"
    )

    top_targets = (
        mapping[
            "target_code"
        ]
        .value_counts()
        .head(15)
    )

    st.bar_chart(
        top_targets
    )


    with st.expander(
        "How should these results be interpreted?"
    ):

        st.markdown(
            """
            - **231 mappings** survived exact-target semantic verification.
            - **1,265 candidate relationships** were rejected as unsupported.
            - **50 projects** received no supported target among their top-10
              retrieved candidates.
            - **4 candidate relationships** produced system-invalid structured
              outputs and are kept outside the supported mapping table.
            - This conservative behaviour is intentional: no project is forced
              into an SDG simply because it is thematically similar.
            """
        )


# ============================================================
# PROJECT EXPLORER
# ============================================================

elif page == "Project Explorer":

    st.header(
        "Project Explorer"
    )

    st.write(
        "Inspect every supported SDG target for an individual "
        "CORDIS project, together with the evidence and explanation."
    )


    project_view = projects.copy()

    project_view[
        "display"
    ] = project_view.apply(
        project_display,
        axis=1,
    )


    selected_display = st.selectbox(
        "Search or select a project",
        project_view[
            "display"
        ].tolist(),
    )


    project_row = project_view[
        project_view[
            "display"
        ]
        == selected_display
    ].iloc[0]


    pid = str(
        project_row[
            "project_id"
        ]
    )


    st.subheader(
        str(
            project_row[
                "title"
            ]
        )
    )


    a, b, c, d = st.columns(4)

    acronym = str(
        project_row.get(
            "acronym",
            "",
        )
    )

    if acronym.lower() == "nan":
        acronym = "—"


    a.metric(
        "CORDIS ID",
        pid,
    )

    b.metric(
        "Acronym",
        acronym,
    )

    c.metric(
        "Framework",
        str(
            project_row.get(
                "framework",
                "—",
            )
        ),
    )

    d.metric(
        "Supported targets",
        int(
            project_row[
                "n_supported_mappings"
            ]
        ),
    )


    matches = mapping_order(
        mapping[
            mapping[
                "project_id"
            ]
            == pid
        ]
    )


    st.divider()


    if matches.empty:

        st.info(
            "No supported SDG target was found among this project's "
            "top-10 retrieved candidates."
        )

        st.caption(
            "This is an explicit no-mapping outcome rather than a "
            "forced classification."
        )


    else:

        st.markdown(
            f"### {len(matches)} supported target"
            + (
                ""
                if len(matches) == 1
                else "s"
            )
        )


        for _, row in matches.iterrows():

            heading = (
                f"SDG {row['target_code']} · "
                f"{row['confidence_level']} · "
                f"{row['contribution_type']}"
            )


            with st.expander(
                heading,
                expanded=True,
            ):

                st.markdown(
                    '<div class="target-title">'
                    + escape(str(
                        row[
                            "target_wording"
                        ]
                    ))
                    + "</div>",
                    unsafe_allow_html=True,
                )


                m1, m2, m3 = st.columns(3)

                m1.metric(
                    "Confidence",
                    row[
                        "confidence_level"
                    ],
                )

                m2.metric(
                    "Contribution",
                    row[
                        "contribution_type"
                    ],
                )

                m3.metric(
                    "Retrieval rank",
                    int(
                        row[
                            "retrieval_rank"
                        ]
                    ),
                )


                st.markdown(
                    "#### Evidence from the CORDIS project"
                )

                st.info(
                    str(
                        row[
                            "evidence"
                        ]
                    )
                )


                st.markdown(
                    "#### Why this target is supported"
                )

                st.write(
                    str(
                        row[
                            "explanation"
                        ]
                    )
                )


                limitations = row.get(
                    "outcome_limitations"
                )

                if (
                    pd.notna(
                        limitations
                    )
                    and str(
                        limitations
                    ).strip()
                ):

                    st.markdown(
                        "#### Outcome limitations"
                    )

                    st.warning(
                        str(
                            limitations
                        )
                    )


                with st.expander(
                    "Technical details"
                ):

                    st.write(
                        "**Target URI:**",
                        row[
                            "concept_uri"
                        ],
                    )

                    st.write(
                        "**Retrieval similarity:**",
                        round(
                            float(
                                row[
                                    "retrieval_score"
                                ]
                            ),
                            4,
                        ),
                    )

                    st.write(
                        "**Evidence segment IDs:**",
                        row[
                            "evidence_segment_ids"
                        ],
                    )

                    st.write(
                        "**Source fields:**",
                        row[
                            "source_fields"
                        ],
                    )

                    st.caption(
                        "Confidence is categorical and is not a "
                        "calibrated probability."
                    )


# ============================================================
# MAPPING EXPLORER
# ============================================================

elif page == "Mapping Explorer":

    st.header(
        "Mapping Explorer"
    )

    st.write(
        "Filter and inspect all 231 supported project-target mappings."
    )


    f1, f2, f3 = st.columns(3)


    with f1:

        search = st.text_input(
            "Project search",
            placeholder=(
                "Title, acronym, ID or target..."
            ),
        )


    with f2:

        confidence_filter = st.multiselect(
            "Confidence",
            [
                "HIGH",
                "MEDIUM",
            ],
            default=[
                "HIGH",
                "MEDIUM",
            ],
        )


    with f3:

        contribution_filter = st.multiselect(
            "Contribution",
            [
                "DIRECT",
                "INDIRECT",
            ],
            default=[
                "DIRECT",
                "INDIRECT",
            ],
        )


    available_goals = sorted(
        mapping[
            "sdg_goal"
        ]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )


    goal_filter = st.multiselect(
        "SDG Goals",
        available_goals,
        default=available_goals,
    )


    filtered = mapping[
        mapping[
            "confidence_level"
        ].isin(
            confidence_filter
        )
        &
        mapping[
            "contribution_type"
        ].isin(
            contribution_filter
        )
        &
        mapping[
            "sdg_goal"
        ].isin(
            goal_filter
        )
    ].copy()


    if search.strip():

        needle = search.strip().lower()

        haystack = (
            filtered[
                "project_id"
            ].fillna("").astype(str)
            + " "
            + filtered[
                "project_acronym"
            ].fillna("").astype(str)
            + " "
            + filtered[
                "project_title"
            ].fillna("").astype(str)
            + " "
            + filtered[
                "target_code"
            ].fillna("").astype(str)
            + " "
            + filtered[
                "target_wording"
            ].fillna("").astype(str)
        ).str.lower()

        filtered = filtered[
            haystack.str.contains(
                needle,
                regex=False,
            )
        ]


    a, b, c = st.columns(3)

    a.metric(
        "Filtered mappings",
        len(filtered),
    )

    b.metric(
        "Unique projects",
        filtered[
            "project_id"
        ].nunique(),
    )

    c.metric(
        "Exact targets",
        filtered[
            "target_code"
        ].nunique(),
    )


    display_columns = [
        "project_id",
        "project_acronym",
        "project_title",
        "target_code",
        "confidence_level",
        "contribution_type",
        "retrieval_rank",
        "evidence",
        "explanation",
    ]


    st.dataframe(
        filtered[
            display_columns
        ],
        width="stretch",
        hide_index=True,
        height=580,
    )


    st.download_button(
        "Download filtered mappings as CSV",
        data=csv_bytes(
            filtered
        ),
        file_name=(
            "filtered_cordis_sdg_mappings.csv"
        ),
        mime="text/csv",
    )


# ============================================================
# SDG EXPLORER
# ============================================================

elif page == "SDG Explorer":

    st.header(
        "SDG Explorer"
    )

    st.write(
        "Explore how the selected CORDIS projects map to "
        "individual SDG Goals and exact targets."
    )


    goals = sorted(
        mapping[
            "sdg_goal"
        ]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )


    selected_goal = st.selectbox(
        "Select SDG Goal",
        goals,
    )


    subset = mapping[
        mapping[
            "sdg_goal"
        ]
        == selected_goal
    ].copy()


    a, b, c, d = st.columns(4)

    a.metric(
        "Supported mappings",
        len(subset),
    )

    b.metric(
        "Projects",
        subset[
            "project_id"
        ].nunique(),
    )

    c.metric(
        "HIGH confidence",
        int(
            (
                subset[
                    "confidence_level"
                ]
                == "HIGH"
            ).sum()
        ),
    )

    d.metric(
        "DIRECT",
        int(
            (
                subset[
                    "contribution_type"
                ]
                == "DIRECT"
            ).sum()
        ),
    )


    target_counts = (
        subset[
            "target_code"
        ]
        .value_counts()
    )


    st.subheader(
        "Exact target distribution"
    )

    st.bar_chart(
        target_counts
    )


    selected_targets = st.multiselect(
        "Filter exact targets",
        sorted(
            subset[
                "target_code"
            ]
            .unique()
            .tolist()
        ),
        default=sorted(
            subset[
                "target_code"
            ]
            .unique()
            .tolist()
        ),
    )


    table = subset[
        subset[
            "target_code"
        ].isin(
            selected_targets
        )
    ]


    st.dataframe(
        table[
            [
                "project_id",
                "project_acronym",
                "project_title",
                "target_code",
                "target_wording",
                "confidence_level",
                "contribution_type",
                "explanation",
            ]
        ],
        width="stretch",
        hide_index=True,
        height=550,
    )


# ============================================================
# METHOD & VALIDATION
# ============================================================

elif page == "Method & Validation":

    st.header(
        "Methodology & validation"
    )


    st.subheader(
        "Pipeline"
    )

    st.markdown(
        """
        **CORDIS project**
        → project objective + metadata
        → **MiniLM retrieval**
        → 169 SDG targets
        → **top 10 candidates**
        → exact-target scope verification
        → depth/contribution verification
        → deterministic composition
        → **evidence-backed mapping**
        """
    )


    st.markdown(
        """
        ### Retrieval

        Candidate generation uses
        `sentence-transformers/all-MiniLM-L6-v2`.

        For each project:

        `0.7 × max objective-chunk similarity + 0.3 × metadata similarity`

        The objective is divided into overlapping chunks
        (`width=220`, `overlap=40`).
        """
    )


    st.markdown(
        """
        ### Semantic verification

        The verifier checks the **exact target**, not just the broad
        SDG Goal.

        A thematic keyword overlap is not enough. The project must
        perform, enable or materially support an action or outcome
        contained in the target.
        """
    )


    st.divider()

    st.subheader(
        "Human-reviewed development benchmark"
    )


    a, b, c, d = st.columns(4)

    a.metric(
        "Reviewed pairs",
        240,
    )

    b.metric(
        "Overlap rows",
        40,
    )

    c.metric(
        "Exact agreement",
        "87.5%",
    )

    d.metric(
        "Binary agreement",
        "92.5%",
    )


    st.markdown(
        """
        The frozen V8 development architecture using GPT-5.4 Mini
        achieved:

        - **86.67%** exact three-class accuracy
        - **93.33%** supported-vs-unsupported accuracy
        - **90.0%** supported precision
        - **75.0%** supported recall
        - **77.78%** contribution accuracy (28/36 pairs supported by both reference and prediction)

        These were **development results**, not an untouched
        confirmatory test.
        """
    )


    st.warning(
        "The final production deployment uses GPT-6 Luna. "
        "Historical metrics from other model/configuration combinations "
        "are not claimed as an independent accuracy estimate for the "
        "exact final deployment."
    )


    st.divider()

    st.error("V8 FAILED the complete internal development gate. Exact matches were 208/240; STRONG recall 40%, supported recall 75%, and WEAK precision 30.77% missed their gate thresholds.")
    st.markdown("STRONG precision: **85.71%**; STRONG recall: **40%**. WEAK precision: **30.77%**; WEAK recall: **44.44%**. These describe the reused development benchmark, not final Luna accuracy.")
    st.warning("Production evaluated 169 Targets only. Indicators/Series were not evaluated. The frozen scope prompt says ONE Horizon Europe project, but 42 of 150 projects are OTHER (420 scope calls; 28 supported mappings). The prompt was not changed and these results were not rerun.")
    st.caption("This deterministic 150-project demonstration is not a probability sample of CORDIS. The original upstream download date is unavailable. Reproducibility here covers frozen-output checks and analysis; final selection/retrieval scripts were not recovered.")
    st.subheader(
        "Production quality control"
    )

    q1, q2, q3, q4 = st.columns(4)

    q1.metric(
        "Final candidates",
        "1,500",
    )

    q2.metric(
        "Contract-valid",
        "1,496",
    )

    q3.metric(
        "System-invalid",
        "4",
    )

    q4.metric(
        "Supported mappings",
        "231",
    )


    st.success(
        "All public supported mappings are contract-valid, "
        "contain evidence IDs and explanations, and have no "
        "duplicate project-target keys."
    )


    st.subheader(
        "Known limitations"
    )

    st.markdown(
        """
        1. **Top-10 retrieval boundary** — targets outside the top ten
           cannot be recovered by the semantic verifier.
        2. **No full final human ground truth** — final mappings are
           model-supported rather than individually human-certified.
        3. **STRONG vs WEAK calibration** is less stable than the broader
           supported-vs-unsupported distinction.
        4. **Confidence is categorical**, not probabilistic.
        5. **Four structured outputs were invalid** and are preserved
           separately rather than manually repaired.
        6. **Fifty projects are intentionally unmapped** because no
           retrieved target passed the support threshold.
        """
    )


# ============================================================
# DOWNLOADS
# ============================================================

elif page == "Downloads":

    st.header(
        "Download final outputs"
    )

    st.write(
        "These files contain the frozen production mapping results."
    )


    st.subheader(
        "Primary mapping dataset"
    )

    st.download_button(
        "Download mapping CSV",
        data=MAPPING_PATH.read_bytes(),
        file_name="cordis_sdg_mapping.csv",
        mime="text/csv",
    )

    st.caption(
        "231 supported project → exact SDG target mappings."
    )


    st.download_button(
        "Download complete Excel workbook",
        data=EXCEL_PATH.read_bytes(),
        file_name="CORDIS_SDG_Final_Mapping.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )

    st.caption(
        "Includes mappings, all 150 projects, uncertain cases "
        "and QC summaries."
    )


    st.subheader(
        "Supporting outputs"
    )

    st.download_button(
        "Download project summary",
        data=PROJECT_PATH.read_bytes(),
        file_name="project_mapping_summary.csv",
        mime="text/csv",
    )

    st.download_button(
        "Download system-uncertain cases",
        data=UNCERTAIN_PATH.read_bytes(),
        file_name="uncertain_system_cases.csv",
        mime="text/csv",
    )


    st.divider()

    st.markdown(
        """
        ### Dataset interpretation

        **HIGH** = STRONG semantic support.

        **MEDIUM** = WEAK but supported semantic relationship.

        **DIRECT** = the project directly performs or delivers an action
        central to the target relationship.

        **INDIRECT** = the project materially enables or supports the
        target without directly performing the final target outcome.

        These categories are descriptive labels, not calibrated
        probabilities.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CORDIS → SDG Target Mapper · Frozen final production results · "
    "No live LLM inference in this application"
)
