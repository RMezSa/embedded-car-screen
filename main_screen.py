from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.clock import Clock
from pathlib import Path


from datetime import datetime

Window.size = (400, 700)


dias = {
    'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
    'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}

meses = {
    'January': 'enero', 'February': 'febrero', 'March': 'marzo',
    'April': 'abril', 'May': 'mayo', 'June': 'junio', 'July': 'julio',
    'August': 'agosto', 'September': 'septiembre', 'October': 'octubre',
    'November': 'noviembre', 'December': 'diciembre'
}

class ImageButton(ButtonBehavior, BoxLayout):
    def __init__(self, image_path, text, screen_name, callback, **kwargs):
        super().__init__(orientation='vertical', spacing=5, padding=5,
                         size_hint=(None, None), width=250, height=300, **kwargs)
        self.screen_name = screen_name
        self.callback = callback
        self.image = Image(source=image_path, size_hint=(1, 0.75), allow_stretch=True)
        self.label = Label(text=text, font_size=30, size_hint=(1, 0.25),
                           halign='center', valign='middle')
        self.label.bind(size=self._update_text_align)
        self.add_widget(self.image)
        self.add_widget(self.label)

    def _update_text_align(self, instance, value):
        self.label.text_size = value

    def on_press(self):
        self.callback(self.screen_name)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.datetime_label = Label(
            text="",
            font_size=40,
            bold=True,
            size_hint=(1, 0.15),
            halign='center',
            valign='middle',
            color=(0.8, 0.8, 0.8, 1) 
        )
        self.datetime_label.bind(size=self._actualizar_fecha_align)
        self.layout.add_widget(self.datetime_label)

        anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.85))
        grid = GridLayout(cols=3, spacing=20, size_hint=(None, None))
        grid.bind(minimum_size=grid.setter('size'))

        
        BASE_DIR = Path(__file__).resolve().parent
        ASSETS_PATH = BASE_DIR / 'assets'
        buttons_info = [
            ('SPOTIFY', 'spotify', str(ASSETS_PATH / 'spotify.png')),
            ('REVERSA', 'camara', str(ASSETS_PATH / 'park.png')),
            ('MAPS', 'scrcpy', str(ASSETS_PATH / 'maps.png'))
        ]

        for text, screen_name, image_path in buttons_info:
            img_btn = ImageButton(image_path=image_path, text=text,
                                  screen_name=screen_name, callback=self.change_screen)
            grid.add_widget(img_btn)

        anchor.add_widget(grid)
        self.layout.add_widget(anchor)

        self.add_widget(self.layout)

        # Reloj en vivo
        Clock.schedule_interval(self.actualizar_fecha, 1)
        self.actualizar_fecha(0)

    def _actualizar_fecha_align(self, instance, value):
        self.datetime_label.text_size = value

    def actualizar_fecha(self, dt):
        now = datetime.now()
        dia = dias[now.strftime('%A')]
        mes = meses[now.strftime('%B')]
        fecha = f'{dia} {now.strftime("%d")} de {mes}, {now.strftime("%H:%M:%S")}'
        self.datetime_label.text = fecha

    def change_screen(self, screen_name):
        print(f"Cambiando a: {screen_name}")
        if self.manager.has_screen(screen_name):
            self.manager.current = screen_name
        else:
            print(f"Error: pantalla '{screen_name}' no existe.")
