# On-call handover procedure

Run at every rotation change, ideally as a 15-minute call or a written handover in the team channel.

## Outgoing engineer

1. List open incidents and their current state.
2. List flapping alarms and any silenced alerts, with expiry times.
3. Note risky changes or deploys scheduled during the next shift.
4. Link tickets for follow-ups that need attention.
5. Mention anything unusual: capacity, vendor issues, certificate expiries within 30 days.

## Incoming engineer

1. Confirm paging works by sending a test page.
2. Confirm access to the cloud console, cluster, VPN and the runbook repo.
3. Read the open items and ask questions before the handover ends.
4. Skim the alarms dashboard for anything already in alarm.

## Handover note format

```text
Open incidents: <links or none>
Silenced alerts: <alarm, reason, expires>
Upcoming changes: <what, when, owner>
Watch items: <what to watch and why>
Follow-ups: <tickets>
```

## Principle

Nothing should be learned for the first time at 3 a.m. If the handover surprised you, improve the handover.
