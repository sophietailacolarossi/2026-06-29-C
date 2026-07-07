import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._nodes=[]
        self._edges=[]
        self._idMap={}


    def buildGraph(self):
        self._nodes=DAO.getAllNodes()
        self._graph.add_nodes_from(self._nodes)
        for node in self._nodes:
            self._idMap[node.ArtistId]=node
        self.addEdges()
        return self._graph

    def addEdges(self):
        archi=DAO.getAllEdges()
        for u_id, v_id, peso in archi:
            if u_id in self._idMap.keys() and v_id in self._idMap.keys():
                u=self._idMap[u_id]
                v=self._idMap[v_id]
                self._graph.add_edge(u, v, weight=peso)
                self._edges.append((u, v))

    def getNumEdges(self):
        return len(self._edges)

    def getNumNodes(self):
        return len(self._nodes)

    def artistaMax(self):
        artisti_grado=[]
        for node in self._nodes:
            grado=self._graph.degree(node)
            artisti_grado.append((node, grado))
        list=sorted(artisti_grado, key=lambda x: x[1], reverse=True)
        return list[0]

    def artistaPesi(self):
        artisti_peso = []
        for node in self._nodes:
            pesi = sum(peso for u, v, peso in self._graph.edges(node, data="weight"))
            artisti_peso.append((node, pesi))
        list = sorted(artisti_peso, key=lambda x: x[1], reverse=True)
        return list[0]
    def dieciArchi(self):
        archi_peso=[]
        ultimo_peso=0
        for u, v, peso in self._edges:
            if peso>ultimo_peso:
                archi_peso.append((u, v, peso))
                ultimo_peso=peso
        archi_peso_ordinati=sorted(archi_peso, key=lambda x: (-x[2], x[0].Name, x[1].Name)) #!!!IMPORTANE, MI SERVE PER ORDINARE ANCHE IN BASE AD ALTRI ATTRIBUTI, IN CASO DI PARITA'
        return archi_peso_ordinati[0:10]

    def returnArtisti(self):
        return self._graph.nodes()

    def handleRicorsione(self, artista, N):
        self._bestPath=[]
        self._maxTot=0
        a_id=int(artista)
        n=int(N)
        primo=self._idMap[a_id]
        visitati=[primo]
        cammino_attuale=[primo]
        totale_attuale=0
        vicini=[set(self._graph.neighbors(primo))]
        self.ricorsione(n, visitati, cammino_attuale, totale_attuale, vicini)
        return self._bestPath, self._maxTot

    def ricorsione(self, n, visitati, cammino_attuale, totale_attuale, vicini):
        if len(cammino_attuale)==n:
            if totale_attuale>self._maxTot:
                self._maxTot=totale_attuale
                self._bestPath=copy.deepcopy(cammino_attuale)
            return

        for node in self._nodes:
            e_vicino = any(node in insieme for insieme in vicini)
            if e_vicino and node not in visitati:
                if self.isValido(node, visitati):
                    vicini.append(set(self._graph.neighbors(node)))
                    visitati.append(node)
                    cammino_attuale.append(node)
                    self.ricorsione(n, visitati, cammino_attuale, totale_attuale+len(node.tracce), vicini)
                    vicini.pop()
                    visitati.pop()
                    cammino_attuale.pop()

    def isValido(self, node, visitati):
        valido=False
        for v in visitati:
            if self._graph.has_edge(node, v):
                peso = self._graph[node][v]['weight']
                if peso>1:
                    valido=True
        return valido















