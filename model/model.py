from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()
        self._risultati = []
        self._map_hub = None



    def load_map_hub(self):
        self._map_hub = DAO.get_hubs() # dizinario del tipo diz[id] = Hub

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        # TODO
        #restituisco una lista di dizionari
        primi_risultati = DAO.get_primi_risultati()
        self._risultati = self.check_risultati(primi_risultati, threshold) #lista di dizionari del tipo {'id_hub_origine': row['id_hub_origine'], #"id_hub_destinazione": row['id_hub_destinazione', #"valore_merce_tot": row['valore_merce_tot'],#"num_spedizioni": row['num_spedizioni']}
        for spedizione in self._risultati:
            self.G.add_edge(self._map_hub[spedizione["id_hub_origine"]], self._map_hub[spedizione["id_hub_destinazione"]],
                            guadagno_medio = spedizione["guadagno_medio"])


        #print(f"{len(self.G.edges)} = numero di edges")
        #print(f"{len(self.G.nodes)} = numero di nodes")

    def check_risultati(self, primi_risultati, c):

        # cerco di ottenere i dati corretti raggruppando le spedizioni tra 2 hub
        # indipendentemente dall'hub di apartenza e da quello di arrivo

        fl_parziale = dict()
        for spedizione in primi_risultati:
            origine = spedizione["id_hub_origine"]
            destinazione = spedizione["id_hub_destinazione"]
            chiave = tuple(sorted((origine, destinazione)))

            if chiave not in fl_parziale:

                fl_parziale[chiave] = {"valore_merce_tot": spedizione["valore_merce_tot"],
                                  "num_spedizioni": spedizione["num_spedizioni"]}

            else:

                fl_parziale[chiave]["valore_merce_tot"] += spedizione["valore_merce_tot"]
                fl_parziale[chiave]["num_spedizioni"] += spedizione["num_spedizioni"]

        result = []
        for chiave in fl_parziale:
            result.append({"id_hub_origine": chiave[0], "id_hub_destinazione": chiave[1],
                           "valore_merce_tot": fl_parziale[chiave]["valore_merce_tot"],
                           "num_spedizioni": fl_parziale[chiave]["num_spedizioni"]})


        rt = []
        for diz in result:
            diz["guadagno_medio"] = diz["valore_merce_tot"] / diz["num_spedizioni"]
            if diz["guadagno_medio"] >= c:
                rt.append(diz)

        return rt

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        # TODO
        #num = len(self.G.edges)
        #return num
        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        # TODO
        #num = len(self.G.nodes)
        #return num
        return len(self._map_hub)

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        # TODO
        l = []
        for edge in self.G.edges:
            l.append([edge[0].nome, edge[0].citta, edge[1].nome, edge[1].citta, self.G[edge[0]][edge[1]]["guadagno_medio"]])
        return l