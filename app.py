from flask import Flask, render_template, request, jsonify
import requests
import time
from transbank.webpay.webpay_plus.transaction import Transaction

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
        print(f"Stock Bajo en {sucursal} (simulado SSE)")

    return jsonify({"status": "ok", "message": "Venta realizada correctamente"})

@app.route("/iniciar_pago", methods=["POST"])
def iniciar_pago():
    data = request.get_json()
    amount = data.get("amount", 1000)
    buy_order = f"ORD-{int(time.time())}"
    session_id = f"SID-{int(time.time())}"
    return_url = "http://127.0.0.1:5000/retorno_pago"

    tx = Transaction.build_for_integration(
    commerce_code="597055555532", 
    api_key="XNN9JI3S7I7LNO0EM9F9D93CN4EXJF49"
)

    response = tx.create(buy_order, session_id, amount, return_url)
    return jsonify({"url": response["url"], "token": response["token"]})

@app.route("/retorno_pago", methods=["POST"])
def retorno_pago():
    token_ws = request.form.get("token_ws")

    tx = Transaction.build_for_integration(
        commerce_code="597055555532",
        api_key="XNN9JI3S7I7LNO0EM9F9D93CN4EXJF49"
    )

    response = tx.commit(token_ws)

    if response["status"] == "AUTHORIZED":
        return f"""
        <h1 style='color: green;'>✅ Pago exitoso</h1>
        <ul>
            <li><strong>Orden:</strong> {response['buy_order']}</li>
            <li><strong>Monto:</strong> ${response['amount']}</li>
            <li><strong>Código autorización:</strong> {response['authorization_code']}</li>
            <li><strong>Fecha:</strong> {response['transaction_date']}</li>
            <li><strong>Tipo de pago:</strong> {response['payment_type_code']}</li>
            <li><strong>Cuotas:</strong> {response['installments_number']}</li>
            <li><strong>Últimos 4 dígitos:</strong> {response['card_detail']['card_number']}</li>
        </ul>
        <p style='color: gray;'>⚠️ Esto es un entorno de pruebas oficial de Transbank</p>
        """
    else:
        return f"""
        <h1 style='color: red;'>❌ Pago rechazado</h1>
        <p>Orden: {response['buy_order']}</p>
        <p>Status: {response['status']}</p>
        <p style='color: gray;'>⚠️ Esto es un entorno de pruebas oficial de Transbank</p>
        """

if __name__ == "__main__":
    app.run(debug=True)
