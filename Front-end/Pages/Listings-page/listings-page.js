let list_grid = document.getElementById("listings-grid")

// Function to fetch a list of objects from the API
function fetchProperties() {
    // URL of the API endpoint
    const apiUrl = 'http://127.0.0.1:5000/properties';

    // Perform a GET request
    fetch(apiUrl+"/getcollection")
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
            data.forEach(property => {
                // Create a property card for each object
                const card = createPropertyCard(property);
                // Append the card to the container element
                list_grid.appendChild(card);
            });
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Example usage: Fetch properties when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchProperties();
});

// Function to create a property card (same as the previous example)
function createPropertyCard(property) {
    const card = document.createElement('div');
    card.id = 'property-card';
    card.className = 'property-card';

    const img = document.createElement('img');
    img.src = property.Thumbnail;
    img.alt = 'property image';
    card.appendChild(img);

    const title = document.createElement('h3');
    title.textContent = property.Title;
    card.appendChild(title);

    const beds = document.createElement('p');
    const BathIcon = document.createElement("i");
    BathIcon.classList.add("fa-regular");
    BathIcon.classList.add("fa-bath");
    beds.appendChild(BathIcon);
    beds.textContent = property.NrBeds + " Bedrooms, " + property.NrBathrooms;
    card.appendChild(beds);

    const bathrooms = document.createElement('p');
    bathrooms.textContent = "Bathrooms " + property.NrBathrooms;
    card.appendChild(bathrooms);

    const parking = document.createElement('p');
    parking.textContent = property.ParkingSpots;
    card.appendChild(parking);

    const link = document.createElement('a');
    link.href = 'details.html';
    link.className = 'cta-button';
    link.textContent = 'View Details';
    card.appendChild(link);

    return card;
}

