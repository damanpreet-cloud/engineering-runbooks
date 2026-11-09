# ACM certificate nearing expiry

Owner: platform-team
Last reviewed: 2026-11-07

## Summary

An AWS Certificate Manager certificate is approaching expiry and has not renewed. Expired certificates cause TLS errors for users and failing service-to-service calls.

## Severity

Default: SEV3 when more than 7 days remain. Raise to SEV2 under 7 days, and SEV1 once a production certificate has expired.

## Detection

- EventBridge event: ACM Certificate Approaching Expiration
- Alarm: `acm-days-to-expiry-low`
- Symptom: browser certificate warnings, client TLS handshake failures.

## Impact

Users and clients cannot establish trusted TLS connections to the affected endpoints.

## Diagnosis

1. Check the certificate status and renewal details.

   ```bash
   aws acm describe-certificate --certificate-arn <arn> \
     --query 'Certificate.[Status,NotAfter,Type,RenewalEligibility,RenewalSummary.RenewalStatus]'
   ```

2. Identify the type.
   - `AMAZON_ISSUED`: ACM renews automatically if validation records still exist and the certificate is in use.
   - `IMPORTED`: ACM does **not** renew it. Someone must replace it.

3. For Amazon-issued certificates, check the validation record exists in DNS.

   ```bash
   aws acm describe-certificate --certificate-arn <arn> \
     --query 'Certificate.DomainValidationOptions[].ResourceRecord'
   dig +short CNAME <validation-record-name>
   ```

   A missing record is the most common reason renewal fails.

4. Confirm the certificate is attached to a load balancer or CloudFront distribution. Unused certificates may not auto-renew.

## Mitigation

1. **Missing DNS validation record:** recreate the CNAME in Route 53 or your DNS provider. Renewal usually proceeds within hours.
2. **Imported certificate:** obtain a new certificate, import it, and update listeners or distributions.

   ```bash
   aws acm import-certificate --certificate-arn <arn> \
     --certificate fileb://cert.pem --private-key fileb://key.pem \
     --certificate-chain fileb://chain.pem
   ```

   **Caution:** keep private keys out of tickets and chat, and delete local copies afterwards.
3. **Renewal stuck near the deadline:** request a new ACM certificate with DNS validation, attach it to the listener, then retire the old one.

## Escalation

- Under 7 days remaining with no fix path: page the platform lead.
- If a DNS provider outside the team is involved, contact the domain owner immediately.

## Verification

```bash
echo | openssl s_client -connect <hostname>:443 -servername <hostname> 2>/dev/null | openssl x509 -noout -dates
```

- New `notAfter` date is in the future.
- No TLS warnings from a browser or client.

## Prevention

- Inventory all certificates and alarm at 45, 30 and 14 days.
- Prefer DNS-validated, Amazon-issued certificates and keep validation records in Terraform.
- Track imported certificates separately with a named owner and calendar reminder.
