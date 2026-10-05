# Translation progress

The latest completed candidate is R09, through Daina and
the Begi historian. It has **1,064 adapted records in 107 reviewed scenes**.
Full route playtesting remains pending.

There is not yet a defensible percentage for the entire game. Source discovery
is incomplete, entries vary from a short label to a long conversation, and
translation coverage does not measure runtime verification.

The R09 source catalog supports these narrower measures:

| Measure | Adapted / cataloged | Coverage |
| --- | ---: | ---: |
| Decoded dialogue/script entries containing text | 623 / 1,564 | 39.8% |
| All known text-bearing records, including names and UI | 1,064 / 2,014 | 52.8% |
| All catalog records, including control-only scripts | 1,064 / 2,699 | 39.4% |

The dialogue measure is the most useful rough translation indicator. The name/UI
measure gives a label the same weight as a lengthy scene. The last denominator
contains 685 control-only scripts that need no English, so it is not a completion
target. None of these measures includes text that has not been cataloged.

Counts come from a fresh `profiles.alshark.replay` catalog: count records with
`target.status == "adapted"`; for text-bearing scripts, require at least one
`source.entry.tokens` member whose `kind` is `text`. Full source catalogs stay in ignored
`work/`. New discoveries can increase the denominator even while work progresses.

See the [section queue](section-release-workflow.md#current-release-queue) for
story boundaries, additions and known limitations, and the
[getting-started guide](getting-started.md) to build the candidate. Automated
validation makes batches ready for PR review; it does not replace player testing
of wrapping, choices, movement and story transitions.
