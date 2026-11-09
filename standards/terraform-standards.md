# Terraform standards

## Structure

- One root module per environment and one reusable module per concern.
- Pin Terraform and provider versions (`required_version`, `~>` constraints).
- Remote state in S3 with encryption and locking. One state per environment.

## Code rules

- Use `for_each` over `count` when items have identity.
- Variables have types, descriptions and validation where input can be wrong.
- No secrets in code or state outputs. Reference Secrets Manager or SSM.
- Prefer data-driven configuration (maps of objects) over copy-pasted blocks.

## Delivery

- Changes go through pull requests: `fmt`, `validate`, lint, security scan, then a reviewed `plan`.
- Apply from CI using OIDC federation, never from a laptop for shared environments.
- Production applies require an approval gate.
- Import existing resources instead of recreating them, and record why.

## Review checklist

- Does the plan only change what the PR describes?
- Any replacement of stateful resources (databases, volumes, load balancers)?
- Least privilege on every new IAM policy?
- Tags, encryption and logging present?
