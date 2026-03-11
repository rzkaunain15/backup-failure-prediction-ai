import time
from simulation import generate_historical_data, generate_realtime_job_stream
from model import BackupFailurePredictor
from alerter import Alerter

def main():
    print("==================================================")
    print("   AI-Powered Backup Failure Prediction System    ")
    print("==================================================")

    # 1. Generate Historical Data
    print("\n[*] Simulating historical Veeam backup logs for training...")
    historical_df = generate_historical_data(num_records=2000)
    print(f"[*] Generated {len(historical_df)} historical records.")

    # 2. Train the Model
    print("\n[*] Initializing and training the Random Forest AI model...")
    predictor = BackupFailurePredictor()
    predictor.train(historical_df)

    # 3. Setup Alerter
    alerter = Alerter(admin_email="rzkaunain@gmail.com")

    # 4. Monitor Real-time stream
    print("\n[*] Starting real-time Veeam backup job monitoring...")
    print("[*] Waiting for incoming jobs...\n")
    time.sleep(2)

    realtime_jobs = generate_realtime_job_stream(num_jobs=3)

    for i, job in enumerate(realtime_jobs):
        job_name = job['job_name']
        print(f"--------------------------------------------------")
        print(f"Analyzing Job [{i+1}/{len(realtime_jobs)}]: {job_name}")
        print(f"  Metrics: Storage {job['storage_usage_pct']}%, Load {job['server_load_pct']}%, Latency {job['latency_ms']}ms")

        fail_prob, risk_level = predictor.predict(job)
        
        print(f"  Result : Probability={fail_prob:.2f}, Risk={risk_level}")

        if risk_level == "HIGH":
            alerter.trigger_alert(job, fail_prob, risk_level)
        
        time.sleep(2)

    print("\n[*] Monitoring complete. Exiting...")

if __name__ == "__main__":
    main()
