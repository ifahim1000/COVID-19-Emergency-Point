var marker;
var infowindow;
function myMap() {
    var mapOptions = {
        center: new google.maps.LatLng(23.6850, 90.3563),
        zoom: 7,
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    google.maps.event.addListener(map, 'click', function (event) {
        placeMarker(map, event.latLng);
    });
}

function placeMarker(map, location) {
    document.getElementById("lat").value = location.lat();
    document.getElementById("long").value = location.lng();
    if (!marker || !marker.setPosition) {
        marker = new google.maps.Marker({
            position: location,
            map: map,
        });
    } else {
        marker.setPosition(location);
    }
    if (!!infowindow && !!infowindow.close) {
        infowindow.close();
    }
    infowindow = new google.maps.InfoWindow({
        content: 'Your service location'
    });
    infowindow.open(map, marker);
}
