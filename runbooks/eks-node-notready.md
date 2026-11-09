# EKS node NotReady

Owner: platform-team
Last reviewed: 2026-11-07

## Summary

One or more Kubernetes worker nodes report `NotReady`. Pods on them may be unreachable or rescheduled. Causes include kubelet failure, disk or memory pressure, network problems, or an unhealthy instance.

## Severity

Default: SEV3 for a single node. Raise to SEV2 if multiple nodes or a whole node group is affected.

## Detection

- Alarm: `eks-prod-node-notready`
- Symptom: `kubectl get nodes` shows `NotReady`; pods stuck `Terminating` or `Pending`.

## Impact

Workloads on the node lose capacity. If many nodes are affected, services degrade.

## Diagnosis

1. List node status.

   ```bash
   kubectl get nodes -o wide
   ```

2. Inspect conditions and events on the affected node.

   ```bash
   kubectl describe node <node-name>
   ```

   Look at `Conditions` for `MemoryPressure`, `DiskPressure`, `PIDPressure`, and the last heartbeat time.

3. Check the instance in EC2: status checks, system log, and whether it is still running.

   ```bash
   aws ec2 describe-instance-status --instance-ids <instance-id> --include-all-instances
   ```

4. Open a shell without SSH using Session Manager and check the kubelet.

   ```bash
   aws ssm start-session --target <instance-id>
   sudo systemctl status kubelet
   sudo journalctl -u kubelet --since "30 min ago" | tail -50
   df -h
   ```

5. If several nodes are affected at once, check for a shared cause: a recent AMI or add-on change, subnet IP exhaustion, a VPC CNI issue, or a security group change.

## Mitigation

1. Cordon the node so no new pods land on it.

   ```bash
   kubectl cordon <node-name>
   ```

2. Drain it if it still responds.

   ```bash
   kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data --timeout=300s
   ```

   **Caution:** check PodDisruptionBudgets first and drain one node at a time.
3. Replace the instance. For a managed node group, terminate the instance and the group launches a new one.

   ```bash
   aws ec2 terminate-instances --instance-ids <instance-id>
   ```

4. Disk pressure: clear unused images and logs, then investigate what filled the disk.
5. If a shared cause is found (bad AMI, config), roll back that change before replacing nodes.

## Escalation

- Multiple nodes down or capacity at risk: page the platform lead.
- Suspected AWS service issue: open a support case and check the Health Dashboard.

## Verification

- All nodes `Ready`.
- Pods rescheduled and `Running`; no pending pods due to capacity.
- Node group at desired size.

## Prevention

- Alarm on node `NotReady` duration and disk usage before pressure occurs.
- Keep headroom in capacity so one node loss is harmless.
- Roll out AMI updates gradually with `max_unavailable` limits.
