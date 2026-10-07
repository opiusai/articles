# Your LLM Dashboard Says “Success.” Show Us the Evidence.

*Following one request through Inferock, from a provider response to a finding an engineer can inspect.*

![Inferock article header: Your LLM Dashboard Says “Success.” Show Us the Evidence.](https://opiusai.github.io/articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/media/hero.png)

Your agent needs to look up a customer's account. It asks the model to call `lookup_account`, with arguments that include the account ID.

The provider returns HTTP 200. The response arrives. The JSON parses.

Your dashboard gets another successful request. Your tool gets this:

```json
{
  "region": "eu",
  "include_history": false
}
```

No `account_id`.

Congratulations, the braces match. Unfortunately, the function still needs its arguments.

This is an illustrative example, but it gives us a useful distinction: the model API completed a request, while the application received something it couldn't use.

At Inferock, we want you to be able to inspect that distinction. Which request produced this result? What did it require? What came back? Which check failed?

“The model did something weird” is a starting point for debugging. We'd prefer to get a little further than that.

## First, make the requirement explicit

For this example, the tool's argument schema looks like this:

```json
{
  "type": "object",
  "properties": {
    "account_id": { "type": "string" },
    "region": { "type": "string" },
    "include_history": { "type": "boolean" }
  },
  "required": ["account_id", "region"]
}
```

The returned arguments are valid JSON, but they violate that schema. We can point to the missing required field. We don't need to debate whether the response felt helpful.

That requirement needs to exist before the check can mean anything. If your application expects an account ID but never declares it, an observer can't reliably reconstruct that expectation from two innocent-looking fields.

The same applies to your application code. Reject the invalid arguments before executing the tool. A record of the failure helps you investigate it; your execution boundary still needs to enforce the contract.

## Put the request somewhere you can follow it

We'll use Inferock Watch for this walkthrough. You connect your existing provider key, then use a separate Inferock key to authenticate requests through the gateway. Your provider account continues to serve the inference.

There are two credentials here because they do different jobs. The provider key belongs in provider setup. The Inferock key belongs in your application's gateway authentication. Our [account setup guide](https://inferock.ai/docs/account-byok/) explains that separation and the key replacement workflow.

The current setup guides cover the development gateway. The documented Chat Completions example uses these headers:

```text
Authorization: Bearer <your Inferock key>
x-governance-provider: openai
x-request-id: account-lookup-001
```

These are the routing and identity headers, not a complete tool-call request. Your request body still contains the model, messages, and tool definition.

Use the gateway base URL from your account settings. Give each new request a unique ID so you can connect the application event to the measured call later. The [first-call guide](https://inferock.ai/docs/first-call/) includes complete curl, Python, and Node.js examples.

For successful calls, the gateway preserves the upstream HTTP status and provider response content. Your application receives the provider's answer rather than an Inferock measurement envelope.

That means our example can still return HTTP 200 through the gateway. We haven't changed what that status means. We're adding the evidence needed to assess the output separately.

## Find the call, then inspect the finding

After the provider result, the gateway emits a measurement event. Open **Calls** and match `account-lookup-001`.

The [call details](https://inferock.ai/docs/receipts-ledger/) can include provider, model, request ID, attempt and failure class, timing, usage, linked findings, and redacted payload evidence when those fields are available.

For our example, the questions are specific:

- Does this record belong to the request our application rejected?
- Was the declared tool schema available to the check?
- What arguments did the model emit?
- Did parsing succeed, and which schema requirement failed?

Keep those questions together. An application log saying “validation failed” and an unrelated provider response saying “200” don't explain much until you can connect them to the same request.

The docs direct you to **Proof** for finding evidence and proof packets. That's where the investigation moves beyond counting failed calls and into examining what supports a finding.

![Illustrative evidence trail: a required account_id field in the contract, its absence in the response, and the corresponding finding.](https://opiusai.github.io/articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/media/evidence-trail.png)

*Illustration only. This shows the relationship between a contract, a response, and a finding; it is not a product screenshot or a measured customer call.*

A useful explanation of this failure is straightforward: the arguments parsed, the declared schema required `account_id`, and the returned object omitted it.

Someone else can inspect that reasoning. They can also challenge it. If the wrong schema was supplied, the finding needs correction. Transparency has to allow that too.

## A failed check has a boundary

The missing field supports a structural failure finding. It doesn't tell us why the model omitted it, whether a different prompt would have prevented it, or what happened inside the provider's infrastructure.

It also doesn't prove that an object containing every required field is correct. The model could supply the wrong customer's account ID and pass this schema. Your application may need authorization checks, database verification, or other business rules before using it.

Inferock's [measurement methodology](https://inferock.ai/methodology/) distinguishes objective failures, signals that need thresholds, and flags that need review. Our missing required argument belongs in the first category when the schema and response evidence support it.

A latency complaint needs a service expectation to compare against. A factuality claim needs ground truth. Those are different questions with different evidence requirements.

We shouldn't give them the same confidence just because they fit on the same dashboard.

## Record where the failure happened

There's another boundary worth checking: did the request reach a model at all?

Inferock's admission controls run after authentication and before the provider call. A rejected payload or exhausted quota doesn't create a provider-loss measurement. The [limits guide](https://inferock.ai/docs/limits/) documents the error reasons and recovery guidance.

That distinction matters during an incident. A request rejected before inference and a completed provider response with invalid arguments need different fixes.

For our account lookup, we have a provider result and an output contract violation. We can investigate the returned arguments. If the request had been rejected at admission instead, blaming the model would send us down the wrong path.

One generic error counter tends to hide this. It is very efficient at telling you that something happened.

## Keep the summary connected to the evidence

Calls helps inspect the individual request. Proof holds finding evidence. Home summarizes the reporting period.

The [receipt guide](https://inferock.ai/docs/receipts-ledger/) documents states such as **No data yet**, **Partial data**, and **Verified**, along with the standard version and the time the receipt was generated. Those details give you context for reading a summary rather than treating every displayed number as equally established.

For engineering, the value is the path back to the failed request. An aggregate can show that a problem exists. The underlying evidence helps you decide what to change.

And a measured failure doesn't automatically establish eligibility for **credits on failure**. That is a separate decision under the applicable [credit terms](https://inferock.ai/docs/credit-promise/). Keep the technical finding and the remedy status distinct.

## Back to the account lookup

We started with a green status and a tool that couldn't run.

Now we have a request ID connecting the application event to the call, a declared requirement, a response that violates it, and an explanation another engineer can inspect.

That gives the team something concrete to work with: check the tool definition and request construction, examine affected calls, and verify whether a change addresses the same failure. We still have to do the engineering. We have a better starting point for it.

This is what we mean by accountable inference at Inferock. We route the call and attach observable evidence so you can examine its outcome, including the limits of the conclusion.

If you want to follow the same path with your own provider account, start with the [Inferock Watch quickstart](https://inferock.ai/docs/quickstart/) and find your first request in Calls.

The green badge can stay. We'd just like it to come with an explanation.
