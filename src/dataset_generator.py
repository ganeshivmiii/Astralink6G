import pandas as pd
import numpy as np
import os
import sys

try:
    np.random.seed(42)
    records = 2500

    slice_types = np.random.choice(
        ["eMBB", "URLLC", "mMTC"],
        records,
        p=[0.45, 0.30, 0.25]
    )

    users = np.random.randint(100, 6500, records)
    bandwidth = np.random.randint(80, 1800, records)
    signal = np.random.randint(35, 101, records)
    mobility_speed = np.random.randint(0, 180, records)
    edge_server_load = np.random.randint(10, 96, records)
    handover_rate = np.random.uniform(0, 12, records).round(2)

    base_latency = (
        8
        + (users / 95)
        + (edge_server_load * 0.45)
        + (mobility_speed * 0.08)
        - (bandwidth / 45)
        - (signal * 0.18)
        + np.random.normal(0, 8, records)
    )
    latency = np.clip(base_latency, 5, 180).round(2)

    packet_loss = np.clip(
        (latency / 22)
        + (edge_server_load / 18)
        + (handover_rate * 0.55)
        - (signal / 35)
        + np.random.normal(0, 1.6, records),
        0,
        25
    ).round(2)

    throughput = np.clip(
        bandwidth * (1 - packet_loss / 120) * (signal / 100) - users * 0.025,
        5,
        None
    ).round(2)

    jitter = np.clip(
        latency * 0.18 + packet_loss * 1.7 + np.random.normal(0, 2, records),
        0.5,
        55
    ).round(2)

    energy_consumption = np.clip(
        18
        + users * 0.006
        + edge_server_load * 0.8
        + mobility_speed * 0.05
        - signal * 0.12
        + np.random.normal(0, 4, records),
        8,
        130
    ).round(2)

    congestion = []

    for i in range(records):
        risk_score = (
            latency[i] * 0.36
            + packet_loss[i] * 5.5
            + edge_server_load[i] * 0.45
            + handover_rate[i] * 2.2
            + jitter[i] * 0.65
            - throughput[i] * 0.03
            - signal[i] * 0.12
        )

        if slice_types[i] == "URLLC":
            risk_score += 8
        elif slice_types[i] == "mMTC":
            risk_score += 4

        if risk_score >= 85:
            congestion.append("High")
        elif risk_score >= 52:
            congestion.append("Medium")
        else:
            congestion.append("Low")

    data = pd.DataFrame({
        "Users": users,
        "Bandwidth": bandwidth,
        "Latency": latency,
        "SignalStrength": signal,
        "PacketLoss": packet_loss,
        "Throughput": throughput,
        "Jitter": jitter,
        "EnergyConsumption": energy_consumption,
        "HandoverRate": handover_rate,
        "MobilitySpeed": mobility_speed,
        "EdgeServerLoad": edge_server_load,
        "NetworkSlice": slice_types,
        "Congestion": congestion
    })

    # Use absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    output_path = os.path.join(project_dir, "data", "raw", "network_data.csv")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    data.to_csv(output_path, index=False)

    print(f"Dataset Created Successfully at {output_path}")
    print(data.head())
    sys.stdout.flush()

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.stderr.flush()
    sys.exit(1)
