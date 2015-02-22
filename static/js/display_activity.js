/**
 * Created by laurianemollier on 21/02/15.
 */


function display_activity(item){

    var address = "<p><small>" + item.address + ", " + item.zipcode + " " + item.city + "</small></p>" ;
    var price = "CHF " + item.price + ".-";

    var main_info = "<div>" +
        "<h4>" + item.name + "</h4>" +
        "<p>" + item.description+ "</p>" +
        "<small style='color: gray;'>" + item.tags.toString()+ "</small>" +
        // item.price
        "</div>";


    return "<div class='row well'>" +
        "<div class='col-sm-2 litteMP'> <img class='img-thumbnail' src='img/ski.jpg'/> </div>" +
        "<div class='col-sm-8 litteMP'>" + main_info + "<br>" + address + "</div>" +
        "<div class='col-sm-2 litteMP'>" + price + "</div>" +
        "</div>";


}