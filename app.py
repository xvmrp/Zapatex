from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Simulamos una base de datos
casa_matriz = {"cantidad": 10, "precio": 999}
sucursales = {
    "Sucursal 1": {"cantidad": 31, "precio": 333},
    "Sucursal 2": {"cantidad": 23, "precio": 222},
    "Sucursal 3": {"cantidad": 100, "precio": 1111}
}

@app.route("/")
def venta():
    return render_template("venta.html", casa_matriz=casa_matriz, sucursales=sucursales)

@app.route("/calcular_usd", methods=["POST"])
def calcular_usd():
    data = request.get_json()
    total_clp = data["total_clp"]
    usd_api = requests.get("https://api.exchangerate-api.com/v4/latest/CLP").json()
    tasa = usd_api["rates"]["USD"]
    total_usd = round(total_clp * tasa, 2)
    return jsonify({"total_usd": total_usd})

@app.route("/realizar_venta", methods=["POST"])
def realizar_venta():
    data = request.get_json()
    sucursal = data["sucursal"]
    cantidad = data["cantidad"]
    
    if sucursales[sucursal]["cantidad"] < cantidad:
        return jsonify({"status": "error", "message": f"Stock insuficiente en {sucursal}"}), 400

    sucursales[sucursal]["cantidad"] -= cantidad

    if sucursales[sucursal]["cantidad"] == 0:
        # Aquí se simula el envío del SSE (real implementarlo con `flask-sse` o `flask-socketio`)
        print(f"Stock Bajo en {sucursal}")

    return jsonify({"status": "ok", "message": "Venta realizada correctamente"})

if __name__ == "__main__":
    app.run(debug=True)
