# You Picked a State-of-the-Art Model. The API Is Making It Hard to Tell.

*The model can do the job. The service delivering it has a job to do, too.*

![Inferock article header: You Picked a State-of-the-Art Model. The API Is Making It Hard to Tell.](https://opiusai.github.io/articles/2026/10/005-you-picked-a-state-of-the-art-model-the-api-is-making-it-hard-to-tell/media/hero.png)

You compare models, run your evaluation set, and find one that gets it. It handles the task, follows your instructions, and gives you answers your application can actually use. Then you put it behind an API. Some requests drag. Some answers stop just before the useful part. A retry saves the day, but the records make it look like the day never needed saving. Then something changes on the serving side, and the model with the same reassuring name starts acting differently.

Your users don't care how well it did on your benchmark last Tuesday. They care about the response they're staring at. Hard to blame them.

Choosing a capable model matters. Getting that capability to users consistently also depends on who's serving it, with what configuration, limits, routing decisions, and behavior under your workload. That doesn't make the API responsible for every bad answer. Models get things wrong. Prompts get things wrong. Integrations find remarkably creative ways to get things wrong. The point is to measure enough to tell those failures apart, instead of throwing them all into a bucket labelled “AI quality.”

At Inferock, our [Baseline](https://inferock.ai/baseline/) defines 19 quality requirements for evaluating model routes. They're part of a broader qualification framework. Here, we're looking specifically at the quality checks. One distinction matters before we get into them: these are **proposed** requirements, not published performance results. The current Baseline contains no completed route assessment. Minimums say what a route would need to meet to qualify; targets say what we're aiming for. Neither means a route has passed. So, before calling an inference service good, here's what we'd want to know.

## Did we get an answer the application can use?

Say you're building a document assistant. It reads a policy, extracts the eligibility rules, and returns structured data so your application can display a comparison. The model might understand the document perfectly. Your application still needs the whole result, in the format it asked for.

Five requirements check different ways that handoff can fail:

- **Broken output (Q01):** does a completed response satisfy its declared, supported schema?
- **Unexpected truncation (Q02):** did generation stop early even though the output budget was sufficient?
- **Tool-call validity (Q12):** are the tool names and arguments structurally valid under the supported contract?
- **Unexpected filtered omission (Q15):** was benign output unexpectedly removed, where the provider exposes filter evidence?
- **Clean stream completion (Q16):** did a started stream end with the terminal or finish evidence its protocol requires?

These aren't five names for the same problem. They need different fixes. A bigger output budget won't fix an invalid tool name. A stream that finishes properly can still deliver an object that fails your schema. And if the user deliberately cancels a request, that shouldn't show up as provider-caused truncation.

For the document assistant, a lovely paragraph isn't a substitute for the structured object you requested. On the other hand, an object that parses perfectly can still contain the wrong eligibility rules. “Valid structure” and “correct answer” are two separate checks.

The [quality definitions](https://inferock.ai/baseline/#inferock-baseline-quality) spell out those boundaries. They also make sure missing filter evidence doesn't get quietly interpreted as proof that nothing was omitted. “We didn't observe a problem” is less comforting when nobody could observe it in the first place.

## Did it arrive before the user tried again?

The extraction can be correct and still take long enough that the customer hits submit a second time. Your model evaluation might call that a success. Your customer probably has a different word for it. Availability (Q08), latency distribution and generation speed (Q09), and retry amplification (Q17) cover this part of the experience.

Availability means eligible operations get a complete, protocol-valid response within their deadline, measured before retries. “The endpoint was reachable” doesn't quite cut it. Time-based uptime and request success need to stay separate. Individual routes need to stay visible, too. One healthy provider shouldn't get to hide another provider's failures in an average.

For latency, a tokens-per-second number isn't enough. Measure when the first usable token arrives, the gaps between output tokens, and how long the full response takes. Look at the distributions, including the tail where some unlucky customer is sitting. A quick opening sentence followed by a long stall is still a long stall. The greeting doesn't get to carry the entire performance claim.

The Baseline's interactive profile shows how specific these measurements need to be: non-reasoning traffic, 2,000 input tokens, 256 output tokens, a same-region client, and an established verified session. For that profile, the proposed p95 time-to-first-token limit is two seconds at the minimum, with a one-second target. Full completion has a separate p95 limit: 13 seconds at the minimum, seven seconds at the target.

Those numbers belong to that profile. Long-context and reasoning workloads have different requirements. Fresh-session setup gets measured separately. Pulling out the fastest number and calling the whole service “fast” leaves behind most of the information that made the number useful.

Retries need their own accounting as well. Q17 measures total upstream attempts per logical operation, including failed attempts, and reports eventual completion separately. Its proposed minimum is no more than 1.020 attempts per operation; the target is 1.005. Across 10,000 logical operations, that allows 200 or 50 extra attempts, respectively. The ratios don't tell you where those attempts went, so keep the underlying records.

A retry can rescue the user's task. It doesn't retroactively make the first attempt successful. And replaying a tool with side effects is not an acceptable way to give your completion chart a little lift.

![Conceptual illustration of output, latency, behavior, integrity, and identity checks along an inference route.](https://opiusai.github.io/articles/2026/10/005-you-picked-a-state-of-the-art-model-the-api-is-making-it-hard-to-tell/media/quality-route.png)

*Conceptual illustration of the checks along a route. This is not a product screenshot or a completed route assessment.*

## Does it still work when something changes?

The document assistant passed your evaluation. Then the serving configuration changed. Does it still extract the right rules? Three requirements deal with this: unnecessary refusal (Q10), quality retained after changes (Q11), and grounded factual accuracy (Q14).

A valid safety refusal can count as an available service response. Whether that refusal was appropriate for the task is a different question. To check unnecessary refusals, you need prompts labelled benign and supported, matched to the task, language, and policy. Removing legitimate safety refusals to improve your completion percentage would certainly move the number. Just not in a direction worth celebrating.

To evaluate a change, you need a fixed reference. Use identical versioned tasks and sampling settings, and look at uncertainty alongside the scores. If a serving change lowers quality, making the lower score your new reference doesn't show that quality was retained. It shows that the goalposts are surprisingly portable.

Factual accuracy needs a clear scope, too. “Does this model tell the truth?” is too broad to be useful here. For the document assistant, you can use a fixed, answerable corpus, source material, and a declared rubric. That gives you a consistent way to score unsupported claims, missed answers, and unjustified abstentions. The Baseline's proposed 98% accuracy target applies to that kind of bounded evaluation. It is not a claim that a route is 98% truthful across arbitrary prompts or every model.

What a developer needs to know is whether this route still meets this workflow's requirements, on an evaluation someone else could understand and repeat. Without that context, a percentage is a decent badge and a lousy debugging tool.

## Do the records agree about what happened?

The service also needs to keep trustworthy records. That means checking billed empty output (Q03), OpenAI token recount (Q04), Anthropic token cross-check (Q05), request identity and duplicate charging (Q06), cache pricing anomalies (Q07), and known price before routing (Q19). You need to know which operation ran, what it delivered, and whether the records line up. Otherwise, your route comparison starts with a debate over whose spreadsheet to believe.

There are a few easy traps here:

- A valid tool payload can be usable output even if the response contains no prose.
- Legitimate retries can share an idempotency key.
- A cache miss charged at its documented rate isn't automatically a cache pricing anomaly.

Provider-specific token comparisons need comparable components, too. Message framing, reasoning, multimodal input, and documented system additions can all affect what you can reconcile. An unexplained difference deserves investigation. A counting estimate, on its own, doesn't prove overcharging.

The known-price requirement is about having explicit terms before a billable routing decision. If the price is missing, record missing evidence. Don't helpfully turn it into a zero and congratulate yourself on the savings.

If the document assistant takes three attempts, we should be able to identify all three and reconcile what came back. The next investigation shouldn't start with everyone trying to remember which request happened when.

## Did we get the route we approved?

The remaining two requirements are security and governance signals (Q13) and served-model identity (Q18).

If you evaluated a particular model revision and configuration, silently serving a different one changes the basis of your decision. Route selection needs to respect the approved contract. A matching model label is useful evidence. It doesn't independently prove the exact weights that ran.

Security and governance checks need the same care with scope. Q13 covers confirmed critical exposures and required policy evidence within an authorized, bounded evaluation. It does not certify confidential computing or end-to-end encryption. The Baseline has a separate privacy category for its own requirements.

These checks belong in a quality discussion because customers need to know what service they actually received. A fast, fluent answer doesn't make an unauthorized model substitution or a critical exposure acceptable. Some requirements are gates. You don't get to average them away because the other charts are having a good day.

## Measure the service your application actually uses

Those five questions cover all 19 quality requirements. In each case, we're assessing the route, not just the model name attached to it. That assessment needs a defined scope: model revision, provider route, region, client and policy, configuration, workload, and traffic envelope. Change the scope, and you need to check whether the old evidence still applies. An interactive chat result doesn't establish long-context performance. A quiet test doesn't tell you how an overloaded deployment behaves.

The [Baseline's qualification rules](https://inferock.ai/baseline/#inferock-baseline-overview) also distinguish a genuinely optional check from a required capability the route doesn't support. Missing evidence isn't a pass. And a mandatory feature your workflow needs doesn't become “not applicable” just because that would make qualification easier.

You don't have to memorize 19 identifiers before shipping. You do have to decide what successful inference means for your application, then keep enough evidence to check whether you're getting it. For the document assistant, that means complete extraction, the right structure, grounded answers, an acceptable wait, and the approved serving configuration. Choosing a strong model gets you off to a good start. It doesn't finish the job.

## Where Inferock fits

At [Inferock](https://inferock.ai/), we're building accountable inference around that distinction: access to models, visibility into what happened, and clear limits on what the evidence actually proves.

[Inferock Watch](https://inferock.ai/watch/) lets you keep your existing provider accounts while gaining visibility into the quality, latency, and usage of calls routed through Inferock. Our [inference workflow](https://inferock.ai/how-it-works/) connects route and response evidence with checks, using active probes where a reference is needed. That workflow and the Baseline's proposed qualification requirements are related. They are not interchangeable proof that every requirement has been met.

To see it with your own calls, start with the [Inferock Watch quickstart](https://inferock.ai/docs/quickstart/). Use the Baseline to ask better questions about the routes your application depends on.

You already spent time choosing a capable model. It would be nice if your users could tell.
