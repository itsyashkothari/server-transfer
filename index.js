function addDynamicMarker(location) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: false,
        // icon: image,
   //     animation: google.maps.Animation.DROP
    });
    setTimeout(function () {
        marker.setMap(null);
        delete marker;
    }, 2000);
    return marker;
}

var map = null;
var z=0;
function initialize() {
    var p1= {lat:22.722443, lng:75.868113};
    var p2= {lat:22.976086, lng:76.051835};
    var mapOptions = {
        zoom: 10,
        center: new google.maps.LatLng((p1.lat+p2.lat)/2,(p1.lng+p2.lng)/2)
    };

    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);


    setInterval(function () {
        z=z+0.01;

      //  var position = new google.maps.LatLng(
      //      20.5937+0.01*z, 78.9629+0.01*z,
      //      );
        var position = new google.maps.LatLng(
            p1.lat+(p2.lat-p1.lat)*z,p1.lng+(p2.lng-p1.lng)*z

        );
        var marker = addDynamicMarker(position);
        /*
         var marker = new google.maps.Marker({
         position: position,
         map: map
         });
         */

        marker.setTitle((i + 1).toString());
        attachSecretMessage(marker, i);
    }, 2000);
}

// The five markers show a secret message when clicked
// but that message is not within the marker's instance data
function attachSecretMessage(marker, num) {
    var message = ['This', 'is', 'the', 'secret', 'message'];
    var infowindow = new google.maps.InfoWindow({
        content: message[num]
    });

    google.maps.event.addListener(marker, 'click', function () {
        infowindow.open(marker.get('map'), marker);
    });
}

google.maps.event.addDomListener(window, 'load', initialize);