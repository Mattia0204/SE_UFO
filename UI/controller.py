import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._model.get_sightings()
        sighting_list = self._model.sightings
        lista_years=[]
        lista_shape=[]
        for s in sighting_list:
            if s.s_datetime.year not in lista_years:
                lista_years.append(s.s_datetime.year)
            if s.shape not in lista_shape:
                lista_shape.append(s.shape)
        self._view.dd_year.options = [ft.dropdown.Option(str(y)) for y in lista_years]
        self._view.dd_shape.options = [ft.dropdown.Option(str(sh)) for sh in lista_shape]
        return

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        try:
            year = int(self._view.dd_year.value)
        except Exception:
            self._view.show_alert("Anno Invalido")
            return
        shape = self._view.dd_shape.value
        self._model.build_graph(year, shape)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {len(self._model.G.nodes)} Numero di archi: {len(self._model.G.edges)}"))
        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
