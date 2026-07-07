import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillDDArtisti(self):
        artisti=self._model.returnArtisti()
        artistiDD=[ft.dropdown.Option(key=artista.ArtistId, text=artista.Name) for artista in artisti]
        self._view._ddArtista.options=artistiDD
        self._view.update_page()


    def handleCreaGrafo(self, e):
        grafo=self._model.buildGraph()
        if grafo is None:
            self._view._txt_result.controls.append(ft.Text("Grafo non creato correttamente"))
        self._view._txt_result.controls.append(ft.Text("Grafo non creato correttamente"))
        nodi=self._model.getNumNodes()
        vertici=self._model.getNumEdges()

        if nodi is None:
            self._view._txt_result.controls.append(ft.Text("No nodi"))
        if vertici is None:
            self._view._txt_result.controls.append(ft.Text("No vertici"))

        self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {nodi}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero vertici: {vertici}"))

        self.fillDDArtisti()
        self._view.update_page()


    def handleStampaInfo(self,e):
        grado = self._model.artistaMax()
        peso = self._model.artistaPesi()
        archi=self._model.dieciArchi()
        if grado is None:
            self._view._txt_result.controls.append(ft.Text("No artista di grado maggiore"))
        if peso is None:
            self._view._txt_result.controls.append(ft.Text("No artista con peso maggiore"))
        if archi is None:
            self._view._txt_result.controls.append(ft.Text("No archi di peso maggiore"))

        self._view._txt_result.controls.append(ft.Text(f"Artista di grado maggiore: {grado}"))
        self._view._txt_result.controls.append(ft.Text(f"Artista di peso maggiore: {peso}"))
        self._view._txt_result.controls.append(ft.Text(f"Dieci archi di peso maggiore:"))
        for u, v, peso in archi:
            self._view._txt_result.controls.append(ft.Text(f"Arco: {str(u)} -> {str(v)}"))
        self._view.update_page()


    def handleSelezione(self, e):
        artista = self._view._ddArtista.value
        n = self._view._txtInN.value

        if artista is None:
            self._view._txt_result.controls.append(ft.Text("Attenzione! Selezionare un artista"))
            self._view.update_page()
            return
        if not n or not n.isdigit():
            self._view._txt_result.controls.append(ft.Text("Attenzione! Inserire un numero di artisti valido"))
            self._view.update_page()
            return

        bestPath, maxTot = self._model.handleRicorsione(artista, n)

        if not bestPath:
            self._view._txt_result.controls.append(ft.Text("Nessun gruppo di artisti trovato"))
        else:
            self._view._txt_result.controls.append(ft.Text("Gruppo di artisti trovato:"))
            for a in bestPath:
                self._view._txt_result.controls.append(ft.Text(f"Artista: {str(a)}"))
            self._view._txt_result.controls.append(ft.Text(f"Totale tracce: {maxTot}"))

        self._view.update_page()
