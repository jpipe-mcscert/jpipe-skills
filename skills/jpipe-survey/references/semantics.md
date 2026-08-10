# Reading elements as propositions

**Authority: `argument`.** This is the method the whole skill runs on, and it is a judgement rather
than a lookup: nothing in the grammar says two differently worded labels mean one thing. Read it before
comparing anything.

The question is never *"are these labels similar?"*. It is **what does each element claim, and what
does the relation between two claims oblige you to do?** There are five answers worth acting on, and
each one is a different edit:

| Relation | Reading | Do this | Rule |
|---|---|---|---|
| **contains** | one label claims a second, separately checkable thing | split it | `D01`, `D02` |
| **mislevelled** | one claim, written as two different kinds | re-level one | `L01` |
| **same** | one claim, two wordings | merge them | `M01`, `M02` |
| **establishes** | one claim would be a reason to believe the other | prove it | `P01` |
| **untimed** | one subject, two moments it could exist at | name it | `N02` |

---

## 1. Subject and assertion

Split every label into the **subject** (what it is about) and the **assertion** (what is claimed of
it). Comparison happens on the pair, never on the string.

| Label | Subject | Assertion |
|---|---|---|
| `evidence` "The committed data/train.csv and its header row" | `data/train.csv` | it is committed, with its header |
| `evidence` "The source and test code are available" | the source; the tests | each is available |
| `strategy` "Confront the split's column set with the protected-attribute list" | the column set, that list | they can be compared, and the comparison is the check |
| `sub-conclusion` "No protected attribute reaches the model" | the model's inputs | a property is claimed of them |
| `conclusion` "The model is trained properly" | the model | a property is claimed of it |

For `evidence`, the subject **is** the artifact, and `artifacts.md` §1 is the extraction: use it, do not
re-invent it. For the other three kinds there is no artifact, which is why `artifacts.md` cannot carry
this file: a strategy denotes a comparison and a conclusion denotes a property, and neither is a thing
you can `Glob` for. That is also why the old method only ever looked at leaves.

**An assertion with no subject is not comparable.** *"Best practices are followed"*, *"the approach is
sound"*: nothing to bucket, nothing to match. Record it and move on. If it blocked a comparison you
wanted to make, that is `N03`, and the fix belongs to `jpipe-review`.

## 2. Bucket before you compare

All pairs over a corpus is quadratic and almost entirely wasted. Bucket by the subject's **head noun**,
then compare only inside a bucket:

```text
split / splits / train.csv   → r13 e_train, r20 e_data, s1 e_train, g3 sc_data
metrics / metrics.json       → g2 e_metrics, g6 e_metrics, r3 c
tests / test code            → a1 e_src, r14 e_tests
```

Normalise for plurals, possessives and the leading article, nothing cleverer. Two labels using
different words for one thing land in different buckets and the pair is missed, which is the known
ceiling of this method.

> **Say the ceiling out loud.** The report states how many buckets held one member and were therefore
> never compared. A survey that implies it examined every pair is lying about its own coverage, and the
> reader has no way to tell.

## 3. The five relations, in this order

Apply the tests in sequence and stop at the first that fires. The order is not arbitrary: a fused label
cannot be compared until it is split, and a kind mismatch changes what a match even means.

### 3.1 contains, first

*Does one label name a second thing that would need its own check?* Then that label is fused, and the
test is mechanical: **would splitting it force two different checks?** *"The source and test code are
available"* would, since one reads the source tree and one reads the test tree. *"The committed Pipfile
and its `[packages]` table"* would not, since one inspection reads both, and a conjunction on its own
is therefore not the tell.

A fused label is unique by construction, because no other model needs exactly that pair, so it can
never share. Splitting it is what makes the rest of the analysis possible, which is why this test comes
first.

**Only report it with a partner named.** If some other element matches one half, that is `D01` and the
finding names the half, the partner, and the merge that follows. If nothing matches either half, say
nothing: a fused leaf with no payoff is `jpipe-review`'s `A05`, decided from one file, and reporting it
here duplicates that skill while adding nothing.

### 3.2 mislevelled

*Do the two express one claim while being different kinds?* A `strategy` in one model and an `evidence`
in another, saying the same thing, means at least one of them is on the wrong rung: a check is not a
fact, and whichever model got it wrong has an argument that cannot fail properly.

```text
g4.jd:9   strategy s_cov  is "Confront the coverage report with the changed file list"
r7.jd:11  evidence e_cov  is "The coverage report is confronted with the changed file list"
```

That is `L01`. **Do not propose the fix.** Which rung is right is a judgement about one model's internal
shape, so name the discrepancy, say which of the two looks wrong and why, and hand the re-level to
`jpipe-review`. Naming a disagreement is this skill's job; settling it is not.

### 3.3 same

*Could one label replace the other with no change in what the argument rests on?* Then it is one claim
under two wordings, and `M01`.

```text
a1.jd:8   evidence e_src  is "The source is available"
b2.jd:12  evidence e_code is "The code is available"
```

Nothing in either label names a path, so `artifacts.md` cannot resolve either one and the old method
stopped here. The subject is the same thing under two words for it, and that is enough to raise the
candidate, at a confidence that says how sure you are.

**Same kind only.** Two elements of different kinds saying one thing went to `L01` above, and merging
them would be the wrong fix.

**Leaves, not warrants.** Where the whole `fact → check → verdict` triple repeats, it is `M02` and the
fix is extraction, not alignment. Where only the fact repeats, align **the leaves and nothing else**:
the same artifact legitimately grounds different checks, and one model confronting a column set while
another confronts a checksum is two arguments doing different work on one fact.

### 3.4 establishes

*Would the other element's `conclusion`, if true, be a reason to believe this leaf?* Then the leaf
asserts something the corpus can prove, and that is `P01`.

This is deliberately weaker than identity. The leaf and the conclusion need not say the same thing:

```text
a1.jd:11  evidence   e_model is "The trained model artifact"
b2.jd:4   conclusion c       is "The model is trained properly"
```

Those are not one claim, and `M01` is wrong here. But b2 is a whole argument about the very thing a1
takes for granted, so grafting it under the leaf turns an assertion into an argument. → `prove.md`

### 3.5 untimed

*Do the two labels imply their shared subject exists at different moments?* One says committed, the
other says produced by a run. That is `N02`, and it **blocks** `M01` on the same pair: merging them
would silently pick a winner. → `lifecycle.md`

## 3b. Read the moment off the label

Per `evidence`, record which of `artifacts.md` §2's six kinds it names, because the kind is a claim
about **when** the artifact exists: a committed path exists now, a produced artifact exists after a run,
an external record exists elsewhere and always. Record "cannot tell" as its own answer; it is the common
case and it is what `JD-N` is about.

**This reads labels only.** Never `Glob` or `Grep` for an artifact a label names. A case may be
discharged at design time or from CI, so a file absent from a clean checkout may be git-ignored or may
not exist yet, and neither is a defect. This skill cannot be wrong about absence because it never looks.
→ `lifecycle.md` §2

## 4. Confidence, and why every finding carries it

Nothing is asked before the report, so the reader calibrates from what you say. Three levels, with
criteria rather than vibes:

| | Criteria | Appears as |
|---|---|---|
| **high** | Both labels resolve to one named artifact (`artifacts.md`), or they differ only in wording with the same subject and assertion | a finding, and a proposed fix |
| **medium** | Same subject, assertions plausibly one claim, but a reading is doing real work | a finding, and a proposed fix, with the reading stated |
| **low** | Same subject, and that is all. The assertions may or may not be one claim | reported, **never** proposed as a fix |

Say the reading in the finding: *"I read both of these as the test suite"*. It tells the reader the
identity claim is yours rather than the file's, which is exactly what makes it safe to act on, and it
is what the old interview was for.

**Low confidence is not a reason to stay silent.** It is a reason not to propose an edit. A candidate
the reader can settle in four seconds is worth naming; a fix applied on a guess is not.

## 5. The traps

These outlive any particular method, and every one of them has been paid for.

> **A wrong merge is worse than a missed one.** It collapses a distinction the author drew on purpose,
> and applied, it silently changes what the case claims. A missed merge costs a duplicated check.

- **String similarity is not identity, in either direction** (`artifacts.md` §3). *"The training split"*
  and *"the training configuration"* share four words in five and name different things; *"The committed
  Pipfile and its `[packages]` table"* and *"the dependency manifest as committed"* share almost nothing
  and name one file. A method that ranks by string distance gets both backwards, so subject and
  assertion are what get compared, never the label.
- **Never merge across a fused label.** §3.1 comes first for this reason.
- **Every merge carries its unification consequence.** Aligning two labels *creates* a shared node and
  renumbers every later `unified_N`, and those ids may be referenced from a step library this skill
  never opens (`language.md` §7).
- **`unifyExclude` is a workaround, never a fix.** It suppresses a merge and leaves two elements still
  claiming to be one fact.
- **Never report a bare count.** *"14 possible duplicates"* is not a finding. If the reader would have
  to redo your analysis to act on it, quote the labels or say nothing.
