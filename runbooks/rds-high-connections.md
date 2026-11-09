# RDS high connections or CPU

Owner: platform-team
Last reviewed: 2026-11-07

## Summary

An RDS instance is near its connection limit or at sustained high CPU, causing slow queries or connection errors in applications.

## Severity

Default: SEV2. Raise to SEV1 if the database is rejecting connections for production traffic.

## Detection

- Alarms: `rds-prod-connections-high`, `rds-prod-cpu-high`
- Symptoms: "too many connections" errors, rising latency, connection timeouts.

## Impact

Applications depending on the database slow down or fail. Retry storms can make it worse.

## Diagnosis

1. Confirm the trend in CloudWatch.

   ```bash
   aws cloudwatch get-metric-statistics --namespace AWS/RDS --metric-name DatabaseConnections \
     --dimensions Name=DBInstanceIdentifier,Value=<db-instance-id> \
     --start-time <start-iso> --end-time <end-iso> --period 60 --statistics Maximum
   ```

2. Open Performance Insights for the instance and sort by **top SQL** and **top waits**. One query or one application is usually responsible.

3. Look at sessions directly.

   PostgreSQL:

   ```sql
   SELECT state, count(*) FROM pg_stat_activity GROUP BY state ORDER BY 2 DESC;
   SELECT pid, usename, state, now() - state_change AS idle_for, left(query, 80)
   FROM pg_stat_activity WHERE state = 'idle in transaction' ORDER BY idle_for DESC LIMIT 20;
   ```

   MySQL:

   ```sql
   SHOW FULL PROCESSLIST;
   ```

   Many `idle in transaction` sessions mean an application is leaking connections or holding transactions open.

4. Identify the client by user, host or application name, and check whether it was recently deployed or scaled out.

## Mitigation

1. **Connection leak or pool misconfiguration:** restart or scale down the offending application so its pools reset. Start with one instance.
2. **Runaway query:** cancel it.

   ```sql
   SELECT pg_cancel_backend(<pid>);
   ```

   **Caution:** use `pg_terminate_backend(<pid>)` only if cancel fails, and never on replication or system sessions.
3. **Legitimate load growth:** scale the instance class up, or add a read replica for read traffic.
4. **Short term:** reduce application pool sizes so total connections stay below the limit.

## Escalation

- No improvement after 20 minutes: page the database or service owner.
- Any risk to data integrity: escalate to SEV1 immediately.

## Verification

- Connections below 70% of the limit and stable.
- CPU back to baseline.
- Application latency and error rates normal.

## Prevention

- Use RDS Proxy or a pooler to cap and reuse connections.
- Set sane pool sizes per application and enforce idle timeouts.
- Add alarms at 70% of connection limit and track slow queries.
