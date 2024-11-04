// static/src/js/ncd_pos.js
odoo.define('pos_ncd_tracking.ncd_pos', function (require) {
    "use strict";

    var PosModel = require('point_of_sale.models');
    var models = require('point_of_sale.models');

    // Extend the ResPartner model to include NCD attributes
    models.load_fields('res.partner', [
        'is_ncd_patient',
        'ncd_history',
        'current_treatment',
        'last_product_received',
        'next_reminder_date',
        'product_reminder_interval',
    ]);

    // Override the customer selection to include NCD attributes
    var _super_get_partners = PosModel.prototype.get_partners;
    PosModel.prototype.get_partners = function (options) {
        var self = this;
        return _super_get_partners.call(this, options).then(function (partners) {
            // Add logic to include NCD attributes in the customer modal
            partners.forEach(function (partner) {
                partner.is_ncd_patient = partner.is_ncd_patient || false;
                partner.ncd_history = partner.ncd_history || '';
                partner.current_treatment = partner.current_treatment || '';
                partner.last_product_received = partner.last_product_received || false;
                partner.next_reminder_date = partner.next_reminder_date || false;
                partner.product_reminder_interval = partner.product_reminder_interval || 30;
            });
            return partners;
        });
    };

    // Extend the customer creation form to include NCD attributes
    var CustomerForm = require('point_of_sale.CustomerForm');
    var _super_render = CustomerForm.prototype.render;
    CustomerForm.prototype.render = function () {
        _super_render.call(this);
        // Add NCD fields to the customer form
        this.$('.customer-form').append(`
            <div>
                <label for="is_ncd_patient">NCD Patient:</label>
                <input type="checkbox" id="is_ncd_patient" name="is_ncd_patient" />
            </div>
            <div>
                <label for="ncd_history">NCD History:</label>
                <input type="text" id="ncd_history" name="ncd_history" />
            </div>
            <div>
                <label for="current_treatment">Current Treatment:</label>
                <input type="text" id="current_treatment" name="current_treatment" />
            </div>
            <div>
                <label for="last_product_received">Last Product Received:</label>
                <input type="text" id="last_product_received" name="last_product_received" />
            </div>
            <div>
                <label for="next_reminder_date">Next Reminder Date:</label>
                <input type="date" id="next_reminder_date" name="next_reminder_date" />
            </div>
            <div>
                <label for="product_reminder_interval">Product Reminder Interval:</label>
                <input type="number" id="product_reminder_interval" name="product_reminder_interval" />
            </div>
        `);
    };

    // Override the partner modal rendering to include NCD attributes
    var PartnerModal = require('point_of_sale.PartnerModal');
    var _super_render = PartnerModal.prototype.render;
    PartnerModal.prototype.render = function () {
        _super_render.call(this);
        // Add NCD fields to the partner modal
        this.$('.partner-modal').append(`
            <div>
                <label for="is_ncd_patient">NCD Patient:</label>
                <input type="checkbox" id="is_ncd_patient" name="is_ncd_patient" />
            </div>
            <div>
                <label for="ncd_history">NCD History:</label>
                <input type="text" id="ncd_history" name="ncd_history" />
            </div>
            <div>
                <label for="current_treatment">Current Treatment:</label>
                <input type="text" id="current_treatment" name="current_treatment" />
            </div>
            <div>
                <label for="last_product_received">Last Product Received:</label>
                <input type="text" id="last_product_received" name="last_product_received" />
            </div>
            <div>
                <label for="next_reminder_date">Next Reminder Date:</label>
                <input type="date" id="next_reminder_date" name="next_reminder_date" />
            </div>
            <div>
                <label for="product_reminder_interval">Product Reminder Interval:</label>
                <input type="number" id="product_reminder_interval" name="product_reminder_interval" />
            </div>
        `);
    };
});
