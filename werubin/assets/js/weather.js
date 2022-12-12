function set_weather(lat, lng, id){
    var API_KEY = "f0fa13a5da8dfa0b1453c158f18d0824";
    var target = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&units=metric&appid=${API_KEY}`;
    var output = ""
    $.getJSON(target, function(fc) {
        output += "<img src='http://openweathermap.org/img/wn/" + fc.weather[0].icon + ".png'><br/>";
        output += fc.main.temp_min + "&deg;C to " + fc.main.temp_max + "&deg;C";
        $(`#${id}`).html(output)
    });
}