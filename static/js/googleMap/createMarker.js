/**
 * Created by laurianemollier on 22/02/15.
 */


function createMarker(i, item, map, c){



//infobulle in google maps
   /* var contentString = "<div id='infoBulle'> <a target='_blank'>" +
        "<img class='img-thumbnail' src='img/ski.jpg'/>" +
        "<h4>" + item.name + "</h4>" +
        "<small style='color: gray;'>" + item.tags.toString()+ "</small>" +
        "</a></div>";
        */
    var address = "<p><small>" + item.address + ", " + item.zipcode + " " + item.city + "</small></p>" ;
    var price = "CHF " + item.price + ".-";
    var distance = "" +  Math.round(item.dist*10)/10 + "";

    var main_info = "<div>" +
        item.name +
        "<small style='color: gray;'>" + item.tags.toString()+ "</small>" +
        "</div>";



    var contentString =
        "<div id='infoBulle'> " +
        "<div class='well map' style='background-image: url(" + item.img_url +") ;'>" +
        "<div class='pull-right distance'><small>" + distance + "&nbsp;km</small></div>" +
        "<div class='banner'>" +
        "<div class='col-sm-8 litteMP'><strong>" + main_info  + "</strong></div>" +
        "<div class='col-sm-4 litteMP pull-right text-right'><small>" + price + "</small></div>" +
            "</div>" +

        "</div>";

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