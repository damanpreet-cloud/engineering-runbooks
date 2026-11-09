# engineering-runbooks

A sanitized, generic set of operational standards, runbooks, procedures and templates for running cloud platforms on AWS. It reflects how I approach operational excellence: clear standards, runbooks anyone on call can follow at 3 a.m., blameless reviews, and automation that checks the docs themselves.

All names, accounts and values are placeholders. Nothing here comes from a specific employer.

## Structure

| Folder | Contents |
|--------|----------|
| `standards/` | How we write runbooks, name and tag resources, write Terraform, and classify incident severity |
| `runbooks/` | Step-by-step guides for common incidents (ALB 5xx, RDS connections, EKS node NotReady, ACM expiry) |
| `procedures/` | Repeatable processes: on-call handover, service request triage |
| `templates/` | Runbook, post-incident review and change request templates |
| `scripts/` | `check_runbooks.py` enforces required sections in CI |

## Principles

1. **Runbooks are for tired people.** Short sentences, copy-paste commands, expected output, and a clear stop condition.
2. **Mitigate first, diagnose second.** Restore service, then find the cause.
3. **Every runbook has an owner and a review date.** Stale docs are worse than none.
4. **Blameless reviews.** Focus on systems and decisions, not individuals.
5. **Docs are code.** Changes go through pull requests, and CI checks structure.

## Contributing

Copy `templates/runbook-template.md` into `runbooks/`. CI fails if a required section or the `Owner:` and `Last reviewed:` lines are missing.

## License

MIT
