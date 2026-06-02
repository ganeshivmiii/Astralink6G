import json
import os
import time

import joblib
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="AstraLink 6G",
    page_icon="A",
    layout="wide"
)


def apply_premium_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --airtel-red: #e4001b;
            --airtel-deep-red: #b00016;
            --ink: #101114;
            --muted: #6f737c;
            --line: #eceef2;
            --soft: #f7f8fa;
            --white: #ffffff;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', Arial, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 0%, rgba(228, 0, 27, 0.10), transparent 32%),
                linear-gradient(180deg, #ffffff 0%, #f7f8fb 44%, #ffffff 100%);
            color: var(--ink);
        }

        .block-container {
            max-width: 1240px;
            padding-top: 28px;
            padding-bottom: 48px;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .main-hero {
            position: relative;
            overflow: hidden;
            padding: 32px 34px;
            border: 1px solid rgba(228, 0, 27, 0.16);
            border-radius: 8px;
            background:
                linear-gradient(135deg, rgba(228, 0, 27, 0.96), rgba(176, 0, 22, 0.96)),
                repeating-linear-gradient(120deg, rgba(255,255,255,0.10) 0 1px, transparent 1px 28px);
            box-shadow: 0 20px 48px rgba(20, 22, 28, 0.16);
            margin-bottom: 22px;
        }

        .main-hero::after {
            content: "";
            position: absolute;
            top: -110px;
            right: -70px;
            width: 280px;
            height: 280px;
            border: 34px solid rgba(255,255,255,0.16);
            border-radius: 50%;
        }

        .brand-row {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            margin-bottom: 26px;
        }

        .brand-mark {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: #fff;
            font-weight: 800;
            font-size: 15px;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .brand-dot {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: #fff;
            color: var(--airtel-red);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        }

        .status-pill {
            color: #fff;
            border: 1px solid rgba(255,255,255,0.40);
            background: rgba(255,255,255,0.12);
            border-radius: 999px;
            padding: 8px 12px;
            font-size: 13px;
            font-weight: 700;
        }

        .hero-title {
            position: relative;
            z-index: 1;
            margin: 0;
            color: #fff;
            font-size: 42px;
            line-height: 1.08;
            font-weight: 800;
            letter-spacing: 0;
            max-width: 820px;
        }

        .hero-copy {
            position: relative;
            z-index: 1;
            max-width: 720px;
            margin: 14px 0 0;
            color: rgba(255,255,255,0.88);
            font-size: 16px;
            line-height: 1.55;
        }

        .metric-card {
            padding: 18px 18px 16px;
            border-radius: 8px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,0.92);
            box-shadow: 0 12px 30px rgba(20, 22, 28, 0.08);
            min-height: 104px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0;
            margin-bottom: 9px;
        }

        .metric-value {
            color: var(--ink);
            font-size: 26px;
            font-weight: 800;
            line-height: 1.1;
        }

        .metric-note {
            margin-top: 7px;
            color: var(--muted);
            font-size: 12px;
            font-weight: 500;
        }

        .section-title {
            margin: 18px 0 8px;
            color: var(--ink);
            font-size: 22px;
            line-height: 1.2;
            font-weight: 800;
            letter-spacing: 0;
        }

        .section-copy {
            margin: 0 0 18px;
            color: var(--muted);
            font-size: 14px;
            line-height: 1.55;
        }

        div[data-testid="stTabs"] button {
            border-radius: 8px 8px 0 0;
            color: #40434a;
            font-weight: 700;
            white-space: nowrap;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--airtel-red);
            border-bottom-color: var(--airtel-red);
        }

        div[data-testid="stTabs"] div[role="tablist"] {
            gap: 6px;
            overflow-x: auto;
            scrollbar-width: thin;
        }

        div[data-testid="stVerticalBlock"] > div:has(> .stDataFrame),
        div[data-testid="stVerticalBlock"] > div:has(> .stPlotlyChart),
        div[data-testid="stVerticalBlock"] > div:has(> .stPyplot),
        div[data-testid="stVerticalBlock"] > div:has(> .stVegaLiteChart) {
            border-radius: 8px;
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: #ffffff;
            padding: 14px 16px;
            box-shadow: 0 10px 24px rgba(20, 22, 28, 0.06);
        }

        .stButton > button {
            width: 100%;
            border: 0;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--airtel-red), var(--airtel-deep-red));
            color: #fff;
            font-weight: 800;
            padding: 12px 18px;
            box-shadow: 0 12px 26px rgba(228, 0, 27, 0.24);
        }

        .stButton > button:hover {
            color: #fff;
            border: 0;
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(228, 0, 27, 0.30);
        }

        input, textarea, select {
            border-radius: 8px !important;
        }

        div[data-baseweb="input"],
        div[data-baseweb="select"] {
            border-radius: 8px;
        }

        div[data-testid="stAlert"] {
            border-radius: 8px;
            border: 1px solid var(--line);
        }

        .route-chip {
            display: inline-block;
            margin: 4px 8px 4px 0;
            padding: 8px 10px;
            border-radius: 999px;
            background: #111217;
            color: #ffffff;
            font-size: 13px;
            font-weight: 800;
        }

        .responsive-note {
            display: none;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.4;
            margin: 2px 0 12px;
        }

        .loader-panel {
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            border: 1px solid rgba(228, 0, 27, 0.22);
            background: linear-gradient(135deg, #111217, #25272f);
            padding: 18px 20px;
            color: #ffffff;
            box-shadow: 0 14px 34px rgba(20, 22, 28, 0.16);
            margin: 12px 0;
        }

        .loader-panel::before {
            content: "";
            position: absolute;
            inset: 0;
            transform: translateX(-100%);
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.16), transparent);
            animation: shimmer 1.5s infinite;
        }

        .loader-title {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 15px;
            font-weight: 800;
        }

        .signal-loader {
            position: relative;
            width: 38px;
            height: 28px;
            display: inline-flex;
            align-items: end;
            gap: 4px;
        }

        .signal-loader span {
            display: block;
            width: 7px;
            border-radius: 999px;
            background: #e4001b;
            animation: signalRise 0.9s ease-in-out infinite;
        }

        .signal-loader span:nth-child(1) {
            height: 10px;
            animation-delay: 0s;
        }

        .signal-loader span:nth-child(2) {
            height: 18px;
            animation-delay: 0.12s;
        }

        .signal-loader span:nth-child(3) {
            height: 26px;
            animation-delay: 0.24s;
        }

        .loader-copy {
            position: relative;
            z-index: 1;
            color: rgba(255,255,255,0.74);
            margin-top: 8px;
            font-size: 13px;
            line-height: 1.5;
        }

        .risk-panel {
            border-radius: 8px;
            border: 1px solid var(--line);
            background: #ffffff;
            padding: 18px;
            box-shadow: 0 12px 30px rgba(20, 22, 28, 0.08);
            margin: 8px 0 16px;
        }

        .risk-track {
            height: 10px;
            border-radius: 999px;
            background: linear-gradient(90deg, #16a34a, #f59e0b, #e4001b);
            margin-top: 10px;
            overflow: hidden;
        }

        .risk-marker {
            width: 3px;
            height: 10px;
            background: #111217;
            margin-left: var(--risk-value);
        }

        .risk-label {
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            margin-top: 8px;
        }

        @keyframes shimmer {
            100% {
                transform: translateX(100%);
            }
        }

        @keyframes signalRise {
            0%, 100% {
                opacity: 0.45;
                transform: scaleY(0.72);
            }
            50% {
                opacity: 1;
                transform: scaleY(1);
            }
        }

        @media (max-width: 980px) {
            .block-container {
                max-width: 100%;
                padding-left: 22px;
                padding-right: 22px;
            }

            .hero-title {
                max-width: 720px;
                font-size: 36px;
            }

            .metric-card {
                min-height: 96px;
                margin-bottom: 10px;
            }

            div[data-testid="stMetric"] {
                margin-bottom: 10px;
            }
        }

        @media (max-width: 760px) {
            .block-container {
                padding-top: 18px;
                padding-left: 14px;
                padding-right: 14px;
                padding-bottom: 32px;
            }

            .main-hero {
                padding: 22px 18px;
                margin-bottom: 16px;
                box-shadow: 0 14px 34px rgba(20, 22, 28, 0.14);
            }

            .main-hero::after {
                top: -92px;
                right: -114px;
                width: 220px;
                height: 220px;
                border-width: 26px;
            }

            .brand-row {
                align-items: flex-start;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 20px;
            }

            .brand-mark {
                font-size: 13px;
            }

            .brand-dot {
                width: 30px;
                height: 30px;
            }

            .status-pill {
                font-size: 12px;
                padding: 7px 10px;
            }

            .hero-title {
                font-size: 28px;
                line-height: 1.12;
                max-width: 100%;
            }

            .hero-copy {
                font-size: 14px;
                line-height: 1.5;
            }

            .metric-card {
                padding: 15px;
                min-height: auto;
            }

            .metric-value {
                font-size: 22px;
                overflow-wrap: anywhere;
            }

            .section-title {
                font-size: 19px;
                margin-top: 14px;
            }

            .section-copy {
                font-size: 13px;
                margin-bottom: 14px;
            }

            div[data-testid="stTabs"] div[role="tablist"] {
                padding-bottom: 4px;
            }

            div[data-testid="stTabs"] button {
                font-size: 13px;
                min-width: max-content;
                padding-left: 10px;
                padding-right: 10px;
            }

            .stButton > button {
                min-height: 46px;
                padding: 12px 14px;
                font-size: 14px;
            }

            .loader-panel {
                padding: 16px;
            }

            .loader-title {
                align-items: flex-start;
                font-size: 14px;
            }

            .risk-panel {
                padding: 15px;
                margin-top: 4px;
            }

            .route-chip {
                font-size: 12px;
                padding: 7px 9px;
                margin-right: 5px;
            }

            .responsive-note {
                display: block;
            }

            div[data-testid="stDataFrame"],
            div[data-testid="stTable"],
            div[data-testid="stVegaLiteChart"],
            div[data-testid="stPyplot"] {
                overflow-x: auto;
            }

            canvas,
            svg {
                max-width: 100% !important;
            }
        }

        @media (max-width: 420px) {
            .hero-title {
                font-size: 24px;
            }

            .hero-copy {
                font-size: 13px;
            }

            .metric-label {
                font-size: 11px;
            }

            .metric-value {
                font-size: 20px;
            }

            .signal-loader {
                width: 32px;
                min-width: 32px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_intro(title, copy):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <p class="section-copy">{copy}</p>
        """,
        unsafe_allow_html=True
    )


def premium_loader(title, copy):
    st.markdown(
        f"""
        <div class="loader-panel">
            <div class="loader-title">
                <span class="signal-loader"><span></span><span></span><span></span></span>
                {title}
            </div>
            <div class="loader-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def estimate_risk(inputs):
    risk = (
        inputs["Latency"] * 0.33
        + inputs["PacketLoss"] * 4.9
        + inputs["Jitter"] * 0.7
        + inputs["EdgeServerLoad"] * 0.36
        + inputs["HandoverRate"] * 1.8
        - inputs["Throughput"] * 0.025
        - inputs["SignalStrength"] * 0.11
    )
    return max(0, min(100, round(risk, 1)))


def risk_panel(score):
    if score >= 70:
        posture = "Critical congestion posture"
    elif score >= 45:
        posture = "Elevated network pressure"
    else:
        posture = "Stable operating posture"

    st.markdown(
        f"""
        <div class="risk-panel">
            <div class="metric-label">Live Risk Index</div>
            <div class="metric-value">{score}%</div>
            <div class="metric-note">{posture}</div>
            <div class="risk-track" style="--risk-value: {score}%;">
                <div class="risk-marker"></div>
            </div>
            <div class="risk-label"><span>Stable</span><span>Watch</span><span>Critical</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )


@st.cache_resource
def load_artifacts():
    model = joblib.load("models/congestion_model.pkl")
    congestion_encoder = joblib.load("models/congestion_label_encoder.pkl")
    slice_encoder = joblib.load("models/network_slice_encoder.pkl")
    return model, congestion_encoder, slice_encoder


@st.cache_data
def load_data():
    raw = pd.read_csv("data/raw/network_data.csv")
    processed = pd.read_csv("data/processed/processed_network_data.csv")
    return raw, processed


def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def route_graph():
    graph = nx.Graph()
    links = [
        ("Device_A", "Device_B", {"latency": 10, "packet_loss": 1.2, "bandwidth": 850, "congestion": 18}),
        ("Device_A", "Device_C", {"latency": 15, "packet_loss": 2.0, "bandwidth": 700, "congestion": 25}),
        ("Device_B", "Device_D", {"latency": 12, "packet_loss": 1.8, "bandwidth": 620, "congestion": 30}),
        ("Device_C", "Device_D", {"latency": 10, "packet_loss": 3.1, "bandwidth": 480, "congestion": 42}),
        ("Device_D", "Device_E", {"latency": 5, "packet_loss": 0.8, "bandwidth": 950, "congestion": 12}),
        ("Device_E", "Device_F", {"latency": 8, "packet_loss": 1.0, "bandwidth": 900, "congestion": 16}),
        ("Device_C", "Device_F", {"latency": 30, "packet_loss": 5.0, "bandwidth": 320, "congestion": 60})
    ]

    for source, target, metrics in links:
        score = (
            metrics["latency"]
            + metrics["packet_loss"] * 7
            + metrics["congestion"] * 0.45
            + (1000 / metrics["bandwidth"]) * 8
        )
        graph.add_edge(source, target, optimization_score=round(score, 2), **metrics)

    path = nx.shortest_path(
        graph,
        "Device_A",
        "Device_F",
        weight="optimization_score"
    )
    score = nx.shortest_path_length(
        graph,
        "Device_A",
        "Device_F",
        weight="optimization_score"
    )
    return graph, path, score


model, congestion_encoder, slice_encoder = load_artifacts()
raw_data, processed_data = load_data()
metrics = read_json("reports/model_metrics.json")

apply_premium_theme()

st.markdown(
    """
    <section class="main-hero">
        <div class="brand-row">
            <div class="brand-mark"><span class="brand-dot">A</span> AstraLink 6G</div>
            <div class="status-pill">AI Operations Console</div>
        </div>
        <h1 class="hero-title">AstraLink 6G intelligence for premium network operations.</h1>
        <p class="hero-copy">
            A telecom-grade command experience for congestion prediction, interactive traffic simulation,
            anomaly detection, model intelligence, and optimized 6G routing.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

overview_cols = st.columns(4)
with overview_cols[0]:
    metric_card("Network Records", f"{len(raw_data):,}", "Synthetic 6G telemetry samples")
with overview_cols[1]:
    metric_card("Best Model", metrics.get("best_model", "Run training"), "Selected by test and CV score")
with overview_cols[2]:
    metric_card("Accuracy", metrics.get("accuracy", "N/A"), "Latest trained model result")
with overview_cols[3]:
    metric_card("High Congestion", int((raw_data["Congestion"] == "High").sum()), "Records needing attention")

prediction_tab, analytics_tab, model_tab, anomaly_tab, routing_tab = st.tabs([
    "Prediction",
    "Traffic Analytics",
    "Model Insights",
    "Anomaly Detection",
    "Smart Routing"
])

st.markdown(
    '<p class="responsive-note">Swipe the tab row horizontally to explore every AstraLink module.</p>',
    unsafe_allow_html=True
)

with prediction_tab:
    section_intro(
        "Network Congestion Prediction",
        "Enter network conditions and get a class prediction with model confidence."
    )

    scenarios = {
        "Balanced city cell": {
            "users": 1200,
            "bandwidth": 820,
            "latency": 34,
            "signal": 82,
            "packet_loss": 2.4,
            "throughput": 610.0,
            "jitter": 7.5,
            "energy": 48.0,
            "handover": 2.1,
            "mobility": 32,
            "edge_load": 42,
            "network_slice": "eMBB"
        },
        "Metro peak load": {
            "users": 5400,
            "bandwidth": 520,
            "latency": 112,
            "signal": 58,
            "packet_loss": 9.8,
            "throughput": 280.0,
            "jitter": 24.0,
            "energy": 92.0,
            "handover": 7.4,
            "mobility": 76,
            "edge_load": 86,
            "network_slice": "eMBB"
        },
        "Ultra-low latency slice": {
            "users": 900,
            "bandwidth": 1450,
            "latency": 12,
            "signal": 91,
            "packet_loss": 0.8,
            "throughput": 1120.0,
            "jitter": 2.4,
            "energy": 38.0,
            "handover": 1.2,
            "mobility": 18,
            "edge_load": 28,
            "network_slice": "URLLC"
        },
        "High mobility handover": {
            "users": 2600,
            "bandwidth": 760,
            "latency": 74,
            "signal": 66,
            "packet_loss": 5.6,
            "throughput": 430.0,
            "jitter": 16.5,
            "energy": 76.0,
            "handover": 10.2,
            "mobility": 150,
            "edge_load": 68,
            "network_slice": "URLLC"
        }
    }

    scenario_name = st.selectbox("Network Scenario", list(scenarios.keys()))
    scenario = scenarios[scenario_name]

    left, right, live = st.columns([1, 1, 0.9])

    with left:
        users = st.slider("Users", 100, 6500, scenario["users"])
        bandwidth = st.slider("Bandwidth (Mbps)", 80, 1800, scenario["bandwidth"])
        latency = st.slider("Latency (ms)", 5, 180, scenario["latency"])
        signal = st.slider("Signal Strength", 35, 100, scenario["signal"])
        packet_loss = st.slider("Packet Loss (%)", 0.0, 25.0, scenario["packet_loss"])
        throughput = st.slider("Throughput (Mbps)", 5.0, 1800.0, scenario["throughput"])

    with right:
        jitter = st.slider("Jitter (ms)", 0.5, 55.0, scenario["jitter"])
        energy = st.slider("Energy Consumption", 8.0, 130.0, scenario["energy"])
        handover = st.slider("Handover Rate", 0.0, 12.0, scenario["handover"])
        mobility = st.slider("Mobility Speed (km/h)", 0, 180, scenario["mobility"])
        edge_load = st.slider("Edge Server Load (%)", 10, 95, scenario["edge_load"])
        network_slice = st.selectbox(
            "Network Slice",
            list(slice_encoder.classes_),
            index=list(slice_encoder.classes_).index(scenario["network_slice"])
        )

    input_data = pd.DataFrame({
        "Users": [users],
        "Bandwidth": [bandwidth],
        "Latency": [latency],
        "SignalStrength": [signal],
        "PacketLoss": [packet_loss],
        "Throughput": [throughput],
        "Jitter": [jitter],
        "EnergyConsumption": [energy],
        "HandoverRate": [handover],
        "MobilitySpeed": [mobility],
        "EdgeServerLoad": [edge_load],
        "NetworkSlice": slice_encoder.transform([network_slice])
    })

    live_inputs = input_data.iloc[0].to_dict()
    live_inputs["NetworkSlice"] = network_slice
    with live:
        risk_panel(estimate_risk(live_inputs))
        st.metric("Scenario", scenario_name)
        st.metric("Slice", network_slice)

    predict_clicked = st.button("Run AstraLink AI Prediction")

    if predict_clicked:
        loader_slot = st.empty()
        with loader_slot:
            premium_loader(
                "AstraLink AI is scanning the network state",
                "Evaluating latency pressure, throughput health, edge load, packet loss, and slice behavior."
            )
        time.sleep(0.8)
        loader_slot.empty()

        prediction = model.predict(input_data)
        label = congestion_encoder.inverse_transform(prediction)[0]
        probabilities = model.predict_proba(input_data)[0]
        probability_df = pd.DataFrame({
            "Congestion": congestion_encoder.inverse_transform(model.classes_),
            "Confidence": probabilities
        }).sort_values("Confidence", ascending=False)

        if label == "High":
            st.error(f"Predicted Congestion: {label}")
        elif label == "Medium":
            st.warning(f"Predicted Congestion: {label}")
        else:
            st.success(f"Predicted Congestion: {label}")

        st.metric("Top Confidence", f"{probability_df.iloc[0]['Confidence']:.2%}")
        st.bar_chart(probability_df.set_index("Congestion"))

with analytics_tab:
    section_intro(
        "Network Traffic Analytics",
        "Review traffic distribution, slice behavior, and performance trends across the generated network."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Congestion Distribution")
        st.bar_chart(raw_data["Congestion"].value_counts())
    with col2:
        st.subheader("Network Slice Distribution")
        st.bar_chart(raw_data["NetworkSlice"].value_counts())

    selected_slice = st.selectbox(
        "Filter by Network Slice",
        ["All"] + sorted(raw_data["NetworkSlice"].unique().tolist())
    )
    filtered_data = raw_data if selected_slice == "All" else raw_data[raw_data["NetworkSlice"] == selected_slice]

    trend_cols = st.columns([1, 1])
    with trend_cols[0]:
        sample_size = st.slider(
            "Telemetry Window",
            100,
            min(1000, len(filtered_data)),
            min(500, len(filtered_data))
        )
    with trend_cols[1]:
        trend_metrics = st.multiselect(
            "Trend Metrics",
            ["Latency", "Jitter", "PacketLoss", "Throughput", "EdgeServerLoad"],
            ["Latency", "Jitter", "PacketLoss"]
        )

    st.subheader("Live-Style Telemetry Trends")
    if trend_metrics:
        st.line_chart(filtered_data[trend_metrics].head(sample_size).reset_index(drop=True))
    else:
        st.info("Choose at least one metric to render the trend chart.")

    st.subheader("Throughput vs Edge Server Load")
    st.scatter_chart(
        filtered_data,
        x="EdgeServerLoad",
        y="Throughput",
        color="Congestion"
    )

with model_tab:
    section_intro(
        "Model Insights",
        "Compare trained models and inspect which network features drive congestion decisions."
    )

    if os.path.exists("reports/model_comparison.csv"):
        st.subheader("Model Comparison")
        st.dataframe(pd.read_csv("reports/model_comparison.csv"), width="stretch")

    if os.path.exists("reports/feature_importance.csv"):
        st.subheader("Feature Importance")
        feature_importance = pd.read_csv("reports/feature_importance.csv")
        st.bar_chart(feature_importance.set_index("Feature"))

    if os.path.exists("reports/confusion_matrix.csv"):
        st.subheader("Confusion Matrix")
        st.dataframe(pd.read_csv("reports/confusion_matrix.csv"), width="stretch")

with anomaly_tab:
    section_intro(
        "Anomaly Detection",
        "Surface abnormal telemetry patterns that may indicate latency spikes, packet loss, or overload."
    )

    if os.path.exists("reports/anomaly_detection.csv"):
        anomalies = pd.read_csv("reports/anomaly_detection.csv")
        col1, col2 = st.columns(2)
        col1.metric("Anomalies", int((anomalies["AnomalyLabel"] == "Anomaly").sum()))
        col2.metric("Normal Records", int((anomalies["AnomalyLabel"] == "Normal").sum()))
        st.bar_chart(anomalies["AnomalyLabel"].value_counts())
        st.subheader("Most Critical Anomalies")
        st.dataframe(
            anomalies.sort_values("AnomalyScore").head(15),
            width="stretch"
        )
    else:
        st.info("Run `python src/anomaly_detection.py` to generate anomaly reports.")

with routing_tab:
    section_intro(
        "Smart Multi-Factor Routing",
        "Find the best path using latency, packet loss, bandwidth, and congestion pressure together."
    )

    graph, path, score = route_graph()
    route_cols = st.columns([2, 1])
    with route_cols[0]:
        chips = "".join(f'<span class="route-chip">{node}</span>' for node in path)
        st.markdown(chips, unsafe_allow_html=True)
    with route_cols[1]:
        st.metric("Optimization Score", round(score, 2))

    pos = nx.spring_layout(graph, seed=42)
    fig, ax = plt.subplots(figsize=(7.8, 5.4), dpi=120)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    nx.draw(
        graph,
        pos,
        ax=ax,
        with_labels=True,
        node_size=2600,
        node_color="#e4001b",
        edge_color="#202228",
        font_weight="bold",
        font_color="#ffffff"
    )
    labels = {
        (u, v): f"L:{d['latency']} P:{d['packet_loss']} S:{d['optimization_score']}"
        for u, v, d in graph.edges(data=True)
    }
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=labels,
        ax=ax,
        font_size=8,
        bbox={"boxstyle": "round,pad=0.24", "fc": "#ffffff", "ec": "#eceef2"}
    )
    ax.set_title(
        "Latency, Packet Loss, Bandwidth, and Congestion Aware Routing",
        fontsize=13,
        fontweight="bold",
        color="#101114"
    )
    ax.axis("off")
    fig.tight_layout()
    st.pyplot(fig)
