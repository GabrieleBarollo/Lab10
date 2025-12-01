from model.model import Model

model = Model()
model.load_map_hub()
model.costruisci_grafo(300)
model.get_all_edges()