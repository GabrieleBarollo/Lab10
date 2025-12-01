import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab10"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Rete Logistica", size=38, weight=ft.FontWeight.BOLD)

        # Guadagno Medio Minimo
        self.guadagno_medio_minimo = ft.TextField(label="Guadagno medio minimo (€)", width=300)
        self.pulsante_analizza = ft.ElevatedButton(text="Analizza Hub",
                                              on_click=self.controller.mostra_tratte)

        # Visualizzazione mediante ListView
        self.lista_visualizzazione = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            # Sezione 2
            ft.Row([self.guadagno_medio_minimo, self.pulsante_analizza], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Divider(),

            # Sezione 3
            ft.Container(
                content=self.lista_visualizzazione,
                height=430,
                border=ft.border.all(1, ft.Colors.BLACK),
                padding=10,
            )
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
