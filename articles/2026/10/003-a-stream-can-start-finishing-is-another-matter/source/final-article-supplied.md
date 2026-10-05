
# A Stream (The LLM Kind, Not the Water Kind) Can Start. Finishing Is Another Matter.

The first chunk proves an LLM response has begun. It does not prove the answer finished, and neither does it prove that your application can use it.

Imagine a support assistant helping a customer reconnect an integration. The first words arrive quickly: “Let’s get this working again.” Then come numbered steps. Check the connection. Open the integration settings. Reauthorize the account.

Halfway through the next instruction, the answer stops:

> “Before you reconnect, make sure you…”

Make sure you what?

The UI has already displayed useful-looking text. In this example, the request began with HTTP 200. The customer sees an answer-shaped object, while the application has no confirmed completion.

Now the app must decide what it received: an answer, an interrupted answer, or something that failed before becoming usable. That decision needs evidence. A spinner disappearing is a surprisingly weak definition of success.

## Streaming is not completion

Streaming means the API sends pieces of an LLM response incrementally, while generation continues. With HTTP streaming over server-sent events, the client can process those events and display text without waiting for the entire response. That improves perceived responsiveness: the customer starts reading instead of staring at an empty chat bubble. It does not make the early pieces a completion signal.[[developers.openai](https://developers.openai.com/api/docs/guides/streaming-responses?api-mode=responses)]

For our support assistant, “Let’s get this working again” is evidence of progress. It says nothing about whether the final instruction will arrive. Keep two concepts separate: content becoming available and the response reaching a confirmed terminal state.

Also distinguish text deltas from other events. A stream may carry lifecycle events, tool-argument fragments, usage information, pings, and errors. A parser that only extracts displayable text can miss the evidence needed to decide whether the request succeeded. Claude’s streaming protocol explicitly includes these different event types.[[platform.claude](https://platform.claude.com/docs/en/build-with-claude/streaming)]

The half-finished support answer could have several explanations.

-   A connection interruption. A read error, timeout, or unexpected end before the required terminal signal leaves completion unconfirmed. Preserve the fragment and investigate the transport path; missing evidence alone does not identify which component caused the interruption.
-   An error inside an established stream. Claude, for example, can emit an `error` event containing `overloaded_error`. Your handler must inspect stream events, not just the initial HTTP status.[[platform.claude](https://platform.claude.com/docs/en/build-with-claude/streaming)]
-   An output limit. Generation can stop because it exhausted its allowed output budget. Claude reports `max_tokens`; its documentation recommends raising the limit or continuing the response. Retrying unchanged does not address that limit.[[platform.claude](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)]

These cases need different fixes, not one generic “LLM failed” bucket.

Provider protocols also express completion differently. OpenAI’s Responses API exposes `response.completed` and `response.incomplete` events. Claude sends a final `message_stop`, with the stop reason supplied in `message_delta`. A terminal event therefore needs interpretation: Claude can finish its stream while reporting that generation hit `max_tokens`. The protocol ended; the support instructions may not have.[[platform.claude](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)][[developers.openai](https://developers.openai.com/api/reference/resources/responses/streaming-events)]

## Three tests for finished

“Finished” hides three separate questions:

1.  Did the transport end cleanly?
2.  Did the provider report an acceptable generation outcome?
3.  Did the accumulated content satisfy the application’s contract?

Treat these as separate checks, not synonyms. Inferock’s methodology likewise considers stream completion, finish reason, delivered content, and structural validation when assessing broken output.[[inferock](https://inferock.ai/methodology/)]

A clean connection close answers only the transport question. The provider’s terminal event and stop information answer the generation question. The application still owns the usability question.

For the support assistant, a declared contract might require a troubleshooting result containing instructions and a final verification step. If the model returns structured data, a missing closing JSON brace makes failure obvious. But a closing brace only proves syntactic closure: the object could still omit a required field.

Tool arguments make the distinction sharper. Claude streams tool inputs as partial JSON strings, which must be accumulated and parsed. Parsing successfully still does not establish that the arguments satisfy your tool’s schema.[[platform.claude](https://platform.claude.com/docs/en/build-with-claude/streaming)][[inferock](https://inferock.ai/methodology/)]

For free-form support prose, completeness is harder to prove. Define checks your application can actually enforce; do not pretend a period at the end establishes that every necessary instruction arrived.

The accidental promotion happens when rendering and success share the same handler:

```
on_text_delta: append_to_ui(delta)
on_connection_close: mark_answer_complete()
```

That second line assumes what it needs to establish.

Use an explicit partial state instead. Our interrupted assistant answer can remain visible, labelled “Response interrupted,” without becoming the final answer in conversation history or a downstream workflow. Rendering is provisional; committing is a separate decision.

This is not an argument against streaming. It is an argument against letting the UI’s enthusiasm write your success criteria. Show progress promptly. Promote it deliberately.

## Keep the useful evidence

When the support answer stops, “it cut off” is a symptom report. A useful call record preserves enough evidence to distinguish possible failure classes without inventing a cause. Inferock’s measurement approach starts with observable request, response, timing, usage, and outcome evidence.[[inferock](https://inferock.ai/methodology/)]

For your application’s own record, keep:

-   Request identity: an application request ID and any available provider request ID.
-   Execution path: provider, API route, requested model, and attempt identity.
-   Timing: request start, first content chunk, last content chunk, and terminal event or error time.
-   Delivered content: what was accumulated at the layer you observed, under appropriate redaction and retention rules.
-   Provider outcome: terminal event, finish or stop reason, and available incomplete-response details.
-   Failure evidence: stream error, transport exception, timeout, or observed cancellation.
-   Application verdict: validation passed, failed, or never ran, with the failed check recorded.

Call these proposed application fields, not a promise that every gateway exposes all of them. Inferock documents streaming milestones “when available” and explicitly notes that provider fields differ.[[inferock](https://inferock.ai/methodology/)]

Keep client cancellation separate from upstream failure when the evidence supports that distinction. If the customer presses Stop, record it. If your server reaches its own deadline, record that too. Otherwise, “provider interrupted” can become a convenient label for your own abort.

Finally, record where observation occurred. Gateway receipt is not proof of browser delivery. That boundary matters when comparing the call record with what the customer actually saw.

## Where Inferock Watch fits

Inferock’s gateway documentation states that successful streaming and non-streaming calls preserve the upstream HTTP status and provider response content. The gateway does not replace the answer with an Inferock-specific measurement envelope.[[inferock](https://inferock.ai/docs/first-call/)]

Its first-call workflow has you supply a request ID, then find the corresponding measured call in Calls. Call details can include provider, model, request ID, attempt and failure class, tokens, cost, timing, linked findings, and redacted payload evidence when those fields are available.[[inferock](https://inferock.ai/docs/first-call/)][[inferock](https://inferock.ai/docs/receipts-ledger/)]

For our interrupted support answer, that gives engineers a concrete starting point: locate the request, inspect the recorded outcome, and compare it with the application’s interrupted state.

Inferock’s broken-output methodology considers delivered content, finish reason, stream completion, output usage, JSON parsing, and schema validation. It describes checks for malformed, truncated, empty, or contract-invalid output.[[inferock](https://inferock.ai/methodology/)]

The boundary matters. A call record helps investigate an interruption; it does not expose every internal provider cause or discover every requirement your support workflow forgot to declare. Inferock explicitly limits structural checks: they do not establish factual correctness, and tool-argument validation needs a declared schema or objective contract.[[inferock](https://inferock.ai/methodology/)]

Useful evidence, not omniscience. That is a better engineering promise anyway.

## Change the success rule

Make the application’s rule explicit: chunks are provisional; success requires an acceptable provider outcome and application validation. That follows the distinction between provider stop information and checks against a declared response contract.[[platform.claude](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)][[inferock](https://inferock.ai/methodology/)]

A practical sequence is:

1.  Display incoming text with an in-progress state.
2.  Accumulate content while inspecting lifecycle and error events.
3.  Require the expected terminal signal and interpret its outcome.
4.  Validate the assembled result before committing success.
5.  If either check fails, preserve the partial state and request ID.

Back in the support chat, “Before you reconnect, make sure you…” should not quietly become a completed answer. Keep it visible as an interruption, with a recovery path—not as finished guidance.

The assistant started helping. Your application still has to establish whether it finished.