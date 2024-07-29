async function viewProperty(RefProperty){
    navigateTo('../Details-page/details-page.html')
    await fetch(apiUrlProperty+'/'+RefProperty, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
    })
    .then( async response => {
        const data = await response.json();
        const title = document.getElementById('details-title');
        const bedroom = document.getElementById('details-bedroom');
        const bathroom = document.getElementById('details-bathroom');
        const parking = document.getElementById('details-parking');
        const user = document.getElementById('details-user');

        const userData = getUserDetails(data.RefUser)
        user.innerHTML = userData.Username + " - " + userData.Email;

        title.innerHTML = data.Title;
        bedroom.innerHTML = data.NrBedrooms;
        bathroom.innerHTML = data.NrBathrooms;
        parking.innerHTML = data.ParkingSpots;
        
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

async function getUserDetails(RefUser){
    await fetch(apiUrlUser+'/'+RefUser, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
        }).then(response => {
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}