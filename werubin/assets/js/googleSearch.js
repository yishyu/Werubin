var autocomplete;

function initGoogle(){
    /**
     * Initiate the localisation services
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
    /**
     * Creates the listener for the autocomplete
     */
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('googleAutocomplete'));
    // add listener on the input
    autocomplete.addListener('place_changed', checkAddress);
}

function checkAddress() {
    /**
     * Get the place details from the autocomplete object.
     */
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
    var error = browserHasGeolocation ? "Error: The Geolocation service failed." : "Error: Your browser doesn't support geolocation."
    console.log(error)
}

