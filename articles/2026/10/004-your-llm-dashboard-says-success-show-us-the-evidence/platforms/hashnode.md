*Following one request through Inferock, from a provider response to a finding an engineer can actually inspect.*

Your agent needs to look up a customer’s account. It asks the model to call `lookup_account`, passing the account ID along with the other arguments.

The provider returns HTTP 200. The response arrives. The JSON parses.

Your dashboard logs another successful request. Meanwhile, your tool gets this:

```json
{
  "region": "eu",
  "include_history": false
}
```

No `account_id`.

Congratulations. The braces match. The function would still like its arguments.

This is an illustrative example, but the distinction matters: the model API completed the request. Your application got something it couldn’t use. Both can be true, even if your dashboard only has room for one green badge.

At Inferock, we want you to be able to follow that gap. Which request produced the response? What was it supposed to return? What actually came back? Which check failed?

“The model did something weird” is a perfectly reasonable opening line for a debugging session. It’s a lousy place to end one.

## Write down the requirement

Here’s the tool’s argument schema for our example:

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

The returned arguments are valid JSON. They’re not valid against this schema.

That gives us something specific to point at: `account_id` is required, and it’s missing. No debate about whether the response seemed helpful. No vibes-based adjudication.

But the requirement has to be declared before the check means anything. If your application needs an account ID and never says so, an observer can’t reliably discover that expectation by staring harder at `region` and `include_history`.

Your application also needs to enforce the contract. Reject invalid arguments before executing the tool. A failure record helps you investigate what happened; it doesn’t replace validation at the execution boundary.

Observability is useful. It is not a permission slip to run broken inputs.

## Give the request a trail

We’ll use Inferock Watch for this walkthrough. You connect your existing provider key, then authenticate gateway requests with a separate Inferock key. Your provider account still serves the inference.

Two keys, two jobs:

- The provider key goes in provider setup.
- The Inferock key goes in your application’s gateway authentication.

Our [account setup guide](https://inferock.ai/docs/account-byok/) covers that separation and the key replacement workflow. Mixing them up won’t make the setup simpler. It will just give you a different problem to debug.

The current guides cover the development gateway. The documented Chat Completions example uses these headers:

```text
Authorization: Bearer <your Inferock key>
x-governance-provider: openai
x-request-id: account-lookup-001
```

Those headers handle authentication, routing, and request identity. They are not a complete tool-call request. Your body still needs the model, messages, and tool definition.

Use the gateway base URL from your account settings, and give each new request a unique ID. That ID is how you connect an application event to the measured call later, rather than squinting at timestamps and hoping for the best. The [first-call guide](https://inferock.ai/docs/first-call/) has complete curl, Python, and Node.js examples.

For successful calls, the gateway preserves the upstream HTTP status and provider response content. Your application gets the provider’s answer, not an Inferock measurement envelope.

So yes, our broken account lookup can still come back through the gateway with HTTP 200. We haven’t redefined the status code. We’re adding evidence you can use to judge the output separately.

## Find the call and evidence

After the provider result, the gateway emits a measurement event. Open Calls and find `account-lookup-001`.

Depending on what’s available, the [call details](https://inferock.ai/docs/receipts-ledger/) can include the provider, model, request ID, attempt and failure class, timing, usage, linked findings, and redacted payload evidence.

For this lookup, you want answers to four questions:

- Is this the request our application rejected?
- Did the check have access to the declared tool schema?
- What arguments did the model return?
- Did JSON parsing succeed, and which schema requirement failed?

Keep those answers attached to the same request. An application log saying “validation failed” and a provider response saying “200” aren’t much help if you can’t establish that they’re talking about the same call.

The docs point you to Proof for finding evidence and proof packets. That’s where you move from “we counted a failure” to “here’s what supports the finding.”

![Illustrative evidence trail: a required account_id field in the contract, its absence in the response, and the corresponding finding.](https://opiusai.github.io/articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/media/evidence-trail.png)

*Illustration only: the declared contract requires `account_id`, the response omits it, and the finding connects the two. This is not a product screenshot or a measured customer call.*

The explanation should be refreshingly boring: the arguments parsed, the schema required `account_id`, and the returned object didn’t contain it.

Another engineer can inspect that reasoning. They can challenge it, too. If the wrong schema was supplied, the finding needs correcting. Transparency doesn’t get to stop being transparent when someone spots a mistake.

## Know what the failure proves

The missing field supports a structural failure finding. It doesn’t explain why the model omitted it, prove that another prompt would have prevented it, or tell us what happened inside the provider’s infrastructure.

And a response with every required field isn’t automatically correct. The model could return the wrong customer’s account ID and pass this schema just fine. Your application may still need authorization checks, database verification, or other business rules before using it.

“All the fields are here” is not the same as “please proceed with confidence.”

Inferock’s [measurement methodology](https://inferock.ai/methodology/) separates objective failures, signals that need thresholds, and flags that need review. A missing required argument belongs in the first category when the schema and response evidence support it.

Other claims need different evidence. A latency complaint needs a service expectation to compare against. A factuality claim needs ground truth. Putting them on the same dashboard doesn’t magically give them the same certainty.

There’s another boundary to check: did the request reach the model at all?

Inferock’s admission controls run after authentication and before the provider call. A rejected payload or exhausted quota doesn’t create a provider-loss measurement. The [limits guide](https://inferock.ai/docs/limits/) explains the error reasons and recovery guidance.

That matters during an incident. A request rejected before inference and a completed provider response with invalid arguments are different failures. They need different fixes.

In our account lookup, we have a provider result and an output contract violation, so we can investigate the returned arguments. If admission had rejected the request instead, blaming the model would send us off debugging a response that never existed.

One generic error counter tends to blur all of this together. Very efficient at telling you something happened. Less impressive at telling you what.

## Make the summary earn it

Calls lets you inspect the individual request. Proof holds the finding evidence. Home summarizes the reporting period.

The [receipt guide](https://inferock.ai/docs/receipts-ledger/) documents states such as “No data yet,” “Partial data,” and “Verified,” along with the standard version and receipt generation time. Those details help you read a summary without pretending every number on the screen is equally established.

For engineers, the useful part is the path back to the request. An aggregate can tell you there’s a problem. The evidence underneath helps you decide what to change.

A measured failure also doesn’t automatically qualify for credits on failure. Eligibility is a separate decision under the applicable [credit terms](https://inferock.ai/docs/credit-promise/). The technical finding and the remedy status need to stay separate, however tempting it is to turn them into one convenient badge.

Back to our account lookup.

We started with a green status and a tool that couldn’t run. Now we have a request ID connecting the application event to the call, a declared requirement, a response that breaks it, and an explanation another engineer can inspect.

That’s enough to start doing useful work: check the tool definition and request construction, examine affected calls, and verify whether a change fixes the same failure.

We still have to do the engineering. Sadly, the dashboard has not volunteered.

This is what we mean by accountable inference at Inferock: route the call, attach observable evidence, and make the outcome inspectable, including the limits of what that evidence proves.

To follow the same path with your own provider account, start with the [Inferock Watch quickstart](https://inferock.ai/docs/quickstart/) and find your first request in Calls.

The green badge can stay. We’d just like it to come with an explanation.
