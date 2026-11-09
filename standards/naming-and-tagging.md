# Naming and tagging standard

## Naming pattern

`<org>-<env>-<workload>-<resource>` in lowercase with hyphens, for example `acme-prod-orders-alb`.

## Required tags

| Tag | Example | Purpose |
|-----|---------|---------|
| `Environment` | `prod`, `nonprod`, `sandbox` | Cost and policy scoping |
| `Owner` | `platform-team` | Who to contact |
| `CostCenter` | `cc-1234` | Chargeback |
| `Service` | `orders` | Group resources by workload |
| `ManagedBy` | `terraform` | Detect drift and manual changes |

## Enforcement

- Terraform `default_tags` apply the baseline automatically.
- A tag policy at the organization level reports non-compliance.
- Untagged resources older than 30 days are reviewed in the monthly cost meeting.
