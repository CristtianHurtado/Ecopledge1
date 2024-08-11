document.getElementById('recycling-point-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const materials_accepted = document.getElementById('materials_accepted').value;

    // Geocodificar la dirección
    console.log('Geocodificando la dirección:', address);
    fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)},Bogotá,Colombia&format=json`)
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta de la API de Nominatim:', data);
            if (data.length > 0) {
                const latitude = data[0].lat;
                const longitude = data[0].lon;

                fetch('http://127.0.0.1:5000/api/recycling-points', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: name,
                        address: address,
                        latitude: parseFloat(latitude),
                        longitude: parseFloat(longitude),
                        materials_accepted: materials_accepted
                    })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    document.getElementById('recycling-point-form').reset();
                    loadRecyclingPoints();
                })
                .catch(error => console.error('Error al agregar punto de reciclaje:', error));
            } else {
                alert('No se encontraron coordenadas para la dirección proporcionada. Por favor, asegúrate de que la dirección sea correcta y específica.');
            }
        })
        .catch(error => console.error('Error al geocodificar la dirección:', error));
});

function loadRecyclingPoints() {
    fetch('http://127.0.0.1:5000/api/recycling-points')
        .then(response => response.json())
        .then(data => {
            const recyclingPointsList = document.getElementById('recycling-points-list');
            recyclingPointsList.innerHTML = ''; // Limpiar la lista antes de agregar puntos de reciclaje nuevos

            data.forEach(point => {
                const li = document.createElement('li');
                li.textContent = `${point.name} - ${point.address}`;
                recyclingPointsList.appendChild(li);
            });
        })
        .catch(error => console.error('Error al cargar puntos de reciclaje:', error));
}

function deleteRecyclingPoint(id) {
    fetch(`http://127.0.0.1:5000/api/recycling-points/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadRecyclingPoints();
    })
    .catch(error => console.error('Error al eliminar el punto de reciclaje:', error));
}

document.addEventListener('DOMContentLoaded', loadRecyclingPoints);
