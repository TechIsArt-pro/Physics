from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default values for charges and distance
    charge1 = 1  # Coulombs
    charge2 = -1 # Coulombs
    distance = 2  # Distance between charges in meters

    # If we get values from the user, update accordingly
    if request.method == 'POST':
        charge1 = float(request.form['charge1'])
        charge2 = float(request.form['charge2'])
        distance = float(request.form['distance'])
    
    # Calculate positions of the charges (placed on the x-axis at the specified distance)
    x1 = -distance / 2
    x2 = distance / 2
    y1 = y2 = 0

    # Electric field calculation (simple version using Coulomb's Law)
    k = 8.99e9  # Coulomb constant
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)

    Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)
    for (xq, yq, q) in [(x1, y1, charge1), (x2, y2, charge2)]:
        dx = X - xq
        dy = Y - yq
        r_squared = dx**2 + dy**2
        r_squared[r_squared == 0] = 1e-20
        r = np.sqrt(r_squared)
        Ex += k * q * dx / r_squared**1.5
        Ey += k * q * dy / r_squared**1.5

    # Save plot to memory and encode it to base64 for rendering in HTML
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.streamplot(X, Y, Ex, Ey, color=np.sqrt(Ex**2 + Ey**2), cmap='coolwarm')
    ax.scatter(x1, y1, c='red', s=100, edgecolors='black')
    ax.scatter(x2, y2, c='blue', s=100, edgecolors='black')
    ax.set_title('Ηλεκτρικό πεδίο με δύο σημειακά φορτία')
    ax.set_xlabel('Απόσταση')
    ax.set_ylabel('')
    ax.set_aspect('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return render_template('index.html', image_data=encoded, charge1=charge1, charge2=charge2, distance=distance)

@app.route('/update', methods=['POST'])
def update():
    # Handle slider changes and return updated image
    charge1 = float(request.form['charge1'])
    charge2 = float(request.form['charge2'])
    distance = float(request.form['distance'])
    
    # Calculate positions of the charges (placed on the x-axis at the specified distance)
    x1 = -distance / 2
    x2 = distance / 2
    y1 = y2 = 0

    # Electric field calculation (simple version using Coulomb's Law)
    k = 8.99e9  # Coulomb constant
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)

    Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)
    for (xq, yq, q) in [(x1, y1, charge1), (x2, y2, charge2)]:
        dx = X - xq
        dy = Y - yq
        r_squared = dx**2 + dy**2
        r_squared[r_squared == 0] = 1e-20
        r = np.sqrt(r_squared)
        Ex += k * q * dx / r_squared**1.5
        Ey += k * q * dy / r_squared**1.5

    # Save plot to memory and encode it to base64 for rendering in HTML
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.streamplot(X, Y, Ex, Ey, color=np.sqrt(Ex**2 + Ey**2), cmap='coolwarm')
    ax.scatter(x1, y1, c='red', s=100, edgecolors='black')
    ax.scatter(x2, y2, c='blue', s=100, edgecolors='black')
    ax.set_title('Ηλεκτρικό πεδίο με δύο σημειακά φορτία')
    ax.set_xlabel('Απόσταση')
    ax.set_ylabel('')
    ax.set_aspect('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return jsonify(image_data=encoded)

if __name__ == '__main__':
    app.run(debug=True)