import networkx as nx
from community import community_louvain  # python-louvain

class GraphAnalyzer:
    def __init__(self, entities, relations):
        self.G = nx.Graph()
        for eid, attrs in entities.items():
            self.G.add_node(eid, **attrs)
        for u, v, rel in relations:
            self.G.add_edge(u, v, type=rel)
    
    def compute_centrality(self):
        degree = nx.degree_centrality(self.G)
        betweenness = nx.betweenness_centrality(self.G)
        nx.set_node_attributes(self.G, degree, 'degree')
        nx.set_node_attributes(self.G, betweenness, 'betweenness')
        return degree, betweenness
    
    def detect_communities(self):
        communities = community_louvain.best_partition(self.G)
        nx.set_node_attributes(self.G, communities, 'community')
        return communities
    
    def find_suspicious_clusters(self):
        # Heuristic: clusters with many private/high-centrality nodes
        suspicious = []
        for node in self.G.nodes:
            if self.G.nodes[node].get('private', False) and self.G.nodes[node].get('degree', 0) > 0.5:
                suspicious.append(node)
        return suspicious