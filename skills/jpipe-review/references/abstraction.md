# Abstraction: what the elements mean as an argument

**Authority: `argument`.** Nothing in this file is enforced by the grammar or the compiler. A model
can violate every rule here and still build, render, and run. These are findings the author may
decline, but they are the findings that decide whether the argument is worth anything.

This is the McSCert house reading of jPipe, promoted here from `jpipe-tutorial-2026/CLAUDE.md`. It is
a lens layered on the language, not a claim about the language designers' intent.

Only fenced blocks tagged `jd` are valid jPipe; blocks tagged `text` are fragments or deliberately
wrong.

---

## §1 Toulmin roles

A justification is an argument, so give its elements the vocabulary of arguments. Stephen Toulmin's
model (*The Uses of Argument*, 1958) names the parts, and jPipe's kinds map onto them cleanly:

| jPipe kind | Toulmin role | The question it answers |
|---|---|---|
| `conclusion` | **Claim** | What are you asserting? |
| `sub-conclusion` | an intermediate **Claim**, which then serves as **Grounds** one step up | What does this leg establish? |
| `strategy` | **Warrant** | What licenses the step from those grounds to that claim? |
| `evidence` | **Grounds** (data) | What does it rest on? |
| `@support` | an abstract **Grounds** slot | What must an implementor supply here? |

jPipe's own design documentation reaches for this vocabulary without naming it:
`jpipe-compiler/docs/design/language.md` glosses `conclusion` as *"A claim"* and `strategy` as
*"An argument"*.

The mapping is not decoration. It converts a vague complaint (*"this evidence is bad"*) into a
precise one (*"this is a Claim written into a Grounds slot"*), which tells the author exactly what to
do about it.

### What jPipe cannot express

Toulmin's model has three further roles, and jPipe has **no syntax for any of them**:

| Role | The question | Where it goes in jPipe |
|---|---|---|
| **Backing** | What authorizes the warrant itself? | Nowhere. Conventionally cited in the file's `/** */` header (*"per SPECS §3.3"*) |
| **Qualifier** | How strongly does the claim hold: *presumably*, *in all cases*? | Nowhere. jPipe claims are unqualified |
| **Rebuttal** | What would defeat this argument? | Nowhere. There is no counter-argument or defeater node |

**Do not raise findings about these.** A reviewer cannot ask an author to write what the language
cannot say. They are named here so you know where the language stops, and so you do not mistake their
absence for a defect in a particular model. If a missing backing or an unstated defeater genuinely
worries you, it belongs in the report's **Open questions** section as prose, never as a rule id.

---

## §2 The ladder

Grounds → Warrant → Claim is a rise in abstraction. Each rung is further from the raw artifact and
closer to what you want to assert:

```text
  claim         "The pipeline runs CPU-only"          ← an assertion about the system
    ↑
  warrant       "confront the declared packages       ← reasoning; has a truth value only
                 with the CPU-only allowlist"            once applied
    ↑
  grounds       "the committed Pipfile and its        ← a thing. It exists or it doesn't.
                 [packages] table"                       No judgement in it.
```

The working vocabulary is **fact → check → verdict**, and it is the one to use in reports because it
is concrete:

- **evidence = a fact.** An artifact that simply *exists*. Reading it requires no judgement. *"The
  committed Pipfile and its `[packages]` dependency table."* Someone who disagrees with the whole
  argument still agrees the Pipfile is there.
- **strategy = a check.** The reasoning applied to that fact, where the pass/fail lives. *"Confront
  the Pipfile's declared packages with the CPU-only allowlist; none lies outside it."*
- **sub-conclusion = a verdict.** What the leg establishes, which then becomes a fact for the leg
  above. *"The declared dependency environment offers no GPU or network capability."*

### Why a mislevelled leaf breaks the argument

Put a verdict in an evidence slot and the argument asserts its own conclusion as its starting point.
Consider:

```text
conclusion c is "The data splits are well-formed"
strategy   s is "The schema check covers every split"
evidence   e is "The schema check over each split passes"     ← the smell
```

The claim is *the splits are well-formed*. The ground offered is *the check passes*, which is the
claim again, one synonym away. The warrant does no work, because the conclusion was smuggled in at
the bottom. Nothing in this argument can fail except by contradicting itself.

Rewritten, the same three nodes carry real weight:

```jd
justification splits {
  conclusion c is "The data splits are well-formed"
  strategy   s is "Confront each split's column set with the schema in SPECS section 2; every split matches"
  evidence   e is "The committed train.csv, test.csv and counterfactual.csv, and their header rows"
  s supports c
  e supports s
}
```

Now the ground is checkable by inspection, the warrant states what would have to hold, and the
argument can fail, which is the only reason to write one.

---

## §3 Atomicity: one leaf, one fact

**An evidence leaf names exactly one artifact.**

```text
evidence e_env is "The committed Pipfile and the pipeline source files"    ← two facts fused
```

Two reasons this is a defect, and the second is the one people miss.

**It cannot be checked.** One warrant now has to do two unrelated things: confront declared packages
with an allowlist, *and* scan imports for GPU modules. If it fails, the report cannot say which. The
pass/fail loses its referent.

**It cannot be shared.** This is the deeper reason, and it reaches past the single file. A fused leaf
is unique by construction: no other model needs *exactly that pair*. Split it, and each atom is a
fact other arguments already depend on: the Pipfile grounds every claim about the dependency
environment, the source grounds every claim about what the code does. **The atom is the reusable
unit**, and in jPipe sharing is mechanical: two atoms with identical labels unify into one
`unified_N` node, so the check runs once and supports both goals (`language.md` §7).

Whether that sharing actually happens is a question about a corpus, which this skill does not read.
Atomicity is what makes it *possible*, and that much is visible right here.

So atomicity findings come **first**. A fused leaf also has no single artifact for the grounding pass
to search for, so splitting it is what makes the rest of the review possible.

### Telling one fact from two

Not every conjunction is a fusion. The test is whether the parts are checked **by the same reasoning**:

- *"the committed Pipfile and its `[packages]` dependency table"*: **one fact.** The table is part
  of the file; one inspection reads both. This is the r9 exemplar's actual wording.
- *"the committed train, test and counterfactual splits and their header rows"*: **one fact.** Three
  files, but one artifact set, read by one schema comparison.
- *"the committed Pipfile and the pipeline source files"*: **two facts.** An allowlist comparison
  and an import scan share nothing but the word "and".

Ask: *would splitting this force me to write two different checks?* If yes, it was two facts.

---

## §4 Category errors

Each of these is an element playing a role that belongs to a different rung.

### A01 · claim-as-evidence: a Claim in a Grounds slot

The canonical smell, and by a wide margin the most common. Tells, in a leaf's label:

| Phrasing | Example |
|---|---|
| *"a … check passes"* | "A schema check over each split passes" |
| *"… confirms …"* / *"… shows …"* / *"… demonstrates …"* | "The audit confirms no protected attribute is used" |
| *"… is computed correctly"* | "The flip-rate is computed correctly" |
| *"X is a Y"* (an assertion about an artifact, not the artifact) | "The feature step is a TF-IDF vectorizer" |
| any leaf that would make a reasonable `conclusion` | (no fixed phrasing) |

The test: **could this leaf be false in a way that requires reasoning to discover?** A fact is true or
false by inspection. If deciding it needs a judgement, it is a verdict.

**Two rewrites, and choosing between them is the actual work.**

*Single-leg*: the model already has a strategy that can host the check. Reword the leaf down to its
artifact and move the judgement up into the existing strategy. No new nodes, no id changes, no
unification impact. This is the cheap and common case.

*Multi-leg*: the verdict is one of several independent legs that must combine. Then the leg needs
its own `sub-conclusion`, its own `strategy`, and the artifact as `evidence` beneath. See §5.

Decide by asking how many independent things the conclusion depends on. One → reword. More → split.

### A02 · warrant-without-inference

The strategy names an artifact, restates the claim, or gives a title rather than licensing a step.
*"Testing argument"*, *"The Pipfile"*, *"The code is tested"*. A warrant must be a sentence that could
be argued with. State what is confronted with what, and what would have to hold.

### A03 · missing-intermediate-claim

Independent legs wire straight into the top strategy with no `sub-conclusion` between. Each leg
reaches a verdict; if it is not written down, the top warrant silently does the work of combining
several judgements, and a failing leg cannot be localised. The tell: one strategy with three or more
evidence leaves that have nothing to do with each other.

### A04 · claim-restates-warrant

The conclusion and the strategy beneath it say the same thing. One of them is not doing any work,
usually the strategy, which should say *how* rather than *what*.

### A05 · non-atomic-evidence

§3. Fix it before the grounding pass: a fused leaf names no single artifact to search for.

### A06 · unfalsifiable-warrant

The check has no observable pass/fail: *"the approach is sound"*, *"best practices are followed"*.
Nobody can run it and nobody can dispute it. Name the artifact, the comparison, and the outcome that
would count as failure.

---

## §5 The exemplar, node by node

`jpipe-tutorial-2026/justifications/requirements/r9.jd`: two `fact → check → verdict` legs
combined by a top warrant. This is what "at the right abstraction" looks like in full.

```jd
justification r9 {
    conclusion     c          is "The pipeline runs CPU-only, with no GPU and no network access (R9)"
    strategy       s          is "A run reaches a GPU or the network only through a capability that is both present in the environment and invoked by the code"

    sub-conclusion sc_stack   is "The declared dependency environment offers no GPU or network capability"
    strategy       s_allow    is "Confront the Pipfile's declared packages with the CPU-only allowlist; none lies outside it"
    evidence       e_pipfile  is "The committed Pipfile and its [packages] dependency table"

    sub-conclusion sc_imports is "The pipeline code invokes no GPU or network capability"
    strategy       s_scan     is "Scan the imports of every pipeline source file for a GPU or network module"
    evidence       e_source   is "The committed pipeline source: the src/ package and the run_v*.py entry points"

    s supports c
    sc_stack   supports s
    sc_imports supports s
    s_allow   supports sc_stack
    e_pipfile supports s_allow
    s_scan    supports sc_imports
    e_source  supports s_scan
}
```

Reading it against the ladder:

- `e_pipfile`, `e_source`: **grounds, and atomic.** Each names one artifact that exists in the tree.
  Neither asserts anything. Either could be shared by any other argument about the environment or the
  code.
- `s_allow`, `s_scan`: **warrants.** Each names what is confronted with what. The pass/fail lives
  here, and each is falsifiable: a package outside the allowlist, an import of `torch`.
- `sc_stack`, `sc_imports`: **verdicts**, one per leg. Written down, so a failure localises to a leg
  rather than to the whole requirement.
- `s`: the **top warrant**, and note what it does: it is not "both legs pass". It states *why those
  two legs are jointly sufficient*: reaching a GPU requires both a present capability and an
  invocation, so closing either suffices. That is a real inferential claim, and the argument is only
  as good as it.
- `c`: the **claim**, at the requirement's own level, tagged `(R9)` for traceability.

Note also what is absent: no **backing** for the allowlist itself (why is *that* the right allowlist?
It is cited in the file header as SPECS §3.3, not argued), and no **rebuttal** (nothing addresses a
dependency pulled in transitively). Both are §1 gaps in the language, not defects in r9.

---

## §6 The file scale

Classify each reviewed file. The scale is from `jpipe-tutorial-2026/justifications/REFACTOR_PROGRESS.md`,
where it was used to triage 34 requirement arguments by hand.

| | Meaning | Typical work |
|---|---|---|
| 🟢 | Already at the right abstraction | none |
| 🟡 | Single-leg reword: a leaf is a verdict, and an existing strategy can host the check | label-only, 1–2 lines, no id changes |
| 🟠 | Multi-leg: needs `sub-conclusion`s and new strategies to separate independent legs | structural; new ids; may shift `unified_N` |
| ⚪ | Judgement call: the "verdict" may legitimately be the fact | none; state it in Open questions and let the author decide |

⚪ is not a hedge, and it should not be rare. A requirement *about the test suite* may legitimately
ground on *"the test suite's last run record"*: the run record is an artifact, and it exists. The
rule is about mislevelling, not about banning the word "passes". When the honest answer is "this
depends on what R32 is really claiming", say that and stop.

---

## A note on the official examples

`jpipe-compiler/docs/design/language.md` uses `evidence e is "Test suite passes"` as its worked
example, and `jpipe-examples/release-example/release.jd` uses `"The test suite passes"`. Both are
`A01` under this reading.

This is worth stating plainly rather than letting it surprise anyone: **the official documentation
teaches the pattern this file flags.** Those examples optimise for showing the syntax in the fewest
possible tokens, which is a fair goal for a language tour and a bad one for an argument. Say so in
the report when a user's model came from that pattern: it is a reason to explain the rule, not a
reason to soften it, and not a reason to imply the author was careless.
