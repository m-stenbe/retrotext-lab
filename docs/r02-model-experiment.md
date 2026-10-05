# R02 model experiment: usage and work audit

## Completed-run usage update

The logs now contain all task completion events. The confirmed R02 implementation
ran **73m 50s**, excluding interrupted preconfirmation setup and subsequent
conversation. The Astra manager plus two Sol workers and one Luna worker used
**1,231 requests**, **2,004,808 uncached input tokens**, **133,447,040 cached input
tokens**, and **457,086 output tokens**. The earlier snapshot below is retained
as historical evidence; the machine-readable audit now contains completed tasks.

Workers alone: 977 requests, 1,689,966 uncached input, 104,909,440 cached input,
and 377,576 output tokens. Manager alone: 254 requests, 314,842 uncached input,
28,537,600 cached input and 79,510 output tokens. These are usage counters, not
billed charges. Compared with R01, total team requests increased 175%, uncached
input 122%, cached input 130%, output 158%, and elapsed wall time 74%. Different
scope and substantial review/fitting assistance prevent causal model claims.

This is a **snapshot at 17:05:24 CEST on 23 September 2026** (15:05:24 UTC),
while the R02 manager and QA worker were still active. The confirmed R02 period
began at 15:53:15 CEST. Its 72m 09s elapsed wall time is therefore a
right-censored runtime, **not a completed release time**. A 266-record,
44-scene candidate had been built at `work/r02-01-xp4`; the strict section
gate passed, and the test suite reported 116 passes and two skips out of 118.
A 1,800-frame boot reached the logo. Final binary QA was still in progress,
and this boot check does not establish a completed story-route playtest. The
[machine-readable R02 audit](../work/agent-audit/r02-agent-usage.json)
and [audit script](../work/agent-audit/analyze-r02.py) preserve the exact
timestamp and counters.

After this usage snapshot, [frozen candidate QA](r02-qa-final.md) passed all disk,
IPS, preservation and trainer checks. The candidate is ready for player
verification; the usage table remains an explicitly timed snapshot.

## Assignment and acceptance

The [experiment configuration](../work/r02-experiment/configuration.json)
records the user-confirmed assignment: a GPT-6 Astra manager, GPT-6 Sol
reverse-engineering and QA workers, and a GPT-6 Luna localization worker, all
at medium reasoning. R01 used GPT-6 Astra at medium reasoning for the manager
and all three workers. R02 retained the R01 source, editorial, byte-preservation,
layout, independent-QA and section-release gates. R02 workers received bounded
standalone packets, whereas R01 used full-history forks. That context change,
reuse of R01 adapters, different story scope and unfinished R02 state prevent
an identical-work A/B comparison.

Two initially assigned GPT-5.6 Sol workers were interrupted before the
confirmed assignment. Their logged startup is outside the confirmed R02
totals below: RE had 14 requests, 73,761 uncached input tokens, 6,905 output
tokens and 5m 27s of task interval; QA had 22 requests, 89,380 uncached input
tokens, 6,201 output tokens and 4m 03s. Those intervals can overlap. Another
25 requests from the manager and early GPT-6 Sol/Luna starts also precede
confirmation. All 61 preconfirmation requests are excluded from the R02
confirmed-period figures; they used 263,647 uncached input and 18,389 output
tokens in total.

## Measured usage

“Task interval” is elapsed agent time inside logged tasks, clipped at the
snapshot for open tasks. It includes tool calls and waiting; concurrent agent
intervals must not be added to obtain wall time. “Uncached input” is reported
input minus reported cached input. Output includes the separately reported
reasoning-output subset, so that subset is not added a second time.

| Role | R01 model | R01 requests | R01 uncached input | R01 output | R01 task interval | R02 model | R02 requests | R02 uncached input | R02 output | R02 task interval to snapshot |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Manager | Astra | 119 | 201,719 | 50,744 | 42m 21s | Astra | 244 | 293,896 | 78,091 | 72m 09s |
| Reverse engineering | Astra | 138 | 305,084 | 52,157 | 33m 30s | Sol | 324 | 721,488 | 114,622 | 64m 38s |
| QA | Astra | 92 | 190,797 | 34,465 | 23m 44s | Sol | 399 | 598,748 | 123,270 | 72m 09s |
| Localization | Astra | 98 | 207,391 | 39,563 | 28m 43s | Luna | 242 | 357,642 | 131,515 | 67m 13s |
| **All four** | | **447** | **904,991** | **176,929** | **42m 21s wall** | | **1,209** | **1,971,774** | **447,498** | **72m 09s wall so far** |

The confirmed R02 agents logged 132,921,278 input tokens, of which
130,949,504 were cached. R01 logged 58,927,135 input tokens, of which
58,022,144 were cached. These are per-request context counters, not unique
source material. The [R01 baseline audit](../work/agent-audit/r01-agent-usage.md)
records its completed 14:47:16–15:29:37 CEST implementation window; its
permission-review infrastructure was counted separately from the four agents.
The R02 audit also excludes that infrastructure, whose session shares the
manager's root turn ID but runs under `codex-auto-review`.

## Work represented by these counters

The manager did substantial production work, not only coordination: Joe's
meeting dialogue fitting and name-boundary rewrite, the 15-record party and
remaining-label adaptation, the name packet, Joe
resident UI, release-plan expansion, and compiler integration. Independent QA
found and helped correct a material narration shift in the manager's Joe fit.
At this snapshot the manager had integrated the candidate and was coordinating
final binary QA.

The Sol RE worker mapped the 143-entry early-route script closure, reviewed
handlers and branch/menu geometry, proved the Hamack bar's tile partition,
implemented guarded menu-width and `GIRL` header-allocation changes, and fitted
the street, fortune, job and 22-record bar packets under original byte and
14×4-cell limits. The bar packet compiled jointly with the manager's 15 shared
party/header records. The Sol QA worker independently checked source IDs,
shop-handler semantics, Joe's equipment and ability names, implemented the protected
name adapter, and checked fixed UI fields,
speaker handoffs, exact token joins and adaptation wording. QA also corrected
its own initial false shop-stock and Joe profile-offset readings. These
contributions are recorded in the [source inventory](r02-qa-source-inventory.md),
[RE evidence](r02-re-source-evidence.md) and [editorial QA log](r02-qa-editorial.md).

Luna produced the canonical English packets for Hamack street, fortune/job,
bar, services and party dialogue, plus a first Joe adaptation, and performed
service fitting. QA-driven
revisions corrected source-meaning and speaker errors, including the job's
no-pay versus 200-credit outcomes, Rarawell/Jaguma relationship, and a party
speaker attribution. Luna's first Joe adaptation exposed repeated literal
names beside immutable `$name` tokens; the manager rebuilt that scene.
Service token joins had been corrected and the 38-record services packet
frozen before this snapshot. The QA log
describes observed defects in these particular packets, **not a model-wide
quality rate**.

The same acceptance rules helped expose these issues, but the work assigned to
each model was not interchangeable. R02 contains different content from R01,
more route closure and shop/name surfaces, and reused R01 engine adapters.
The manager provided major fitting assistance to both the RE and localization
streams. These usage totals therefore show the actual mixed-team run; they do
not establish which model is faster, cheaper or better for an equal packet.

## Measurement limits

The audit reads local JSONL session logs. It includes only each agent's own
`thread_id` token records, deduplicates `response_id`, sums per-response usage
instead of cumulative counters, and matches the manager by the workers'
`root_turn_id`. Model and effort come from turn context. Open task intervals
end at the audit timestamp, so a later snapshot will change R02 request,
token and elapsed-time figures. Agent intervals include waits and tool time;
they are neither inference time nor a measured speedup. The logs and audit do
not provide billed cost, exact model latency, or a solo control. No normalized
winner or cost-per-record claim follows from these measurements.
