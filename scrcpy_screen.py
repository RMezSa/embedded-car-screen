import subprocess
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.app import App


class ScrcpyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scrcpy_proc = None
        
        layout = BoxLayout(orientation='vertical')
        
        exit_btn = Button(
            text='Salir de Scrcpy',
            size_hint=(1, 0.1),
            background_color=(0.247, 0.408, 0.576, 1)
        )
        exit_btn.bind(on_press=self.volver_main)
        layout.add_widget(exit_btn)
        
        self.add_widget(layout)

    def volver_main(self, instance):
        app = App.get_running_app()
        app.show_main()

    def on_enter(self):
        try:
            subprocess.run(["adb", "start-server"], check=True, timeout=5)
            
            self.scrcpy_proc = subprocess.Popen([
                "/home/roberd/apps/scrcpy/scrcpy",
                "--no-audio",
                "--max-size", "1024",
                "--video-bit-rate", "2M",  
                "--max-fps", "30",
                "--always-on-top"
            ])

        except subprocess.TimeoutExpired:
            print("error timeout")
        except subprocess.CalledProcessError as e:
            print(f"ADB error")
        except Exception as e:
            print(f"ERROR: {e}")

    def on_leave(self):
        if self.scrcpy_proc:
            try:
                self.scrcpy_proc.terminate()
                self.scrcpy_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.scrcpy_proc.kill()
            finally:
                self.scrcpy_proc = None