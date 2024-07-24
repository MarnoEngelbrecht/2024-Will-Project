const apiUrl = 'http://127.0.0.1:5500/users';

async function onSubmit(e){
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const response = await fetch(apiUrl+'/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    console.log(data);
    console.log(response);
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