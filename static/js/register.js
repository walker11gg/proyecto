document.getElementById("formRegistro").addEventListener("submit", async function(e){
    e.preventDefault();

    const email = document.getElementById("email_reg").value;
    const password = document.getElementById("pass_reg").value;
    const mensaje = document.getElementById("mensaje_reg");

    mensaje.textContent = "Registrando...";

    const resp = await fetch("/api/registrar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    });

    const data = await resp.json();

    if (data.success) {
        mensaje.style.color = "green";
        mensaje.textContent = data.message;
    } else {
        mensaje.style.color = "red";
        mensaje.textContent = data.message;
    }
});