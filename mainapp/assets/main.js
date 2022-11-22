// Used django default forms, add form-control to all input fields
document.querySelectorAll('input').forEach(input => {
    input.classList.add('form-control')
})


// Default location
const defaultLocation = {
    'lat': -33.9328078,
    'lng': 18.8622583
}


// Set OSM copyright
function setCopyright(map) {
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}


// Map to show users in the world
let locationData = document.getElementById("locations-data");

if (locationData !== null) {
    const map = L.map("map");

    const locationGlobe = JSON.parse(locationData.textContent);

    // Set osm copyright
    setCopyright(map);

    let feature = L.geoJSON(locationGlobe, {
        style: function (feature) {
            return {
                color: "#ff4d33"
            }
        }
    })
        .bindPopup(function (layer) {
            return `<b>${layer.feature.properties.name}</b>`;
        })
        .addTo(map);

    map.fitBounds(feature.getBounds(), { padding: [100, 100] });
}


// Map to select user's location
const locationInput = document.getElementById('locationInput');


function updateLocationInput(lat, lng) {
    // Add the lat and lng to location input
    let text = `${lat},${lng}`;
    locationInput.value = text;
}

if (locationInput !== null) {
    const formMapEl = document.getElementById('form-map')

    let lat = formMapEl.getAttribute("lat")
    let lng = formMapEl.getAttribute("lng")

    let value = formMapEl.getAttribute("value")
    
    if (value){
        try {
            // Set the lat and lng if there is a value,
            // if a form is submitted with location, and the location
            // is valid. No need to let the user pick again.
            [lat, lng] = value.split(',')
            updateLocationInput(lat, lng)
        } catch (error) {
            console.error(error)
        }
        
    }


    /* View to set depends on the value of lat and lng above,
    if it's set, use them, if not use the default location values*/
    var formMap = L.map(formMapEl.id).setView(
        [
            lat || defaultLocation.lat,
            lng || defaultLocation.lng
        ], 13);

    // Set osm copyright
    setCopyright(formMap);

    var popup = L.popup();

    /* Set marker here to use only one marker,
    so that onMapClick won't create a new marker for
    every selection
    */
    var marker = null;

    if (lat && lng){
        setMarker(lat, lng);
    }

    function setMarker(lat, lng) {
        if (marker !== null) {
            marker.remove()
        }

        marker = L.marker([lat, lng]).addTo(formMap)
            .bindPopup('Your home location')
            .openPopup();
    }

    // Update map marker everytime a new location is selected
    function onMapClick(e) {
        lat = e.latlng.lat
        lng = e.latlng.lng

        // Update location input
        updateLocationInput(lat, lng)

        setMarker(lat, lng)

    }

    formMap.on('click', onMapClick);
}


// Map for user profile view
const userLocationView = document.getElementById('user-location-view');

if (userLocationView !== null) {
    let lat = userLocationView.getAttribute("lat")
    let lng = userLocationView.getAttribute("lng")

    var userLocationViewMap = L.map(userLocationView.id).setView([lat, lng], 13);

    // Set osm copyright
    setCopyright(userLocationViewMap);

    L.marker([lat, lng]).addTo(userLocationViewMap)
        .bindPopup('Your home location');
}
