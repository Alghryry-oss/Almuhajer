import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
from pathlib import Path

class Visualizer:
    def __init__(self, graph):
        self.G = graph
    
    def plot_static(self, filename='data/network.png'):
        plt.figure(figsize=(12,8))
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=8)
        plt.savefig(filename, dpi=300)
        plt.close()
    
    def plot_interactive(self, filename='data/network.html'):
        pos = nx.spring_layout(self.G)
        edge_trace = []
        for u, v in self.G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_trace.append(go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                                         mode='lines', line=dict(width=0.5, color='#888'),
                                         hoverinfo='none'))
        
        node_x = [pos[n][0] for n in self.G.nodes]
        node_y = [pos[n][1] for n in self.G.nodes]
        node_text = [f"ID: {n}<br>" + "<br>".join([f"{k}: {v}" for k,v in self.G.nodes[n].items() if k not in ['raw']]) for n in self.G.nodes]
        
        node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text',
                                text=node_text, textposition="top center",
                                hoverinfo='text',
                                marker=dict(size=10, color='lightblue', line=dict(width=2)))
        
        fig = go.Figure(data=edge_trace + [node_trace],
                        layout=go.Layout(title='OSINT Network', showlegend=False))
        fig.write_html(filename)