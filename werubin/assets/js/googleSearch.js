var autocomplete;

$(document).ready(function(){
    initAutocomplete()
})
function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('googleAutocomplete'));
    // add listener on the input
    autocomplete.addListener('place_changed', checkAddress);
}

function checkAddress() {
    // Get the place details from the autocomplete object.
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
    document.getElementById("lat").value = lat
    document.getElementById("lng").value = lng
    // console.log(document.getElementById('lat').value)
    // console.log(document.getElementById('lng').value)
}
