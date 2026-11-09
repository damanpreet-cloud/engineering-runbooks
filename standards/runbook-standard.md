# Runbook standard

## Purpose

A runbook lets any on-call engineer resolve a known failure mode without needing the author.

## Required sections

| Section | What it must answer |
|---------|---------------------|
| Summary | What is this, in two sentences? |
| Severity | Default severity and when to raise it (see the severity standard) |
| Detection | Which alerts or symptoms lead here? |
| Impact | Who or what is affected? |
| Diagnosis | Ordered checks, each with a command and what the output means |
| Mitigation | The fastest safe way to restore service, including rollback |
| Escalation | Who to call, and after how long |
| Verification | How to prove it is fixed |
| Prevention | The follow-up work that stops a repeat |

## Writing rules

- Put the **safest, fastest** mitigation before long diagnosis when service is down.
- Every command is copy-paste ready with placeholders in `<angle-brackets>`.
- State **expected output** and the decision it drives ("if X, go to step 4").
- Mark destructive steps with **Caution** and say how to undo them.
- Link dashboards and alarms; do not paste screenshots that go stale.
- Include `Owner:` and `Last reviewed:`. Review at least every six months and after every incident that used the runbook.

## Quality bar

A new team member should be able to follow the runbook cold. Test it in a game day or a tabletop exercise.
