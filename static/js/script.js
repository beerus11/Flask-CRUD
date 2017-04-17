/**
 * Created by Anurag on 17-04-2017.
 */
$(document).ready(function () {
    $('select').material_select();
    $('.modal').modal();
    $("select").change(function () {
        console.log(this);
        var val = this.val();
        if (this.id = "action_product") {
        }
        else if (this.id = "action_category") {

        }
        else if (this.id = "action_users") {

        }
        else if (this.id = "action_orders") {

        }
    });

});
