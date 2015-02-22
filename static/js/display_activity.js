/**
 * Created by laurianemollier on 21/02/15.
 */


function display_activity(item){

    var address = "<p><small>" + item.address + ", " + item.zipcode + " " + item.city + "</small></p>" ;
    var price = "CHF " + item.price + ".-";
    var distance = "" +  Math.round(item.dist*10)/10 + "";

    var main_info = "<div>" +
        item.name +
        "<small style='color: gray;'>" + item.tags.toString()+ "</small>" +
        "</div>";


    return "<a target='_blank' href='activity.html?key="+ item.key +"'><div class='col-sm-6 litteMP' >"+
        "<div class='row well' style='background-image: url(" + item.img_url +") ;'>" +
            "<div class='pull-right distance'><small>" + distance + "&nbsp;km</small></div>" +
            "<div class='banner'>" +
                "<div class='col-sm-8 litteMP'><strong>" + main_info  + "</strong></div>" +
                "<div class='col-sm-4 litteMP pull-right text-right'><small>" + price + "</small></div>" +
        "</div>" +
        "</div> </a>";


}