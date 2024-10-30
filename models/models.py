# pos_ncd_tracking/models/models.py
from odoo import models, fields, api
from datetime import timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'  # Inherit from the existing partner model

    is_ncd_patient = fields.Boolean(string='NCD Patient', default=False)  # Indicates if the customer is an NCD patient
    ncd_history = fields.Text(string='NCD History')  # Store NCD history
    current_treatment = fields.Text(string='Current Treatment')  # Current treatments
    last_product_received = fields.Date(string='Last Product Received Date')  # Date of last product received
    next_reminder_date = fields.Date(string='Next Reminder Date')  # Date for next reminder
    product_reminder_interval = fields.Integer(string='Reminder Interval (Days)', default=30)  # Days until next reminder

    # Communication log for tracking interactions
    communication_log_ids = fields.One2many('ncd.communication.log', 'patient_id', string='Communication Log')


class ProductTemplate(models.Model):
    _inherit = 'product.template'  # Inherit from the existing product model

    ncd_capable = fields.Boolean(string='NCD Capable', default=False)  # Indicates if the product is for NCDs
    expiration_date = fields.Date(string='Expiration Date')  # Track expiration date
    ncd_notes = fields.Text(string='NCD Specific Notes')  # Additional notes related to NCDs
    usage_duration_days = fields.Integer(string='Usage Duration (Days)', help="Number of days this product is expected to last for a patient")  # Expected product duration


class PosOrder(models.Model):
    _inherit = 'pos.order'  # Inherit from the existing POS order model

    ncd_patient_id = fields.Many2one('res.partner', string='NCD Patient')  # Link to the NCD patient
    ncd_product_ids = fields.Many2many('product.template', string='NCD Products')  # Link to NCD products purchased
    product_received_date = fields.Date(string='Product Received Date', default=fields.Date.today)  # Date the product was received by patient

    # Update next reminder date on confirming an order for an NCD patient
    @api.model
    def create(self, vals):
        order = super(PosOrder, self).create(vals)
        if order.ncd_patient_id and order.ncd_product_ids:
            # Update the patient's last product received date and next reminder date
            patient = order.ncd_patient_id
            patient.last_product_received = order.product_received_date
            # Calculate the next reminder date based on product usage duration
            max_duration = max(order.ncd_product_ids.mapped('usage_duration_days'))
            patient.next_reminder_date = order.product_received_date + timedelta(days=max_duration)
        return order


class NcdCommunicationLog(models.Model):
    _name = 'ncd.communication.log'
    _description = 'NCD Communication Log'

    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    communication_type = fields.Selection([('sms', 'SMS'), ('email', 'Email'), ('call', 'Call')], string='Communication Type')
    communication_date = fields.Datetime(string='Communication Date', default=fields.Datetime.now)
    message_content = fields.Text(string='Message Content')
