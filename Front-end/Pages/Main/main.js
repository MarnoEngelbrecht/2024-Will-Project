content = document.getElementById('content');
function navigateTo(href) {
    if (href != null ){
        fetch(href)
        .then(response => response.text())
        .then(html => {
            content.innerHTML = html;
        })
        .then(() => {
            // Dynamically load the script for listings
            if (href === '../Listings-page/listings-page.html') {
                loadListingsPage()
            }
            else if (href === '../Landing-page/landing-page.html') {
                // loadLandingPage()
            }
            else if (href === '../Login-page/login-page.html') {
                // loadLandingPage()
            }
        });
    }
}

document.querySelectorAll('nav a, button[data-href], a').forEach(element => {
    element.addEventListener('click', function(event) {
        event.preventDefault();
        const href = element.tagName.toLowerCase() === 'a' ? element.getAttribute('href') : element.getAttribute('data-href');
        navigateTo(href);
    });
});

function loadListingsPage() {
    const script = document.createElement('script');
    script.src = '../Listings-page/listings-page.js';
    script.onload = () => {
        fetchProperties();
    };
    content.appendChild(script);
}

// function loadLoginPage() {
//     const script = document.createElement('script');
//     script.src = '../Login-page/login-page.js';
//     script.onload = () => {
//         fetchProperties();
//     };
//     content.appendChild(script);
// }

const openLoginDialogButton = document.getElementById('open-login-dialog');
const closeLoginDialogButton = document.getElementById('close-login-dialog');
const closeCreateDialogButton = document.getElementById('close-create-dialog');
const closeDialogSubmitButton = document.getElementById('close-dialog-submit');
const closeDialogCreateAccountButton = document.getElementById('goToCreateDialog');
const closeDialogLoginButton = document.getElementById('goToLoginDialog');
const loginDialog = document.getElementById('login-dialog');
const createDialog = document.getElementById('create-dialog');

document.addEventListener('DOMContentLoaded', function() {
    navigateTo('../Landing-page/landing-page.html');

    openLoginDialogButton.addEventListener('click', function() {
        loginDialog.showModal();
    });

    closeLoginDialogButton.addEventListener('click', function() {
        loginDialog.close();
    });

    closeCreateDialogButton.addEventListener('click', function() {
        createDialog.close();
    });

    closeDialogSubmitButton.addEventListener('click', function() {
        loginDialog.close();
    });

    closeDialogCreateAccountButton.addEventListener('click', function() {
        loginDialog.close();
        createDialog.showModal();
    });

    closeDialogLoginButton.addEventListener('click', function() {
        openLoginDialog();
    });
});

function openLoginDialog(){
    createDialog.close();
    loginDialog.showModal();    
}

const apiUrl = 'http://127.0.0.1:5000/user';

async function onLoginSubmit(e){
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const response = await fetch(apiUrl+'/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"Email" : username, "Password" : password }),
        credentials: 'include'
    });
    const data = await response.json();
    if (response.status === 200) {
        // Redirect to a new HTML page
        navigateTo('../Landing-page/landing-page.html');
    }
    // insert toast
}

async function onRegisterSubmit(e){
    e.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const response = await fetch(apiUrl+'/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"Username" : username, "Password" : password, "Email" : email})
    }).then(response=>{
        if (response.status === 201){
            openLoginDialog()
            const data = response.json();
        }
    }).catch(error=>{
        console.warn(error);
    })
    // insert toast
}
