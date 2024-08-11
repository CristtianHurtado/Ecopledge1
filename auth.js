document.getElementById('login-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch('http://127.0.0.1:5000/api/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          username: username,
          password: password
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          alert(data.message); // Mostrar el mensaje recibido del servidor
      } else {
          alert("Error desconocido durante el inicio de sesión.");
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert("Error durante el inicio de sesión.");
  });
});

document.getElementById('register-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch('http://127.0.0.1:5000/api/auth/register', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          username: username,
          password: password
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          alert(data.message); // Mostrar el mensaje recibido del servidor
      } else {
          alert("Error desconocido durante el registro.");
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert("Error durante el registro.");
  });
});
