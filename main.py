from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from spotify_screen import SpotifyScreen
from main_screen import MainScreen
from camera_screen import CameraReverseScreen
from scrcpy_screen import ScrcpyScreen

from flask_server import set_kivy_app, start_server


from kivy.config import Config
from kivy.clock import Clock

Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'fullscreen', '0')

class MultiModuleApp(App):
    def build(self):
        self.sm = ScreenManager()
        
        # Añadir pantallas
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(SpotifyScreen(name='spotify'))
        self.sm.add_widget(CameraReverseScreen(name='camara'))
        self.sm.add_widget(ScrcpyScreen(name='scrcpy'))

        # Pasar referencia de app a Flask
        set_kivy_app(self)
        start_server()

        return self.sm

    def change_screen(self, screen_name):
        if self.sm.has_screen(screen_name):
            Clock.schedule_once(lambda dt: setattr(self.sm, 'current', screen_name))
        else:
            print(f"Pantalla '{screen_name}' no encontrada")


    def show_main(self):
        def _show_main(dt):
            if self.sm.has_screen("main"):
                self.sm.current = 'main'
            else:
                print("La pantalla 'main' no está registrada")
    
        Clock.schedule_once(_show_main)

    def show_scrcpy(self):
        def _show_scrcpy(dt):
            if self.sm.has_screen("scrcpy"):
                self.sm.current = 'scrcpy'
            else:
                print("La pantalla 'scrcpy' no está registrada")
        
        Clock.schedule_once(_show_scrcpy)


if __name__ == '__main__':
    MultiModuleApp().run()