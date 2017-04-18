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
                var row = $(this).closest("tr");
                var id = row.find("td#id").text().trim();
                var username = row.find("td#username").text().trim();
                var email = row.find("td#email").text().trim();
                var password = row.find("td#password").text().trim();
                var address = row.find("td#address").text().trim();
                var phone = row.find("td#phone").text().trim();
                var role = row.find("td#role").text().trim();
                $('#modal2').modal('open');
                $("#edit_username").val(username);
                $("#edit_email").val(email);
                $("#edit_password").val(password);
                $("#edit_address").val(address);
                $("#edit_phone").val(phone);
                if (role == "Admin") {
                    $("#edit_role").val('1');
                } else if (role == "Customer") {
                    $("#edit_role").val('2');
                }


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
                var row = $(this).closest("tr");
                var category_name = row.find("td#category_name").text().trim();
                var parent_category = row.find("td#parent_category").text().trim();
                $('#modal2').modal('open');
                $("#edit_category_name").val(category_name);
                $("#edit_parent_category").val(parent_category);

            } else if (val == 1) {
                console.log("Deleting Category");
                var category_name = $('option:selected', this).attr('data').trim();
                $.ajax({
                    type: "POST",
                    url: "delCategory",
                    data: {category_name: category_name},
                    success: function (result) {
                        location.reload();
                    }
                });
            }
        }
        else if (this.id == "action_orders") {
            if (val == 0) {

            } else if (val == 1) {
                console.log("Deleting Order");
                var id = $('option:selected', this).attr('data').trim();
                $.ajax({
                    type: "POST",
                    url: "delOrder",
                    data: {id: id},
                    success: function (result) {
                        location.reload();
                    }
                });
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
        var json = convertFormToJSON("#categoryForm");
        console.log(json);
        $.ajax({
            type: "POST",
            url: "addCategory",
            data: json,
            success: function (result) {
                location.reload();
            }
        });
    })

    $("#add_order").click(function () {
        var json = convertFormToJSON("#myorderForm");
        console.log(json);
        $.ajax({
            type: "POST",
            url: "addOrder",
            data: json,
            success: function (result) {
                location.reload();
            }
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

    $("#edit_user").click(function () {
        var json = convertFormToJSON("#edituserForm");

        console.log(json);
        $.ajax({
            type: "POST",
            url: "editUser",
            data: json,
            success: function (result) {
                location.reload();
                $('#modal2').modal('close');
            }
        });

    });

    $("#edit_category").click(function () {
        var json = convertFormToJSON("#editcategoryForm");
        json["category_name"] = $("#edit_category_name").val();
        json["parent_category"] = $("#edit_p_category").val();
        console.log(json);
        $.ajax({
            type: "POST",
            url: "editCategory",
            data: json,
            success: function (result) {
                location.reload();
                $('#modal2').modal('close');
            }
        });


    });


    $("#edit_order").click(function () {
        var json = convertFormToJSON("#edituserForm");
        console.log(json);
        /*
         $.ajax({
         type: "POST",
         url: "editOrder",
         data: json,
         success: function (result) {
         location.reload();
         $('#modal2').modal('close');
         }
         });
         */

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
