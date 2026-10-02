# The Retry Worked. What Broke the First Time?

*How we use Inferock Watch to make failed inference calls easier to investigate—even when the application recovers.*

![Inferock title card: The Retry Worked. What Broke the First Time?](https://opiusai.github.io/articles/2026/10/002-the-retry-worked-what-broke-the-first-time/media/hero.png)

Imagine your application asks a model to summarize a document. The first attempt fails. Your retry logic kicks in, the second attempt returns an answer, and the user gets their summary.

The recovery worked. But when someone asks why the first attempt failed, your logs offer a timestamp, a generic exception, and the comforting knowledge that it worked eventually.

That leaves you with a decision to make and very little to base it on. Should you adjust a timeout? Change the retry policy? Investigate the provider? Leave everything alone?

“Probably transient” is doing an impressive amount of engineering here.

We built Inferock Watch to give teams more evidence for that investigation. Watch measures inference calls routed through your existing provider accounts and lets you inspect the recorded call and its linked findings. The problem we want to address is specific: recovering from a failed request should not leave you guessing about what happened to it.

Start with the two attempts in that document-summary example. They belong to one application task, but they are separate calls. If your application keeps only the final result, the successful response can obscure the failed attempt that preceded it.

That matters even when the user receives an answer. A recurring failure can add waiting time to otherwise successful tasks. It can also train a team to accept retries as normal before anyone has established what keeps triggering them. Increasing the retry count may improve completion rates, but it does not explain the underlying behavior.

The first step is to make each attempt findable. When routing a request through Inferock, supply a unique `x-request-id` and record it in your application logs. If the application retries, give that attempt its own request ID and associate both IDs with the same application task.

For example, your application might record:

```text
Task: document-summary-1842
  Attempt 1 → request ID: summary-1842-a1 → application recorded failure
  Attempt 2 → request ID: summary-1842-a2 → application accepted response
```

Your application keeps the task-to-attempt association; Inferock records each routed call under its request ID. Together, those records let you inspect the failed attempt and its retry without mistaking the final answer for the full history of the task.

With Watch, you connect your provider account and send calls through the Inferock gateway using an Inferock key. Successful calls preserve the upstream HTTP status and provider response content. Your application receives the model response, while measurement happens alongside the request flow. The [first-call guide](https://inferock.ai/docs/first-call/) covers the request ID and gateway behavior.

Now return to the failed attempt. In the development app’s Calls view, you can look it up using its request ID. The documented record includes provider and model, attempt information, failure class, token usage, cost, timing, and linked findings. Redacted payload evidence is available where present. The Proof view provides finding evidence and proof packets. These views are described in [Receipts + ledger](https://inferock.ai/docs/receipts-ledger/).

You can compare that record with what your application observed. Did your client report a timeout? What timing did the gateway record? Is there a failure classification or a linked finding to examine? What evidence is available, and what is still missing?

Those questions produce a more useful investigation than sending the same prompt again and hoping the failure is feeling cooperative.

They also help keep the diagnosis honest. Suppose your application rejected a response because a required field was missing. That application validation result belongs in your logs. A gateway record alone cannot establish every requirement your product has. You need both the call evidence and the application’s reason for rejecting the answer before deciding what to change.

There is another boundary worth checking: whether the request reached a provider at all. Inferock applies admission limits after authentication and before calling the provider. If a request is rejected at that stage, it does not create a provider-loss measurement. For example, a gateway `429` caused by an account limit needs to be investigated using its reason and reset guidance. Blaming the model would send you in the wrong direction. The [Limits guide](https://inferock.ai/docs/limits/) documents that behavior.

None of this makes a retry wrong. Recovery is useful. We want the user to get their summary. We also want the engineer investigating the incident to have enough evidence to choose a sensible next step.

That might mean fixing request construction, changing how the application handles a response, respecting a limit reset, or taking a documented provider failure to support. Sometimes the available evidence will still be incomplete. An unresolved question is a better starting point than a confident diagnosis built around the last successful attempt.

This is where transparency becomes useful in practice. You can inspect the recorded call, follow a finding to its evidence, and compare it with your own application logs. That gives the team something concrete to review when deciding whether a recurring failure needs a code change or further investigation.

If this sounds familiar, start with [Inferock Watch setup](https://inferock.ai/docs/account-byok/) and add request IDs to the calls you route through it. The next time a retry succeeds, you should be able to investigate the attempt that made it necessary.
