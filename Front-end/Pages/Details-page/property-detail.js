let selectedProperty = {
    title : "", 
    Username: "", 
    Email: ""
};

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

        const userData = await getUserDetails(data.RefUser)
        user.innerHTML = userData.Username + " - " + userData.Email;

        title.innerHTML = data.Title;
        const BedIcon = document.createElement("i");
        bedroom.innerHTML = data.NrBeds + ' - Bedrooms';
        bathroom.innerHTML = data.NrBathrooms + ' - Bathrooms';
        parking.innerHTML = data.ParkingSpots + ' - Parking Spots';
        selectedProperty = {
            title : data.Title,
            Username : userData.Username,
            Email : userData.Email,
        }
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

async function getUserDetails(RefUser){
    return await fetch(apiUrlUser+'/'+RefUser, {
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

function showDetailsPageContactPage(){
    const detailsPageContact = document.getElementById('details-page-contact');
    detailsPageContact.style.display="flex";
    detailsPageContact.showModal();
}

function closeDetailsPageContactPage(){
    const detailsPageContact = document.getElementById('details-page-contact');
    detailsPageContact.style.display="none";
    detailsPageContact.close();
}

async function detailsDialogContact(){
    let log_user = await getUserDetails(currentUser);
    const message_el = document.getElementById('details-page-message');
    const params = {
        reply_to : selectedProperty.Email,
        from_email : log_user.Email,
        to_name : selectedProperty.Username,
        from_name : log_user.Username,
        property_name : selectedProperty.title,
        message : message_el.value
    }
    sendEmail(params)
    alert('Agent Was Notified')
}

function sendEmail(templateParams) {
    const serviceID = 'service_vywle5l';
    const templateID = 'template_2jf5539';
    const userID = 'rp_aF3--qQe2ApP8n';

    emailjs.init({
        publicKey: "rp_aF3--qQe2ApP8n",
    });
  
    emailjs.send(serviceID, templateID, templateParams, userID)
      .then((response) => {
        console.log('SUCCESS!', response.status, response.text);
      })
      .catch((error) => {
        console.error('FAILED...', error);
      });
}