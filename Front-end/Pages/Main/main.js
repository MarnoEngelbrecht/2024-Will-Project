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

function loadLoginPage() {
    const script = document.createElement('script');
    script.src = '../Login-page/login-page.js';
    script.onload = () => {
        fetchProperties();
    };
    content.appendChild(script);
}

document.addEventListener('DOMContentLoaded', function() {
    navigateTo('../Landing-page/landing-page.html');
    const openDialogButton = document.getElementById('open-dialog');
    const closeDialogButton = document.getElementById('close-dialog');
    const closeDialogSaveButton = document.getElementById('close-dialog-save');
    const dialog = document.getElementById('login-dialog');

    // Open the dialog when the "Open Dialog" button is clicked
    openDialogButton.addEventListener('click', function() {
        dialog.showModal();
    });

    closeDialogButton.addEventListener('click', function() {
        dialog.close();
    });

    closeDialogSaveButton.addEventListener('click', function() {
        dialog.close();
    });

    dialog.addEventListener('click', function(event) {
        if (event.target === dialog) {
            dialog.close();
        }
    });
});

const apiUrl = 'http://127.0.0.1:5000/user';

async function onSubmit(e){
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
    console.log(response)

}