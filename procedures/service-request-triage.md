# Service request triage

How an infrastructure team handles a steady flow of requests in a ticket system without losing the urgent ones or drowning in the routine ones.

## Intake

Every request needs: requester, environment, business reason, and a deadline if one exists. Missing information is requested once, in one message.

## Categories and targets

| Category | Examples | Target |
|----------|----------|--------|
| Access | New IAM role, SSO group change, VPN | 1 business day |
| Standard change | New S3 bucket, security group rule, DNS record | 2 business days |
| Project | New environment, migration | Planned and estimated |
| Incident | Something is broken now | Use the incident process, not the queue |

## Daily routine

1. Triage new tickets each morning and assign an owner.
2. Pick up the oldest breaching ticket before starting a new one.
3. Automate anything requested more than three times in a quarter.
4. Close with a short note on what changed and how to verify.

## Guardrails

- Production changes follow the change request template.
- Access requests need the owner's approval, recorded on the ticket.
- Anything that looks like an incident is escalated immediately.

## Metrics worth watching

- Time to first response and time to resolution by category
- Ticket reopen rate
- Top repeat requests (candidates for self-service)
