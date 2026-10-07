# X thread adaptation

Attach `../media/hero.png` to post 1 and `../media/evidence-trail.png` to post 5. Post text is inside each block below. This is a condensed adaptation, not the full article.

## Post 1

```text
1/10
Your LLM dashboard says "Success."

The provider returned 200. The JSON parsed. Your tool still can't run because account_id is missing.

Congratulations. The braces match. The function would still like its arguments.
```

## Post 2

```text
2/10
Valid JSON and valid tool arguments are different checks.

If account_id is required by the declared schema, an object without it fails that contract.

No debate about whether the response seemed helpful. No adjudication by vibes.
```

## Post 3

```text
3/10
The requirement has to be declared. Your app also has to enforce it before executing the tool.

A failure record helps explain what happened. It doesn't replace validation.

Reject invalid arguments before executing the tool.
```

## Post 4

```text
4/10
With Inferock Watch, you connect your existing provider key and authenticate gateway requests with an Inferock key.

Give each new request a unique x-request-id. That connects the application event to the measured call, without timestamp guesswork.
```

## Post 5

```text
5/10
Find that request in Calls, then inspect finding evidence in Proof.

For our example: did parsing succeed? Was the declared schema available? Which required field was missing?

The illustration shows this relationship, not a measured customer call.
```

## Post 6

```text
6/10
Missing account_id supports a structural failure finding when the schema and response evidence support it.

It doesn't explain the provider's internals. It also doesn't prove that an ID which passes the schema belongs to the right customer.

Business checks still matter.
```

## Post 7

```text
7/10
Different claims need different evidence.

A missing required field needs the contract and response.
A latency complaint needs a service expectation.
A factuality claim needs ground truth.

One dashboard doesn't make them equally certain.
```

## Post 8

```text
8/10
Did the request reach the model at all?

Inferock's admission controls run after authentication, before the provider call. A rejected payload or exhausted quota doesn't create a provider loss measurement.

Blaming the model here means debugging a response that never existed.
```

## Post 9

```text
9/10
Calls: inspect the request.
Proof: examine finding evidence.
Home: read the period summary.

A measured failure doesn't automatically qualify for failure credit. Eligibility follows the credit promise and your account's terms.

Keep the finding and remedy status separate.
```

## Post 10

```text
10/10
At Inferock, we want the outcome to be inspectable, including what the evidence does and doesn't prove.

The green badge can stay. We'd just like it to come with an explanation.

Start with one request:
https://inferock.ai/docs/quickstart/
```
