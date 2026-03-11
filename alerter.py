import smtplib
from simulation import ERROR_CATALOG

class Alerter:
    def __init__(self, admin_email="rzkaunain@gmail.com"):
        self.admin_email = admin_email

    def guess_error_code(self, storage, latency, load):
        """Guess the most likely error if a job fails based on telemetry"""
        if storage > 90:
            return "ERR_003" # Storage Full
        elif latency > 150:
            return "ERR_002" # Network Reset
        elif load > 85:
            return "ERR_005" # Limits Reached
        else:
            return "ERR_001" # Default to VSS timeout

    def trigger_alert(self, job_data, fail_prob, risk_level):
        """Format and send the alert"""
        job_name = job_data.get('job_name', 'Unknown_Job')
        storage = job_data.get('storage_usage_pct', 0)
        latency = job_data.get('latency_ms', 0)
        load = job_data.get('server_load_pct', 0)

        error_code = self.guess_error_code(storage, latency, load)
        error_details = ERROR_CATALOG.get(error_code, ERROR_CATALOG["ERR_001"])
        
        msg = f"""
=====================================================
ALERT: PREDICTED BACKUP FAILURE - ACTION REQUIRED
=====================================================
To: {self.admin_email}
Subject: [Veeam] High Risk Backup Job Detected

Backup Job Name: {job_name}
Backup Job Risk Level: {risk_level}
Failure Probability: {fail_prob * 100:.0f}%

Reason for failure: {error_details['message']}

Troubleshooting Steps: 
{error_details['troubleshooting']}

Automated Retry Recommendation: Wait 15 minutes, check limits and storage, then retry.
=====================================================
"""
        # We simulate the email sending to console
        print(f"\n[!] SENDING EMAIL TO {self.admin_email}...")
        print(msg)
