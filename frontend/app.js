async function cargarModulos(){
    const respuesta = await fetch("http://127.0.0.1:8000/python/modulos");
    const datos = await respuesta.json();

    const contenedor = document.getElementById("modulos");
    contenedor.innerHTML = "";

    datos.forEach(modulo => {
        contenedor.innerHTML += `
            <div class="card">
                <h3>${modulo.titulo}</h3>
                <p>XP: ${modulo.xp}</p>
            </div>
        `;
    });
}