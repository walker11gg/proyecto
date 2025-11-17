document.getElementById("formLogin").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const respuesta = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await respuesta.json();

    const mensaje = document.getElementById("mensaje");

    if (data.success) {
        mensaje.style.color = "green";
        mensaje.textContent = "Bienvenido (" + data.rol + ")";
        
        // ejemplo: redirigir después del login
        // window.location.href = "/panel";
    } else {
        mensaje.style.color = "red";
        mensaje.textContent = data.mensaje;
    }
});