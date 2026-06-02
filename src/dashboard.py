import time
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Astralink6G", page_icon="assets/favicon.svg", layout="wide")


def asset_uri(path):
    file = Path(path)
    if not file.exists():
        return ""
    import base64

    return "data:image/svg+xml;base64," + base64.b64encode(file.read_bytes()).decode("ascii")


def style():
    st.markdown(
        """
        <style>
        :root {
            --red: #e4001b;
            --dark: #111217;
            --muted: #69707a;
            --line: #eceef2;
        }
        .stApp {
            background: #f5f6f8;
            color: var(--dark);
        }
        #MainMenu, footer, [data-testid="stDeployButton"] {
            display: none;
        }
        .block-container {
            max-width: 1200px;
            padding-top: 26px;
            padding-bottom: 38px;
        }
        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 12px;
            padding: 34px;
            background:
                radial-gradient(circle at 92% 0%, rgba(255,255,255,.22) 0 16%, transparent 17%),
                linear-gradient(135deg, #e4001b, #b00016 72%);
            box-shadow: 0 20px 48px rgba(20, 22, 28, .16);
            margin-bottom: 20px;
            min-height: 290px;
        }
        .hero:after {
            content: "";
            position: absolute;
            right: -88px;
            top: -110px;
            width: 260px;
            height: 260px;
            border: 32px solid rgba(255,255,255,.15);
            border-radius: 50%;
        }
        .brand-logo {
            position: relative;
            z-index: 1;
            width: min(230px, 66vw);
            margin-bottom: 28px;
            display: block;
        }
        .hero h1 {
            position: relative;
            z-index: 1;
            max-width: 760px;
            margin: 0;
            color: white;
            font-size: 42px;
            line-height: 1.08;
            letter-spacing: 0;
            text-shadow: 0 2px 18px rgba(0,0,0,.18);
        }
        .hero p {
            position: relative;
            z-index: 1;
            max-width: 680px;
            color: #fff;
            font-size: 15px;
            line-height: 1.55;
            font-weight: 600;
        }
        .card {
            border: 1px solid var(--line);
            border-radius: 10px;
            background: white;
            padding: 16px;
            box-shadow: 0 12px 28px rgba(20, 22, 28, .08);
            min-height: 96px;
        }
        .label {
            color: var(--muted);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .value {
            color: var(--dark);
            font-size: 25px;
            font-weight: 900;
            margin-top: 8px;
            overflow-wrap: anywhere;
        }
        div[data-testid="stTabs"] div[role="tablist"] {
            overflow-x: auto;
            scrollbar-width: thin;
        }
        div[data-testid="stTabs"] button {
            white-space: nowrap;
            font-weight: 800;
            color: #4b5563 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #e4001b !important;
        }
        .stMarkdown, .stText, p, label, span, h1, h2, h3, h4 {
            color: #111217;
        }
        div[data-testid="stWidgetLabel"] label,
        div[data-testid="stWidgetLabel"] p,
        .stSlider label,
        .stSelectbox label,
        .stMultiSelect label {
            color: #111217 !important;
            font-weight: 800 !important;
        }
        div[data-baseweb="select"] > div {
            background: #fff !important;
            color: #111217 !important;
            border: 1px solid #d8dce3 !important;
        }
        div[data-baseweb="select"] span {
            color: #111217 !important;
        }
        div[data-testid="stSlider"] [data-baseweb="slider"] div {
            color: #111217 !important;
        }
        div[data-testid="stSlider"] [role="slider"] {
            background: #e4001b !important;
            border-color: #e4001b !important;
        }
        div[data-testid="stSlider"] [data-testid="stTickBar"] {
            color: #111217 !important;
        }
        .stButton > button {
            width: 100%;
            border: 0;
            border-radius: 9px;
            background: linear-gradient(135deg, #e4001b, #a80015);
            color: white;
            font-weight: 900;
            min-height: 46px;
            box-shadow: 0 14px 28px rgba(228,0,27,.25);
        }
        .loader {
            border-radius: 10px;
            background: linear-gradient(135deg, #111217, #272a33);
            color: white;
            padding: 16px;
            position: relative;
            overflow: hidden;
            margin: 10px 0;
        }
        .loader:before {
            content: "";
            position: absolute;
            inset: 0;
            transform: translateX(-100%);
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.18), transparent);
            animation: sweep 1.2s infinite;
        }
        @keyframes sweep { to { transform: translateX(100%); } }
        @media (max-width: 780px) {
            .block-container { padding: 16px 13px 30px; }
            .hero { padding: 22px 18px; min-height: auto; }
            .brand-logo { width: min(190px, 72vw); margin-bottom: 22px; }
            .hero h1 { font-size: 27px; line-height: 1.14; }
            .hero p { font-size: 13px; }
            .card { min-height: auto; margin-bottom: 8px; }
            .value { font-size: 21px; }
            div[data-testid="stHorizontalBlock"] { gap: .65rem; }
            div[data-testid="stTabs"] button { font-size: 13px; padding-left: 10px; padding-right: 10px; }
        }
        @media (max-width: 430px) {
            .hero h1 { font-size: 23px; }
            .hero { border-radius: 10px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def sample_data(rows=900):
    rng = np.random.default_rng(42)
    data = pd.DataFrame(
        {
            "Users": rng.integers(100, 6500, rows),
            "Bandwidth": rng.integers(80, 1800, rows),
            "Latency": rng.normal(55, 28, rows).clip(5, 180),
            "SignalStrength": rng.integers(35, 100, rows),
            "PacketLoss": rng.normal(4, 3, rows).clip(0, 25),
            "Throughput": rng.normal(650, 260, rows).clip(40, 1800),
            "Jitter": rng.normal(10, 7, rows).clip(0.5, 55),
            "EdgeServerLoad": rng.integers(10, 96, rows),
            "NetworkSlice": rng.choice(["eMBB", "URLLC", "mMTC"], rows),
        }
    )
    risk = (
        data["Latency"] * 0.32
        + data["PacketLoss"] * 5
        + data["Jitter"] * 0.7
        + data["EdgeServerLoad"] * 0.38
        - data["Throughput"] * 0.025
        - data["SignalStrength"] * 0.10
    )
    data["Congestion"] = np.select(
        [risk >= 70, risk >= 45],
        ["High", "Medium"],
        default="Low",
    )
    data["Risk"] = risk.clip(0, 100).round(1)
    return data


def card(label, value):
    st.markdown(
        f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def route_graph():
    graph = nx.Graph()
    links = [
        ("Device_A", "Device_B", 24),
        ("Device_A", "Device_C", 38),
        ("Device_B", "Device_D", 31),
        ("Device_C", "Device_D", 36),
        ("Device_D", "Device_E", 18),
        ("Device_E", "Device_F", 22),
        ("Device_C", "Device_F", 64),
    ]
    graph.add_weighted_edges_from(links)
    path = nx.shortest_path(graph, "Device_A", "Device_F", weight="weight")
    return graph, path, nx.shortest_path_length(graph, "Device_A", "Device_F", weight="weight")


style()
data = sample_data()
logo = asset_uri("assets/astralink6g_white.svg")
logo_html = f'<img class="brand-logo" src="{logo}" alt="Astralink6G logo" />' if logo else '<div class="brand-logo">Astralink6G</div>'

st.markdown(
    f"""
    <section class="hero">
        {logo_html}
        <h1>Premium AI console for 6G network intelligence.</h1>
        <p>Predict congestion, explore telemetry, detect risk, and optimize communication paths from one responsive dashboard.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    card("Telemetry Records", f"{len(data):,}")
with m2:
    card("High Congestion", int((data["Congestion"] == "High").sum()))
with m3:
    card("Avg Risk", f"{data['Risk'].mean():.1f}%")
with m4:
    card("AI Status", "Active")

tab1, tab2, tab3, tab4 = st.tabs(["Prediction", "Analytics", "Risk Insights", "Smart Routing"])

with tab1:
    st.subheader("Congestion Prediction")
    scenario = st.selectbox("Scenario", ["Balanced city cell", "Metro peak load", "Ultra-low latency slice"])
    defaults = {
        "Balanced city cell": [1200, 820, 34, 82, 2.4, 610, 7.5, 42],
        "Metro peak load": [5400, 520, 112, 58, 9.8, 280, 24.0, 86],
        "Ultra-low latency slice": [900, 1450, 12, 91, 0.8, 1120, 2.4, 28],
    }[scenario]

    left, right = st.columns(2)
    with left:
        users = st.slider("Users", 100, 6500, defaults[0])
        bandwidth = st.slider("Bandwidth", 80, 1800, defaults[1])
        latency = st.slider("Latency", 5, 180, defaults[2])
        signal = st.slider("Signal Strength", 35, 100, defaults[3])
    with right:
        packet_loss = st.slider("Packet Loss", 0.0, 25.0, float(defaults[4]))
        throughput = st.slider("Throughput", 40, 1800, defaults[5])
        jitter = st.slider("Jitter", 0.5, 55.0, float(defaults[6]))
        edge_load = st.slider("Edge Server Load", 10, 95, defaults[7])

    risk = latency * 0.32 + packet_loss * 5 + jitter * 0.7 + edge_load * 0.38 - throughput * 0.025 - signal * 0.1
    risk = max(0, min(100, round(risk, 1)))
    label = "High" if risk >= 70 else "Medium" if risk >= 45 else "Low"
    st.progress(int(risk), text=f"Live Risk Index: {risk}%")

    if st.button("Run Astralink AI Prediction"):
        slot = st.empty()
        slot.markdown('<div class="loader">Scanning live network posture...</div>', unsafe_allow_html=True)
        time.sleep(0.7)
        slot.empty()
        if label == "High":
            st.error(f"Predicted Congestion: {label}")
        elif label == "Medium":
            st.warning(f"Predicted Congestion: {label}")
        else:
            st.success(f"Predicted Congestion: {label}")

with tab2:
    st.subheader("Network Analytics")
    selected_slice = st.selectbox("Network Slice", ["All", "eMBB", "URLLC", "mMTC"])
    filtered = data if selected_slice == "All" else data[data["NetworkSlice"] == selected_slice]
    window = st.slider("Telemetry Window", 100, len(filtered), min(500, len(filtered)))
    metrics = st.multiselect("Metrics", ["Latency", "PacketLoss", "Throughput", "Jitter", "EdgeServerLoad"], ["Latency", "PacketLoss", "Jitter"])
    if metrics:
        st.line_chart(filtered[metrics].head(window).reset_index(drop=True))
    st.bar_chart(filtered["Congestion"].value_counts())

with tab3:
    st.subheader("Risk Insights")
    st.dataframe(filtered.sort_values("Risk", ascending=False).head(20), width="stretch")
    st.bar_chart(pd.Series({"Packet Loss": .31, "Latency": .25, "Jitter": .18, "Edge Load": .15, "Throughput": .11}))

with tab4:
    st.subheader("Smart Routing")
    graph, path, score = route_graph()
    st.success("Best Route: " + " -> ".join(path))
    st.metric("Optimization Score", score)
    pos = nx.spring_layout(graph, seed=42)
    fig, ax = plt.subplots(figsize=(7.6, 5.2), dpi=120)
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color="#e4001b", edge_color="#202228", font_color="white", node_size=2300, font_weight="bold")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight"), ax=ax)
    ax.axis("off")
    fig.tight_layout()
    st.pyplot(fig)
