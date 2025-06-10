from flask import Flask, request, jsonify
from kivy.app import App
import threading
from kivy.clock import Clock


app = Flask(__name__)
kivy_app = None

def set_kivy_app(app_instance):
    global kivy_app
    kivy_app = app_instance

@app.route('/call_event', methods=['POST'])
def call_event():
    data = request.form
    event_type = data.get('event_type', '')
    
    if kivy_app:
        if event_type == "incoming":
            
            Clock.schedule_once(lambda dt: kivy_app.show_scrcpy())
            return jsonify({"status": "ok"}), 200     
    return jsonify({"status": "no_change"}), 200

def run_server():
    app.run(host='0.0.0.0', port=5000, threaded=True)

def start_server():
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
