# Incident severity levels

| Level | Definition | Examples | Response |
|-------|------------|----------|----------|
| SEV1 | Full outage or data loss risk for production, or a security breach | Production unreachable, data corruption | Page immediately, incident commander assigned, updates every 30 minutes |
| SEV2 | Major degradation or a critical feature unavailable | Elevated 5xx for most users, a region impaired | Page on-call, updates every hour |
| SEV3 | Partial or limited impact with a workaround | One service degraded, non-production outage | Handle in business hours unless it worsens |
| SEV4 | Minor issue, no user impact | Cosmetic defect, warning alarm | Track as a ticket |

## Rules

- When unsure, **start one level higher** and downgrade later.
- Anyone can declare an incident. The on-call engineer owns severity.
- SEV1 and SEV2 get a post-incident review within five business days.
- Customer-facing communication goes through the incident commander.
