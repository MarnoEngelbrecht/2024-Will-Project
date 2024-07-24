//Api Host
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
        window.location.href = '../Landing-page/landing-page.html';
    }
    console.log(response)

}

// document.getElementById('loginForm').onsubmit = async function(e) {
//     e.preventDefault();
//     const username = document.getElementById('loginUsername').value;
//     const password = document.getElementById('loginPassword').value;
//     const response = await fetch(apiUrl+'/login', {
//         method: 'GET',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ username, password })
//     });
//     const data = await response.json();
//     alert(data.message);
// };