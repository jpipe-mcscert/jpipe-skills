# The interview: asking instead of guessing

Read this at Step 5. It is the step that makes this skill trustworthy, and the one most likely to make
it obnoxious.

---

## Why ask at all

Every other pass in this family resolves from evidence in the files. This one cannot. Whether *"the
committed training split"* and *"the train.csv split as committed"* name one file is knowledge **the
author has and the corpus does not record**. Two labels, two models, and nothing written down anywhere
that settles it.

There are only three things to do with that, and two are bad:

| | Result |
|---|---|
| Guess yes | A wrong merge. Collapses a distinction the author drew on purpose, and if applied, silently changes what the case claims |
| Guess no | The duplication survives, and the report claims the corpus is fine |
| **Ask** | One sentence of the author's attention buys a finding that is actually true |

A wrong merge is the worst outcome available to this skill, worse than finding nothing, because it
corrupts the argument while looking like an improvement. So: ask.

## Ask in prose, never with a picker

Write the questions as text and let the author answer in text. Do not reach for an interactive
question tool: this skill's `allowed-tools` deliberately excludes one, because a picker cannot be
answered in a headless run, and an approval step built on one deadlocks there instead of degrading.

The corollary matters as much as the rule. **If no answer arrives, the run must still be useful.**
Every unanswered cluster becomes an open question in the report and nothing is applied. A survey that
found and documented eleven candidate merges without confirming any of them is a good outcome.

---

## What to ask, and what never to ask

Ask **only** about artifact identity, and only where it is genuinely undecidable from the files. One
cluster, one question, answerable with a yes or a no.

Never ask:

- **anything the files answer.** Byte-identical labels naming the same artifact are already unified;
  byte-identical labels naming different ones are `R03` and get reported, not asked about.
- **anything the author would have to research.** If they have to go read a third file to answer,
  the question is really an open question in disguise.
- **for permission to think.** "Shall I look for shared evidence?" wastes the budget below.
- **the same thing twice.** Answers are recorded (see Decisions) precisely so a second run does not
  re-litigate them.

## Shape of a question

Quote both labels in full, give both locations, name the artifact you believe is shared, and say what
a yes will cause. The author should be able to answer without opening a file:

```text
1. Same artifact?
   r13.jd:11  `e_train`  "The committed training split"
   r20.jd:9   `e_data`   "The train.csv split as committed"
   I read both as data/train.csv. If yes, I will align both labels on
   "The committed data/train.csv split and its header row", and assemble will unify them
   into one node, so the check runs once for both goals.

2. Same artifact?
   g4_perf.jd:8   `e_report`  "The benchmark report"
   g6_green.jd:12  `e_timing`  "The recorded run timings"
   Less sure about this one: "report" may be the published summary rather than the raw
   timings. If they are different things, say no and I will leave both alone.
```

Note the second one. **Say how confident you are**, because it tells the author how much attention the
question deserves, and a question you are 55% sure about is more valuable than one you are 95% sure
about.

## Budget: at most 7 questions, in one message

One batched message, numbered, at most seven questions. Order by payoff: the cluster touching the most
models first, since aligning it removes the most duplicated work.

**What happens to the rest is part of the contract.** Clusters past the cap are *not* dropped and *not*
silently deferred: they go into the report's Open questions with both labels quoted, so the author can
resolve them in a second pass or answer them unprompted. Say how many there are.

Seven is a judgement about attention, not a technical limit. An author who answers three questions and
stops has still improved the corpus; an author facing forty answers none of them and stops reading the
report, which loses the findings you were certain about too.

If a corpus produces more than about twenty uncertain clusters, that is itself the finding: the corpus
has no shared vocabulary for its artifacts. Say that in the report, propose a canonical wording for the
two or three artifacts that recur most, and skip the interview entirely. One convention fixes what
twenty merges would only paper over.

## Recording answers

The report carries a **Decisions** section listing every question, its answer, and what followed:

```text
## Decisions

1. `data/train.csv` shared by r13 `e_train` and r20 `e_data` → **yes**. Became R1.
2. `g4_perf` `e_report` vs `g6_green` `e_timing` → **no**, different artifacts. Not reported.
3. r9 `e_env` and r14 `e_deps` → *unanswered*. In Open questions as O2.
```

This exists so the work is not repeated. A declined cluster is a real result: it says a human looked
and said no, which is worth more than silence. Never re-ask a declined cluster in a later run over the
same corpus, and never quietly promote one to a finding because a later question made it look likelier.

## After the answers

- **yes** → the cluster becomes an `R01`/`R02`/`F01` finding, citing the answer as its authority for
  artifact identity.
- **no** → recorded in Decisions as declined. Not a finding, not an open question.
- **unanswered, or an ambiguous answer** → an open question. Never act on silence, and never read a
  partial answer ("the first two look right") as covering the rest.
