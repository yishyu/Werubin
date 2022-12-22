var autocomplete;

function initGoogle(){
    /*
    * This function is called when the google maps api is loaded
    * It initializes the autocomplete input
    * It also adds a listener on the locate me button
    * When the button is clicked, it gets the current location and fills the input with the address
    * It also fills the lat and lng hidden inputs that are needed for the post
    */
    initAutocomplete();
    $("#locate-me").unbind().click(() => {
        var onError = function(error) {
            alert("Could not get the current location.");
        };
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    let lat = position.coords.latitude, lng = position.coords.longitude
                    $("#lat").val(lat)
                    $("#lng").val(lng)
                    $("#locate-me").prop('disabled', true);
                    geocoder = new google.maps.Geocoder();
                    var latlng = new google.maps.LatLng(lat,lng);
                    geocoder.geocode({ 'latLng': latlng }).then((results) => {
                        // taking the first possible result
                        $("#googleAutocomplete").val(results.results[0].formatted_address)
                    })
                },
                onError
            );
        }else{
            onError();
        }
    })
}
function initAutocomplete() {

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('googleAutocomplete'));
    // add listener on the input
    autocomplete.addListener('place_changed', checkAddress);
}

function checkAddress() {
    /*
    * This function is called when the user selects an address in the autocomplete input
    * It gets the lat and lng of the address and fills the hidden inputs
    */
    // Get the place details from the autocomplete object.
    $("#locate-me").prop('disabled', false);
    var place = autocomplete.getPlace();
    document.getElementById("addressMissingElements").innerHTML = ""
    $("#googleAutocomplete").css('border-color', '#28a745 ')
    if (place.geometry === undefined){
        $("#googleAutocomplete").css('border-color','#dc3545')
        var error_text = "The place you picked is not recognised. Please make sure you click on one option in the box"
        document.getElementById("addressMissingElements").innerHTML = error_text;
        return false;
    }
    var lat = place.geometry.location.lat(),
    lng = place.geometry.location.lng();
    $("#lat").val(lat)
    $("#lng").val(lng)
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    /*
    * This function is called when the geolocation service fails
    */
    var error = browserHasGeolocation ? "Error: The Geolocation service failed." : "Error: Your browser doesn't support geolocation."
    console.log(error)
}

