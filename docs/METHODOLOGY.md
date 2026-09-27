# Methodology

## Question and scope
Map each CORDIS project to zero or more exact UN SDG Targets, with inspectable evidence and explanations. Isolated keywords or broad topical similarity do not establish a contribution. Retrieval proposes candidates; the frozen verifier assesses target actions and defining qualifiers. No fixed number of accepted labels is forced.

## Source and demonstration population
The source is CORDIS project data. The frozen processed master source is `data/processed/projects_clean.csv`, SHA-256 `003dd63261ba9d31433c7c6f6753d55135700f4c88e53b8f8f94cd271e17a1b2`. This source path is provenance only and is not needed by this release. The original upstream download date is **unavailable**. The included final privacy-clean corpus is byte-identical to its frozen source.

The corpus manifest records 23,329 eligible projects after development/validation and reserve exclusions, minimum objective length 250 characters, 111 excluded development/validation IDs and 24 reserve IDs (metadata only). These selection-stage counts are retained manifest claims, not a new reproduction of corpus selection. The seed is `CORDIS_SDG_FINAL_SUBMISSION_2026_V1`; selection is described as deterministic balanced-proportional stratification, without SDG labels or prior predictions.

The original freeze omitted privacy eligibility. Its amendment records 1,350 privacy-blocked population candidates, then the identical hash ordering and stratum allocation with six deterministic replacements. The original unclean corpus is deliberately excluded from the release. No new selection or screening was used to change the final set.

| Framework/time stratum | Projects |
|---|---:|
| HORIZON_EUROPE, 2021–2023 | 40 |
| HORIZON_EUROPE, 2024+ | 68 |
| OTHER, 2021–2023 | 15 |
| OTHER, 2024+ | 27 |

## Taxonomy and retrieval
The retained EU Vocabularies SDG concept export contains 812 concepts, including 17 Goals and 169 Targets; additional Indicator/Series concepts are present. Production evaluated only the **169 Targets**. Blank narrower-concept fields do not mean narrower concepts were individually evaluated.

Recorded retriever: `sentence-transformers/all-MiniLM-L6-v2`. Objective chunks use width 220 and overlap 40. The final retrieval manifest records:

`0.7 × max(objective chunk similarity) + 0.3 × metadata similarity`

Metadata uses available title, keywords, EuroSciVoc and Horizon/topic fields. Top K=10 gives 1,500 pairs. The historical implementation uses normalized embeddings and descending score/URI tie-breaking; the final orchestration source was not recovered, so this release does not pretend that the final retrieval execution has been rerun or fully reconstructed. Candidate identities, finite scores and frozen order can be checked locally. A model name alone is not an immutable weights revision.

## Frozen V8 verification
Stage 1 checks exact-target eligibility, action bridge and defining qualifiers. Only valid ELIGIBLE results proceed to Stage 2. Stage 2 assesses role, realization depth, specificity, material gap, causal immediacy and operative action alignment; it defers final labels to the deterministic composer. Here “depth” is contribution depth within a Target, not Indicator/Series descent.

For valid eligible results, STRONG requires CORE_OR_MAJOR role, GOVERNING_ACTION_MATCH and either PERFORMS_OR_INSTANTIATES_COMPONENT or SUBSTANTIAL_TARGET_SPECIFIC_CAPACITY. Other valid eligible cases compose to WEAK. NOT_ELIGIBLE composes to UNSUPPORTED. DIRECT requires IMMEDIATE_TARGET_MECHANISM; other valid supported causal states compose to INDIRECT. Invalid required stages cannot become supported. The included composer is authoritative.

The production deployment used `gpt-6-luna`; historical development used GPT-5.4 Mini. These are distinct deployments. The app displays precomputed results only and cannot map new projects.

## Recorded API configuration
The prepared scope requests use the Responses API format, reasoning effort `none`, `store=false`, `tools=[]`, structured JSON-schema output, `max_output_tokens=1536`, `service_tier=default`. All 1,500 retained scope bodies were inspected for this configuration. The run summary records zero retries and no human-label transmission or reserve semantic access. The public release includes parsed composition inputs, not provider event logs or live authorization. All 234 retained depth provider responses echo gpt-6-luna, max_output_tokens=1536, service_tier=default, reasoning effort none, store=false and no tools. Full outbound depth request bodies are not retained here; provider echoes are identified separately from request provenance. See `artifacts/production_configuration.json` for the recorded scope settings and provenance.

| Frozen artifact | SHA-256 |
|---|---|
| candidate_pairs_sha256 | `6eab96127aacf69215b3acb33e205a15e3bc4883dc6ec241f6d7ad0c06a6a108` |
| candidate_payloads_sha256 | `b13b4bef875202e41cf3efbf9aee79544662156f565056b1bb969d9de76496e4` |
| composer_sha256 | `7ec0981ea8bddf4fb1c1feb585a8dcf763868e11de7f19c73ddadb986140dd79` |
| depth_prompt_sha256 | `334e6e07c7f6652d6146e8b09d164493ad4cd94f21ba1e8387187ddcb488d12c` |
| depth_schema_sha256 | `bbc71cfe704c06abbb93c645f25cd67ae9fdd7bcdc4a1b1fbc91851cac650722` |
| privacy_clean_corpus_sha256 | `7075a9da63228019f0968b5d7060a4c1ac266ebe421150517f504a44d1a19e96` |
| scope_prompt_sha256 | `94179b56cdec02d4afdf5c87acf22f207881e649b4f5cf222cffa3c1a5db35f9` |
| scope_requests_sha256 | `876144b6470ad556a3749c65f9439224bc49808c219c5acde09b5910c8ef21b4` |
| scope_schema_sha256 | `ff693135c38e894fc5b13def7545fe6b4cc09c8490fea8643594a233efd42293` |

## Evidence and uncertainty
Evidence segment IDs resolve to source fields and offsets in the same project's frozen corpus. Public evidence joins quoted segments with ` | ` and normalizes whitespace. The original segments are retained for exact inspection; normalized public display strings are not necessarily byte-for-byte source substrings. HIGH=STRONG and MEDIUM=WEAK are categorical labels, never calibrated probabilities. Retrieval scores are similarities, not confidence probabilities.

## Prompt mismatch
The scope prompt says `ONE Horizon Europe project`, but 42 OTHER projects were included (420 scope evaluations; 28 supported mappings). This frozen wording was not edited. Target/evidence-based verification does not prove immunity to that mismatch. The optional diagnostic CSV uses mechanical phrase checks, not a human semantic certification.

## Reproduction boundary
Run the offline integrity test and notebook to reproduce joins, composition, aggregate statistics and five figures from included frozen files. No full model inference, source download or selection is performed. Manifest-only stages and unknown upstream date remain disclosed limitations. API usage cost is an **estimate** of $0.63096, not a billing-verified invoice.
