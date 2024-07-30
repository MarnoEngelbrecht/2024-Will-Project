const listContainer = document.getElementById('listings-list');

async function fetchUserProperties(user){
    const data = getUserDetails(user)
    bindProfile(data);
    
    url = apiUrlUser+"/properties/"+user;
    await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
        }).then(response => {
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            // Parse the JSON response
            return response.json();
        })
        .then(data => {
            loadUserProperties(data);
        })
        .catch(error => {
            noItem = document.createElement('h1');
            listContainer.children = [];
            noItem.innerHTML = 'No Properties';
            listContainer.appendChild(noItem);
        });
}




function loadUserProfile(user){
    fetchUserProperties(user);
}

function loadUserProperties(data){
    if(data){
        data.forEach(property => {
            const card = createPropertyListItem(property);
            listContainer.appendChild(card);
        });
    }  
}

function createPropertyListItem(property){
    const card = document.createElement('div');
    card.id = 'property-list-item';
    card.className = 'item';

    const title = document.createElement('h3');
    title.textContent = property.Title;
    card.appendChild(title);

    const iconContainer = document.createElement('div');
    iconContainer.id = 'icon-container';
    iconContainer.className = 'icon-container';
    const beds = document.createElement('p');
    const BedIcon = document.createElement("i");
    BedIcon.classList.add("bx");
    BedIcon.classList.add("bx-bed");
    beds.textContent = property.NrBeds + " ";
    beds.appendChild(BedIcon);
    iconContainer.appendChild(beds);

    const bathrooms = document.createElement('p');
    const BathIcon = document.createElement("i");
    BathIcon.classList.add("bx");
    BathIcon.classList.add("bx-bath");
    bathrooms.textContent = property.NrBathrooms + " ";
    bathrooms.appendChild(BathIcon);
    iconContainer.appendChild(bathrooms);

    const parking = document.createElement('p');
    const CarIcon = document.createElement("i");
    CarIcon.classList.add("bx");
    CarIcon.classList.add("bx-car");
    parking.textContent = property.ParkingSpots + " ";
    parking.appendChild(CarIcon);
    iconContainer.appendChild(parking);
    card.appendChild(iconContainer)

    const spacer = document.createElement('div');
    spacer.classList.add('spacer');
    card.appendChild(spacer);
    const linkContainer = document.createElement('div');
    linkContainer.classList.add('link-container');
    const link = document.createElement('a');
    link.href = 'details.html';
    link.className = 'cta-button';
    link.textContent = 'View Details';
    link.setAttribute('onclick', `viewProperty('${property.RefProperty}')`);
    linkContainer.appendChild(link);
    card.appendChild(linkContainer);

    return card;
}

function bindProfile(data){
    const userName = document.getElementById('agent-username');

    userName.innerHTML = data["Username"] + " - " + data["Email"];
}

async function doDelete(){
    await fetch(apiUrlUser+'/delete/'+currentUser, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
        }).then(response => {
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            logout();
            location.reload();
        })
        .catch(error => {
            console.error(error);
        });
}

function confirmDelete(){
    const response = confirm('Are you sure you want to delete your account?');
    if (response){
        doDelete();
    }
}