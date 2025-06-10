from gpiozero import RotaryEncoder
from signal import pause
import subprocess

encoder = RotaryEncoder(a=17, b=18, max_steps=100) 
vol_actual = 50

def set_vol(vol):
    vol = max(0, min(100, vol))  # Limita entre 0 y 100
    subprocess.call(f"{vol}%", shell=True)
    print(f"Volumen: {vol}%")

def actualizar_vol():
    global vol_actual
    vol_actual = max(0, min(100, encoder.steps))
    set_vol(vol_actual)

encoder.steps = vol_actual  
encoder.when_rotated = actualizar_vol

pause()
