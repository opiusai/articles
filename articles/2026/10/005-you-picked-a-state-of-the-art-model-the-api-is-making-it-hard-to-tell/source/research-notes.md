# Article 5 source and claim notes

Reviewed 2026-10-09. This is an editorial draft, not a route assessment or production benchmark.

## Primary sources

- https://inferock.ai/baseline/ and its Quality, Overview, and Route evidence sections.
- https://inferock.ai/watch/
- https://inferock.ai/how-it-works/
- https://inferock.ai/docs/quickstart/

The live Baseline identifies itself as proposed requirements, version inferock-baseline-v1, September 23, 2026. It provides 19 quality requirements within 38 total requirements and no completed route assessment. Do not convert minimums or targets into achieved performance claims. A scope includes exact model revision, provider route, region, client and policy, configuration, workload and traffic envelope.

## Coverage map

The five article groups are editorial groupings, not additional official product categories.

- Usable delivery: Q01 broken output; Q02 unexpected truncation; Q12 tool-call validity; Q15 unexpected filtered omission; Q16 clean stream completion.
- Timeliness and recovery: Q08 availability; Q09 latency distribution and generation speed; Q17 retry amplification.
- Task behavior: Q10 unnecessary refusal; Q11 quality retained after changes; Q14 grounded factual accuracy.
- Operation integrity: Q03 billed empty output; Q04 OpenAI input-token recount; Q05 Anthropic input-token cross-check; Q06 request identity/duplicate charging; Q07 cache pricing anomaly; Q19 known price before routing.
- Approved route: Q13 security/governance signals; Q18 served-model identity.

## Numeric examples

- Q09 interactive non-reasoning profile: 2,000 input / 256 output tokens, same-region client, established verified session. p95 first usable token: minimum ceiling 2 seconds / target ceiling 1 second. p95 completion: minimum ceiling 13 seconds / target ceiling 7 seconds. Do not generalize to reasoning, long-context, fresh sessions, or arbitrary regions.
- Q17 minimum at most 1.020 upstream attempts per eligible logical operation; target at most 1.005. For 10,000 operations, these ratios represent 200 and 50 excess attempts. They do not specify the number of distinct retried operations.
- Q14 grounded accuracy target 98% on a fixed answerable source-grounded corpus with a declared rubric, not universal truthfulness. Unjustified abstentions count as misses.

## Limits carried into the draft

- Model errors, integration errors, and service-path errors need distinguishing; no claim that every output defect is caused by the API.
- Structural validity is separate from semantic correctness.
- Availability is evaluated before retries; valid safety refusals may count as available service while appropriateness is assessed separately.
- Client cancellations and deliberately undersized budgets are not provider-caused premature completions.
- Token differences need provider-specific component reconciliation; estimates alone do not prove overcharging.
- Matching a model label does not establish exact weights.
- Q13 does not certify confidential computing or end-to-end encryption. No privacy qualification is claimed for ordinary Watch connections.
- A missing required capability or missing evidence cannot become a passing N/A result.
- Watch visibility and proposed Baseline route qualification are distinct. No claim that every Baseline check is available for every routed call.
- Images are conceptual and do not display measured customer results.

## Supplied rewrite review

The live Baseline was checked again and was unchanged from the initial research. The rewrite preserves all 19 quality requirements, the proposed/not-achieved distinction, route scope, profile-specific latency requirements, correct retry arithmetic, and limits on factuality, identity and security claims. No factual correction was needed. The caption punctuation was adjusted to avoid an em dash; image positions were restored.
