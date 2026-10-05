# R03 agent usage snapshot

Audit timestamp: `2026-09-23T15:41:50.722569+00:00`. Candidate and independent binary/boot checks are complete; manager handoff work is still active, so these are snapshot counters.

All four agents used GPT-6 Astra at medium effort. Three workers handled RE, localization and QA; the manager integrated the release and drafted equipment names for independent review.

| Role | Requests | Uncached input | Cached input | Output | Task elapsed |
| --- | ---: | ---: | ---: | ---: | ---: |
| /root | 102 | 167,940 | 14,533,504 | 35,152 | 29m 32s |
| /root/r03_localizer | 81 | 103,785 | 5,991,296 | 25,210 | 21m 06s |
| /root/r03_qa | 148 | 184,545 | 17,167,616 | 34,806 | 28m 22s |
| /root/r03_re | 110 | 210,150 | 10,663,424 | 29,924 | 21m 47s |

Team totals: 441 requests; 666,420 uncached input, 48,355,840 cached input and 125,092 output tokens.

Task elapsed includes tools and waiting; concurrent times must not be summed as wall time. Per-response usage is deduplicated by response ID and restricted to each agent’s own thread; automatic approval review is excluded. Cached input is repeated context, not unique material. These counters do not measure weekly allowance or billed cost.

This batch added 37 story records, 24 menu/service records and 223 names, reusing previous engine adapters and adding new source proofs. Different content and work allocation prevent a controlled speed/cost comparison with R01 or R02. Six recommended name corrections and seven optional readability improvements came from independent review of the manager’s 220-name draft. QA/RE also corrected a false numeric-table alias and found reachable bridge UI and an unload refusal before release.

The audit script is `work/agent-audit/analyze-r03.py`; the machine-readable snapshot is `work/agent-audit/r03-agent-usage.json`. Rerunning after handoff recovers completed task intervals.
