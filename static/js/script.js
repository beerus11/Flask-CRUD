/**
 * Created by Anurag on 17-04-2017.
 */
$(document).ready(function () {
    $('select').material_select();
    $('.modal').modal();
    $("select").change(function () {
        console.log(this);
        var val = $('option:selected', this).attr('value');
        console.log(this.id);
        if (this.id == "action_product") {
            if (val == 0) {
                var row = $(this).closest("tr");
                var id = row.find("td#id").text().trim();
                var product_name = row.find("td#product_name").text().trim();
                var category = row.find("td#category").text().trim();
                var price = row.find("td#price").text().trim();
                var date_added = row.find("td#date_added").text().trim();
                var status = row.find("td#status").text().trim();
                $('#modal2').modal('open');
                $("#edit_product_id").val(id);
                $("#edit_product_name").val(product_name);
                $("#edit_category").val(category).change();
                $("#edit_status").val(status).change();
                $("#edit_price").val(price);
                console.log(category);
                console.log(price);


            } else if (val == 1) {
                console.log("Deleting Product");
                var id = $('option:selected', this).attr('data').trim();
                $.ajax({
                    type: "POST",
                    url: "delProduct",
                    data: {id: id},
                    success: function (result) {
                        location.reload();
                    }
                });
            }
        }
        else if (this.id == "action_user") {
            if (val == 0) {

            } else if (val == 1) {
                console.log("Deleting User");
                var username = $('option:selected', this).attr('data').trim();
                $.ajax({
                    type: "POST",
                    url: "delUser",
                    data: {username: username},
                    success: function (result) {
                        location.reload();
                    }
                });
            }
        }
        else if (this.id == "action_category") {
            if (val == 0) {

            } else if (val == 1) {

            }
        }
        else if (this.id == "action_orders") {
            if (val == 0) {

            } else if (val == 1) {

            }
        }
    });

    $("#add_product").click(function () {
        var json = convertFormToJSON("#productForm");
        console.log(json);
        $.ajax({
            type: "POST",
            url: "addProduct",
            data: json,
            success: function (result) {
                location.reload();
            }
        });
    });
    $("#add_category").click(function () {

        var json = convertFormToJSON("#productCategory");
        console.log(json);
        $.ajax({
            type: "POST",
            url: "addCategory",
            data: json,
        });
    });
    $("#add_order").click(function () {
        var json = convertFormToJSON("#productOrder");
        console.log(json);
        $.ajax({
            type: "POST",
            url: "addOrder",
            data: json,
        });
    });


    $("#edit_product").click(function () {
        var json = convertFormToJSON("#editproductForm");
        json["id"] = $("#edit_product_id").val();
        json["status"] = $("#edit_p_status").val();
        console.log(json);
        $.ajax({
            type: "POST",
            url: "editProduct",
            data: json,
            success: function (result) {
                location.reload();
                $('#modal2').modal('close');
            }
        });

    });

});

function convertFormToJSON(form) {
    var array = jQuery(form).serializeArray();
    var json = {};

    jQuery.each(array, function () {
        json[this.name] = this.value || '';
    });

    return json;
}
