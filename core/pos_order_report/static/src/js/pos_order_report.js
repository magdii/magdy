//odoo.define('pos_order_report.pos_order_report', function (require) {
//    var models = require('point_of_sale.models');
//    var order_model_super = models.Order.prototype;
//    models.Order = models.Order.extend({
//        var first_option = self.$('#input_text_element').val();
//        // we need to patch export_as_JSON because that's what's used
//        // when sending orders to backend
//        console.log(this.first_option)
//        export_as_JSON: function () {
//            var json = order_model_super.export_as_JSON.bind(this)();
//            var to_return = _.extend(json, {
//                'pos_data': this.first_option,
//            });
//            return to_return;
//        },
//});
//});
console.log(":::::::::::::::HELLO")
odoo.define('pos_order_report.models', function (require) {
    var models = require('point_of_sale.models');
    var order_model_super = models.Order.prototype;
    models.Order = models.Order.extend({
        // we need to patch export_as_JSON because that's what's used
        // when sending orders to backend
        export_as_JSON: function () {
            var self = this;
            var json = order_model_super.export_as_JSON.bind(this)();
            console.log("::::::::::::::: IN")
            var first_option = $('#input_text_element').val();
            var to_return = _.extend(json, {
                'pos_data': first_option,
            });
            console.log("::::::::::::::: to_return", to_return)
            return to_return;
        },
    });

});