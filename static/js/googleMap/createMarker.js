/**
 * Created by laurianemollier on 22/02/15.
 */


function createMarker(i, item, map, c){



//infobulle in google maps
    var contentString = "<div id='infoBulle'> <a target='_blank'>" +
        "<img class='img-thumbnail' src='img/ski.jpg'/>" +
        "<h4>" + item.name + "</h4>" +
        "<small style='color: gray;'>" + item.tags.toString()+ "</small>" +
        "</a></div>";

    var icon_png = i > 10? 'bleu' : i + 1;


    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(item.pos.lat, item.pos.lng),
        map: map,
        icon: 'img/marker/' + icon_png + '.png'
    });
    // save new marker in markers array
    markers.push(marker);

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker);
    });
}