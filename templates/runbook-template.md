# <Alert or failure name>

Owner: <team>
Last reviewed: <YYYY-MM-DD>

## Summary

<Two sentences: what this is and what usually causes it.>

## Severity

Default: <SEV level>. Raise to <level> if <condition>.

## Detection

- Alarm: `<alarm-name>`
- Symptom: <what users or engineers notice>

## Impact

<Who or what is affected.>

## Diagnosis

1. <Check>

   ```bash
   <command>
   ```

   Expected: <output>. If <condition>, go to step <n>.

## Mitigation

1. <Fastest safe action.>
2. Rollback: <how to undo.>

## Escalation

- After <time> without progress, page <role>.
- Contacts: <team channel, rotation link>

## Verification

- <Metric or check that proves recovery.>

## Prevention

- <Follow-up ticket or improvement.>
