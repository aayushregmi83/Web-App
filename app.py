from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {
    'admin': {'password': 'adminpass', 'role': 'admin'},
    'client': {'password': 'clientpass', 'role': 'client'}
}

sensor_data = {
    "temperature": round(random.uniform(20, 30), 2),
    "humidity": round(random.uniform(40, 60), 2),
    "gas": "Normal"
}

device_states = {
    "light": False,
    "fan": False
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    user = users.get(username)

    if user and user['password'] == password and user['role'] == role:
        session['username'] = username
        session['role'] = user['role']
        return redirect(url_for('dashboard'))

    return render_template('login.html', error="Invalid credentials")

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/control', methods=['POST'])
def control_device():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    device = data.get('device')
    state = data.get('state')

    if device not in device_states:
        return jsonify({"error": "Invalid device"}), 400

    device_states[device] = state
    return jsonify({"device": device, "state": state})

@app.route('/sensor-data', methods=['GET'])
def fetch_sensor_data():
    sensor_data["temperature"] = round(random.uniform(20, 30), 2)
    sensor_data["humidity"] = round(random.uniform(40, 60), 2)
    sensor_data["gas"] = "Alert" if random.random() > 0.8 else "Normal"
    return jsonify(sensor_data)

@app.route('/analytics-data', methods=['GET'])
def fetch_analytics_data():
    analytics = {
        "power_consumption": round(random.uniform(10, 50), 2),
        "water_usage": round(random.uniform(100, 500), 2),
        "device_usage": {"light": device_states["light"], "fan": device_states["fan"]}
    }
    return jsonify(analytics)

if __name__ == '__main__':
    app.run(debug=True)
