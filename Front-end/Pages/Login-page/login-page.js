const apiUrl = 'http://127.0.0.1:5000/users';

function onSubmit(){
    fetch(apiUrl+"/login")
        .then(response => {
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Login failed ' + response.statusText);
            }
            // Parse the JSON response
            return response.json();
        })
        .then(data => {
            // Handle the list of objects returned by the API
            console.log(data);
            // Assuming the data is an array of property objects
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('There was a problem with the fetch operation:', error);
        });

}