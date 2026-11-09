# ALB 5xx error spike

Owner: platform-team
Last reviewed: 2026-11-07

## Summary

An Application Load Balancer is returning an elevated rate of HTTP 5xx responses. Causes are usually a bad deploy, unhealthy targets, saturated targets, or a dependency failure.

## Severity

Default: SEV2. Raise to SEV1 if most production traffic is failing or the checkout/login path is down.

## Detection

- Alarm: `alb-prod-5xx-rate-high`
- Symptom: users see errors or timeouts; dashboards show 5xx above baseline.

## Impact

Users of the services behind the load balancer receive errors. Retries can amplify load on backends.

## Diagnosis

1. Decide who is producing the errors: the load balancer or the targets.

   ```bash
   aws cloudwatch get-metric-statistics --namespace AWS/ApplicationELB \
     --metric-name HTTPCode_ELB_5XX_Count --dimensions Name=LoadBalancer,Value=<app/lb-name/id> \
     --start-time <start-iso> --end-time <end-iso> --period 60 --statistics Sum
   ```

   Repeat with `HTTPCode_Target_5XX_Count`. If **ELB** 5xx dominates, the problem is the load balancer or no healthy targets. If **Target** 5xx dominates, the application is failing.

2. Read the status code.
   - 502: target closed the connection or sent an invalid response.
   - 503: no healthy targets registered.
   - 504: target did not respond before the idle timeout.

3. Check target health.

   ```bash
   aws elbv2 describe-target-health --target-group-arn <target-group-arn> \
     --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State,TargetHealth.Reason]' --output table
   ```

   Many `unhealthy` targets point to a bad deploy or a failing health check path.

4. Check for a recent change: deploys, config changes, Terraform applies in the last hour.

5. Check target saturation (CPU, memory, connections) and `TargetResponseTime`. High latency with 504s suggests overload or a slow dependency such as a database.

## Mitigation

1. **Recent deploy:** roll back to the last known good version. Do this first if the timing matches.
2. **Saturated targets:** scale out the service or node group.
3. **No healthy targets:** fix the health check path or security group so the load balancer can reach targets, then wait for targets to pass checks.
4. **Dependency failing:** follow that dependency's runbook (for example `rds-high-connections.md`).
5. **Caution:** do not restart all targets at once. Restart in small batches to keep capacity.

## Escalation

- No improvement after 15 minutes: page the service owner.
- Customer impact beyond 30 minutes: involve the incident commander.

## Verification

- 5xx rate back to baseline for 15 minutes.
- All targets `healthy`.
- Synthetic checks pass.

## Prevention

- Add deployment health gates and automatic rollback.
- Alarm on `UnHealthyHostCount` and `TargetResponseTime`, not only on 5xx.
- Load-test capacity before peak events.
