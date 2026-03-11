import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Mock error catalog based on typical Veeam errors
ERROR_CATALOG = {
    "ERR_001": {
        "message": "VSS Snapshot Timeout (Error 0x80042306)",
        "troubleshooting": "1. Check VSS writers on the guest OS using 'vssadmin list writers'.\n2. Ensure no conflicting snapshot processes are running.\n3. Increase VSS snapshot timeout in Veeam settings."
    },
    "ERR_002": {
        "message": "Network Connection Reset by Peer",
        "troubleshooting": "1. Verify network connectivity between proxy and repository.\n2. Check firewall or antivirus blocking the connection.\n3. Implement traffic throttling rules if bandwidth is overwhelmed."
    },
    "ERR_003": {
        "message": "Storage Destination Full",
        "troubleshooting": "1. Free up space on the backup repository.\n2. Adjust backup retention policy to keep fewer restore points.\n3. Add extents to the Scale-Out Backup Repository."
    },
    "ERR_004": {
        "message": "Guest Processing Authentication Failure",
        "troubleshooting": "1. Verify guest OS credentials configured in the backup job.\n2. Ensure the account has administrative privileges.\n3. Check if the password has expired or been changed."
    },
    "ERR_005": {
        "message": "Proxy Resource Reached Processing Limit",
        "troubleshooting": "1. Add additional backup proxies.\n2. Increase concurrent task limits on existing proxies.\n3. Stagger backup jobs to avoid overlapping schedules."
    }
}

JOB_NAMES = [
    "SQL_DB_Nightly_Backup",
    "File_Server_Daily",
    "Exchange_Log_Backup",
    "VM_Infrastructure_Weekly",
    "Critical_App_Servers"
]

def generate_historical_data(num_records=1000):
    """
    Simulates historical Veeam backup logs to train the prediction model.
    Generates a mix of successful and failed jobs based on conditions.
    """
    data = []
    
    for _ in range(num_records):
        job_name = random.choice(JOB_NAMES)
        
        # Base features
        storage_usage_pct = round(random.uniform(30.0, 99.0), 2)
        server_load_pct = round(random.uniform(10.0, 99.0), 2)
        network_latency_ms = random.randint(1, 200)
        job_duration_mins = random.randint(10, 240)
        
        # Introduce failure conditions (high load, high storage, high latency)
        # If conditions are bad, higher probability of failure
        fail_prob = 0.05 # base 5%
        
        if storage_usage_pct > 90:
            fail_prob += 0.4
        if server_load_pct > 85:
            fail_prob += 0.3
        if network_latency_ms > 150:
            fail_prob += 0.2
            
        is_failed = random.random() < fail_prob
        
        if is_failed:
            status = "Failed"
            # Assign an error code based on conditions if possible, or random
            if storage_usage_pct > 90:
                error_code = "ERR_003"
            elif network_latency_ms > 150:
                error_code = "ERR_002"
            elif server_load_pct > 85:
                error_code = "ERR_005"
            else:
                error_code = random.choice(list(ERROR_CATALOG.keys()))
        else:
            status = "Success"
            error_code = "None"
            
        data.append({
            "job_name": job_name,
            "duration_mins": job_duration_mins,
            "latency_ms": network_latency_ms,
            "storage_usage_pct": storage_usage_pct,
            "server_load_pct": server_load_pct,
            "status": status,
            "error_code": error_code
        })
        
    return pd.DataFrame(data)

def generate_realtime_job_stream(num_jobs=5):
    """
    Generates a stream of real-time incoming backup jobs, deliberately pushing 
    some to high risk to trigger the alert system.
    """
    stream = []
    
    # 1 normal job
    stream.append({
        "job_name": "File_Server_Daily",
        "duration_mins": 45,
        "latency_ms": 20,
        "storage_usage_pct": 55.0,
        "server_load_pct": 30.0
    })
    
    # 1 high storage risk job
    stream.append({
        "job_name": "SQL_DB_Nightly_Backup",
        "duration_mins": 120,
        "latency_ms": 30,
        "storage_usage_pct": 96.5,  # High risk
        "server_load_pct": 50.0
    })
    
    # 1 high load and latency risk job
    stream.append({
        "job_name": "VM_Infrastructure_Weekly",
        "duration_mins": 210,
        "latency_ms": 180,  # High risk
        "storage_usage_pct": 70.0,
        "server_load_pct": 95.0     # High risk
    })
    
    return stream
