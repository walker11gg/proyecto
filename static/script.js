const lista = document.getElementById("lista");
const formulario = document.getElementById("formulario");

// Cargar los eventos al inicio
async function cargarEventos() {
  const respuesta = await fetch("/api/eventos");
  const eventos = await respuesta.json();
  lista.innerHTML = "";

  if (eventos.length === 0) {
    lista.innerHTML = "<li>No hay eventos registrados.</li>";
    return;
  }

  eventos.forEach(evento => {
    const li = document.createElement("li");
    li.textContent = `${evento.id}. ${evento.tipo} - ${evento.fecha} (Cliente: ${evento.cliente})`;
    lista.appendChild(li);
  });
}

// Registrar un nuevo evento
formulario.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nuevoEvento = {
    cliente: document.getElementById("cliente").value,
    tipo: document.getElementById("tipo").value,
    fecha: document.getElementById("fecha").value
  };

  await fetch("/api/eventos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevoEvento)
  });

  formulario.reset();
  cargarEventos();
});

// Ejecutar al inicio
cargarEventos();