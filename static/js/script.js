/**
 * Created by benoit on 15/02/2015.
 */

function make_table_line(pot) {
    var return_value= "<td>"+pot.type+"</td>"+
            "<td>"+pot.quantity+" kg</td>"+
            "<td>"+pot.price+" €</td>";
    if (pot.sellable)
        return_value=return_value+"<td>Oui</td>";
    else
        return_value=return_value+"<td>Non</td>";
    return "<tr>"+return_value+"</tr>";
}

function make_order_line(pot) {
    var return_value;
    if (pot.sellable) {
        return_value = "<td>" + pot.type + "</td>" +
            "<td>" + pot.quantity + " kg</td>" +
            "<td>" + pot.price + " €</td>" +
            "<td class='col-xs-2'><div class='form-group-sm'><input type='text' class='form-control' name='phone' value='0'></div>";
        return_value="<tr>"+return_value+"</tr>";
    } else
        return_value = "";
    return return_value;
}

$( function() {
    var price_table=$('#price-table');
    var order_table=$('#order-table');

    var pot = JSON.parse('{"quantity": 10.0, "sellable": true, "type": "Agata", "key": 4573968371548160, "price": 5.0}');

    $.getJSON('potatoes_list')
        .done(function(data) {
            $.each( data, function( i, item ) {
                price_table.append(make_table_line(item));
            });
            $.each( data, function( i, item ) {
                order_table.append(make_order_line(item));
            });
    });

});