import networkx as nx
import matplotlib.pyplot as plt

# Create Network Graph
G = nx.Graph()

# Nodes
nodes = [
    "Device_A",
    "Device_B",
    "Device_C",
    "Device_D",
    "Device_E",
    "Device_F"
]

G.add_nodes_from(nodes)

# Connections with latency, packet loss, bandwidth, and congestion pressure
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
    metrics["optimization_score"] = round(score, 2)
    G.add_edge(source, target, **metrics)

# Shortest Path
path = nx.shortest_path(
    G,
    source="Device_A",
    target="Device_F",
    weight="optimization_score"
)

score = nx.shortest_path_length(
    G,
    source="Device_A",
    target="Device_F",
    weight="optimization_score"
)

print("Best Route:")
print(path)

print("\nTotal Optimization Score:")
print(round(score, 2))

# Draw Network
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color="#8ecae6",
    edge_color="#555555"
)

labels = {
    (u, v): f"L:{d['latency']} P:{d['packet_loss']} S:{d['optimization_score']}"
    for u, v, d in G.edges(data=True)
}

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=labels
)

plt.title("AI + 6G Smart Communication Network")
plt.tight_layout()
plt.savefig("reports/smart_route.png")
print("\nRouting visualization saved to reports/smart_route.png")
