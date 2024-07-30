// Function to fetch a list of objects from the API

async function fetchProperties() {
    // URL of the API endpoint
    // Perform a GET request
    let list_grid = document.getElementById("listings-grid")
    await fetch(apiUrlProperty+"/getcollection",{
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })
        .then(response => {
            // Check if the request was successful
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            // Parse the JSON response
            return response.json();
        })
        .then(data => {
            // Handle the list of objects returned by the API
            console.log(data);
            // Assuming the data is an array of property objects
            data.forEach(async property => {
                // Create a property card for each object
                const card = await createPropertyCard(property);
                // Append the card to the container element
                list_grid.appendChild(card);
            });
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Function to create a property card 
async function createPropertyCard(property) {
    const card = document.createElement('div');
    card.id = 'property-card';
    card.className = 'property-card';

    const img = document.createElement('img');
    img.src = await getThumbnail(property.RefProperty);
    img.alt = 'property image';
    card.appendChild(img);

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

    const link = document.createElement('a');
    link.className = 'cta-button';
    link.textContent = 'View Details';
    link.setAttribute('onclick', `viewProperty('${property.RefProperty}')`);
    card.appendChild(link);

    return card;
}

function showListingAddDialog(){
    const dialog = document.getElementById('listing-add');
    dialog.showModal();
}

function oncloseListingsDialog(){
    const dialog = document.getElementById('listing-add');
    dialog.close();
}

async function onupload() {
    
    let title = document.getElementById('property-title').value;
    let nrBedrooms = document.getElementById('property-bedrooms').value;
    let nrBathrooms = document.getElementById('property-bathrooms').value;
    let nrParking = document.getElementById('property-parking').value;
    let image = document.getElementById('imageInput').files[0];

    await fetch(apiUrlProperty + "/insert", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"Thumbnail" : image, 'Title': title, 'Address': null, 'NrBeds' : nrBedrooms, 'NrBathrooms' : nrBathrooms, 'ParkingSpots' : nrParking }),
        credentials: 'include',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        refreshList();
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function refreshList(){
    location.reload()
    navigateTo('../Listings-page/listings-page.html')
    fetchProperties();
}

async function getThumbnail(RefProperty){
    // await fetch('http://127.0.0.1:5000/properties/image/'+RefProperty, {
    //     method: 'GET',
    //     headers: { 'Content-Type': 'application/json' },
    //     credentials: 'include',
    // })
    // .then( async response => {
    //     if (!response.ok) {
    //         throw new Error('Network response was not ok ' + response.statusText);
    //     }
    //     const data = await response.json();
    //     return data.image;
    // }).catch(error => {
    //     console.error('There was a problem with the fetch operation:', error);
    // });
}
