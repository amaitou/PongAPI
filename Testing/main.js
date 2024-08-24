import { renderNavbar } from './components/navbar.js';
import { renderHome } from './components/home.js';
import { rendercontent } from './components/content.js';
import { renderSignUp } from './components/signup.js';
import { renderSignIn } from './components/signin.js';
import { renderChat } from './components/chat.js';
import { renderSettings } from './components/setting.js';
import { renderWhite } from './components/white.js';

function navigate() 
{
    const route = window.location.pathname
    console.log(route);

    if (route === '/') 
        renderSignUp();
    else if (route === '/index.html') 
        renderSignUp();
    else if (route === '/signin') 
        renderSignIn();
    else if (route === '/signup') 
        renderSignUp();
    else if (route === '/setting') 
        renderSettings();
    else if (route === '/profile') 
    {

        renderNavbar();
        renderHome();
        rendercontent();
    }
    else if (route === '/chat') 
        renderChat();
    else 
        renderWhite();
}


window.addEventListener('hashchange', navigate);
navigate();


const element = document.getElementById("solix");
const chatBox = document.getElementById('chat-box');
element.addEventListener("click", myFunction);

function myFunction() {
    chatBox.innerHTML = "";
    addMessage('Bonjour ! Comment vas-tu ?', 'other');
    addMessage('Très bien, merci. Et toi ?', 'user');
    addMessage('Je vais aussi très bien, merci.', 'other');
}

function addMessage(message, sender) 
{
  const messageElement = document.createElement('p');
  
  if (sender === 'user') 
  {
      messageElement.classList.add('message-right');
  } 
  else 
  {
      messageElement.classList.add('message-left');
  }
  
  messageElement.textContent = message;
  chatBox.appendChild(messageElement);
}


// function new_message()
// {
//     const messageInput = document.getElementById('input-box');
//     const message = messageInput.value;
    
//     if (message.trim()!== '') 
//     {
//       addMessage(message, 'user');
//       messageInput.value = '';
//     }
// }


// function change_box()
// {
//   const chatBox = document.getElementById('chat-box');
//   chatBox.innerHTML = ""; // Remove the element from the DOM
// }


// ------------------------------SignUp--------------------------------------------------------------------------

document.getElementById('signUpForm').addEventListener('submit', function(e) 
{
    e.preventDefault();

    const formData = 
    {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        RepeatPassword: document.getElementById('Repeat Password').value,
        avatar: document.getElementById('avatar').value
    };
    console.log(formData);
    fetch('http://localhost:8000/registre/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('authToken', data.token);
            alert('Registration successful!');
        } else {
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while registering.');
    });
});



// ------------------------------SignIn----------------------------------------------------------------------------

document.getElementById('signInForm').addEventListener('submit', function(e) 
{
    e.preventDefault();

    const loginData = 
    {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };
    
    console.log(loginData);
    console.log('reda');
    fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('authToken', data.token);
            alert('Login successful!');
        } else {
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while logging in.');
    });
});