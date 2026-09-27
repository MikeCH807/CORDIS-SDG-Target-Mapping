# Validation

## Human-reviewed development reference
The development reference contains 24 projects / 240 project-target pairs: STRONG 30, WEAK 18, UNSUPPORTED 192. Two reviewers each reviewed 140 rows, with 40 common project-target decisions. Pre-adjudication agreement was 35/40=87.5% for three-class judgment and 37/40=92.5% for supported/unsupported. Cohen's kappa was approximately 0.653 and 0.778 respectively. Kappa concerns the same overlapping project-target decisions, not disjoint projects or free multi-label set agreement. `artifacts/reviewer_agreement_summary.json` contains the aggregate recomputation; individual reviewer labels are not published here.

## Frozen V8 development result — GPT-5.4 Mini
| Metric | Value | Numerator / denominator |
|---|---:|---|
| Exact three-class accuracy | 86.67% | 208 / 240 |
| Binary accuracy | 93.33% | 224 / 240 |
| Supported precision | 90.00% | 36 / 40 |
| Supported recall | 75.00% | 36 / 48 |
| STRONG precision | 85.71% | 12 / 14 |
| STRONG recall | 40.00% | 12 / 30 |
| WEAK precision | 30.77% | 8 / 26 |
| WEAK recall | 44.44% | 8 / 18 |
| Contribution accuracy | 77.78% | 28 / 36 jointly supported pairs |

**V8 FAILED the complete internal development gate.** Exact matches 208 were below 216; STRONG recall 40% was below 75%; supported recall 75% was below 80%; WEAK precision 30.77% was below 50%. See the retained gate result and metrics JSON. Passing contract checks is not passing this quality gate.

Repeated development-set reuse means these figures are development evidence, not untouched confirmatory performance. They are not an accuracy estimate for the final GPT-6 Luna deployment. The final 150 projects have no full independent human reference; no final precision/recall or calibrated confidence is claimed.

## Final data/engineering checks
The offline release test checks protected hashes, all 1,500 deterministic compositions, 231 supported mappings and evidence ownership, confidence/contribution labels, all project summaries, taxonomy references and primary workbook/CSV equality. These are integrity checks, not semantic certification. No model is run by the release test. The four invalid cases are preserved without repair. The source audit found zero final/development and final/reserve ID overlap; reserve text is not included or read by this release.

## Future evaluation
If undertaken, human review must be independently locked before model labels are shown, use a representative sample and meaningful reviewer overlap, and report agreement on a defined common coding unit. No such new evaluation was performed in this release phase. Do not tune on a final evaluation resource and still call it untouched.
