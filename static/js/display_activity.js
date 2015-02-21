/**
 * Created by laurianemollier on 21/02/15.
 */


function display_activity(item){

    var address = "<address> <div>" + item.address + "</div> <div>" + item.zipcode + " " + item.city + "</div>" + "</address>";

    var main_info = "<div>" +
        "<h4>" + item.name + "</h4>" +
        "<p>" + item.description+ "</p>" +
        "<small style='color: gray;'>" + item.tags.toString()+ "</small>" +
        // item.price 
        "</div>";


    return "<div class='row well'>" +
        "<div class='col-sm-2'> <img class='img-thumbnail' src='img/ski.jpg'/> </div>" +
        "<div class='col-sm-8'>" + main_info + "</div>" +
        "<div class='col-sm-2'>" + address + "</div>" +
        "</div>";


}