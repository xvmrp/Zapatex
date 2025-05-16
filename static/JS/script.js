function calcular() {
    const cantidad = parseInt(document.getElementById("cantidad").value);
    const sucursal = document.getElementById("selectSucursal").value;

    const precio = getPrecioSucursal(sucursal);
    const total_clp = precio * cantidad;

    fetch("/calcular_usd", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ total_clp: total_clp })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("resultados").innerText = `Total CLP: ${total_clp} | Total USD: ${data.total_usd}`;
    });
}

function realizarVenta() {
    const cantidad = parseInt(document.getElementById("cantidad").value);
    const sucursal = document.getElementById("selectSucursal").value;

    fetch("/realizar_venta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sucursal: sucursal, cantidad: cantidad })
    })
    .then(res => res.json())
    .then(data => alert(data.message))
    .catch(err => alert("Error en la venta"));
}

function getPrecioSucursal(nombre) {
    const precios = {
        "Sucursal 1": 333,
        "Sucursal 2": 222,
        "Sucursal 3": 1111
    };
    return precios[nombre];
}
