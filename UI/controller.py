import flet as ft

from UI.alert import AlertManager
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        # TODO
        try:
            costo = int(self._view.guadagno_medio_minimo.value)
            if costo <= 0:
                alert = AlertManager(self._view.page)
                alert.show_alert("Inserisci un valore adatto")
            else:
                self._model.load_map_hub()
                self._model.costruisci_grafo(costo)
                numero_edges = self._model.get_num_edges()
                numero_nodes = self._model.get_num_nodes()
                self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di tratte: {numero_edges}"))
                self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di nodi: {numero_nodes}"))
                lista_edges = self._model.get_all_edges()
                i = 1
                for info in lista_edges:
                    self._view.lista_visualizzazione.controls.append(ft.Text(f"{i}) {info[0]}: {info[1]} --> {info[2]}: {info[3]} || guadagno medio per spedizione: {info[4]}"))
                    i += 1
                self._view.update()

        except ValueError:
            alert = AlertManager(self._view.page)
            alert.show_alert("Inserisci un valore adatto")