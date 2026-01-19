import networkx as nx
from database.dao import DAO

class Model:

    def __init__(self):
        self.G = nx.Graph()
        self.sightings = []
        self.states = []
        self._nodes = []
        self.neighbors_map = []
        self.weights = {}

    def get_sightings(self):
        self.sightings = DAO.get_all_sightings()

    def get_states(self):
        self.states = DAO.get_all_states()

    def build_graph(self, year, shape):
        self.G.clear()
        dict_weight={}
        for p in self.states:
            self._nodes.append(p)
        self.G.add_nodes_from(self._nodes)
        self.neighbors_map = DAO.get_all_neighbors()
        self.weights = DAO.get_weight(year, shape)


        for s1, s2 in self.neighbors_map:
            if (s1, s2) not in dict_weight:
                if (s2, s1) not in dict_weight:
                    w = float(self.weights.get(s1, 0)) + float(self.weights.get(s2, 0))
                    dict_weight[(s1, s2)] = w
                else:
                    dict_weight[(s2, s1)] += float(self.weights.get(s1, 0)) + float(self.weights.get(s2, 0))
            else:
                dict_weight[(s1, s2)] += float(self.weights.get(s1, 0)) + float(self.weights.get(s2, 0))

        for (s1, s2), w in dict_weight.items():
            self.G.add_edge(s1, s2, weight=w)
