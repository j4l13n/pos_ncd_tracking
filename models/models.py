# pos_ncd_tracking/models/models.py
from odoo import models, fields, api
from datetime import timedelta
import requests
import base64
import os
from odoo import api, SUPERUSER_ID

# Define the token constant
SMS_AUTH_TOKEN = ''  # Initialize as empty

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_ncd_patient = fields.Boolean(string='NCD Patient', default=False)
    ncd_history = fields.Text(string='NCD History')
    current_treatment = fields.Text(string='Current Treatment')
    last_product_received = fields.Date(string='Last Product Received Date')
    next_reminder_date = fields.Date(string='Next Reminder Date')
    product_reminder_interval = fields.Integer(string='Reminder Interval (Days)', default=30)
    sms_opt_in = fields.Boolean(string='Opt-in for SMS Notifications', default=False)
    communication_log_ids = fields.One2many('ncd.communication.log', 'patient_id', string='Communication Log')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ncd_capable = fields.Boolean(string='NCD Capable', default=False)
    expiration_date = fields.Date(string='Expiration Date')
    ncd_notes = fields.Text(string='NCD Specific Notes')
    usage_duration_days = fields.Integer(string='Usage Duration (Days)', help="Expected product duration for a patient")


class PosOrder(models.Model):
    _inherit = 'pos.order'

    ncd_patient_id = fields.Many2one('res.partner', string='NCD Patient')
    ncd_product_ids = fields.Many2many('product.template', string='NCD Products')
    product_received_date = fields.Date(string='Product Received Date', default=fields.Date.today)

    @api.model
    def create(self, vals):
        global SMS_AUTH_TOKEN  # Declare the variable as global
        SMS_AUTH_TOKEN = self.env['ir.config_parameter'].sudo().get_param('sms_auth_token')  # Fetch from Odoo settings
        order = super(PosOrder, self).create(vals)
        
        has_patient = order.ncd_patient_id is not None
        has_products = bool(order.ncd_product_ids)
        sms_opt_in = order.ncd_patient_id.sms_opt_in
        is_ncd_patient = order.ncd_patient_id.is_ncd_patient

        if not sms_opt_in:
            # If SMS opt-in is false, do not send anything
            return order

        if has_patient and has_products and is_ncd_patient:
            self._update_patient_info(order)
            self._log_communication(order)
            self._send_purchase_confirmation(order)
        return order

    def _update_patient_info(self, order):
        patient = order.ncd_patient_id
        patient.last_product_received = order.product_received_date
        max_duration = max(order.ncd_product_ids.mapped('usage_duration_days'))
        patient.next_reminder_date = order.product_received_date + timedelta(days=max_duration)

    def _log_communication(self, order):
        for product in order.ncd_product_ids:
            if product.ncd_capable and product.expiration_date:
                next_communication_date = product.expiration_date - timedelta(days=product.usage_duration_days)
                self.env['ncd.communication.log'].create({
                    'patient_id': order.ncd_patient_id.id,
                    'communication_type': 'sms',
                    'communication_date': fields.Datetime.now(),
                    'next_communication_date': next_communication_date,
                    'message_content': f"New order created for patient {order.ncd_patient_id.name} with NCD products."
                })

    def _send_purchase_confirmation(self, order):
        if order.ncd_patient_id.sms_opt_in:
            self.send_sms(order.ncd_patient_id, f"Thank you for your purchase, {order.ncd_patient_id.name}!")

    def send_sms(self, patient, message):
        if patient.phone:  # Ensure the patient has a phone number
            url = 'https://www.intouchsms.co.rw/api/sendsms/.json'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {SMS_AUTH_TOKEN}'  # Use the encoded credentials
            }
            data = {
                'recipients': patient.phone,
                'sender': 'ADBanking',
                'message': message
            }
            try:
                response = requests.post(url, headers=headers, data=data)
                response_data = response.json()
                if response_data.get('success') and response_data.get('summary', {}).get('totalmessages', 0) > 0:
                    print(f"Sending SMS to {patient.name}: {message}")  # Log the action
                else:
                    print(f"Failed to send SMS to {patient.name}: {response_data.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"Failed to send SMS to {patient.name}: {str(e)}")


class NcdCommunicationLog(models.Model):
    _name = 'ncd.communication.log'
    _description = 'NCD Communication Log'

    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    communication_type = fields.Selection([('sms', 'SMS'), ('email', 'Email'), ('call', 'Call')], string='Communication Type')
    communication_date = fields.Datetime(string='Communication Date', default=fields.Datetime.now)
    message_content = fields.Text(string='Message Content')
    next_communication_date = fields.Datetime(string='Next Communication Date')

    @api.model
    def send_scheduled_communications(self):
        global SMS_AUTH_TOKEN  # Declare the variable as global
        SMS_AUTH_TOKEN = self.env['ir.config_parameter'].sudo().get_param('sms_auth_token')  # Fetch from Odoo settings
        today = fields.Datetime.now().date()
        logs = self.search([('next_communication_date', '=', today)])
        
        for log in logs:
            self._send_message(log)

        self._send_refill_reminders(today)

    def _send_message(self, log):
        patient = log.patient_id
        message = log.message_content
        if patient.sms_opt_in:  # Check if the patient opted in for SMS
            self.send_sms(patient, message)

    def _send_refill_reminders(self, today):
        patients = self.env['res.partner'].search([('sms_opt_in', '=', True)])
        for patient in patients:
            if patient.last_product_received and patient.next_reminder_date == today:
                self.send_sms(patient, "Your refill is due. Please visit us to get your medication.")

    def send_sms(self, patient, message):
        if patient.phone:  # Ensure the patient has a phone number
            url = 'https://www.intouchsms.co.rw/api/sendsms/.json'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {SMS_AUTH_TOKEN}'
            }
            data = {
                'recipients': patient.phone,
                'sender': 'ADBanking',
                'message': message
            }
            try:
                response = requests.post(url, headers=headers, data=data)
                response_data = response.json()
                if response_data.get('success') and response_data.get('summary', {}).get('totalmessages', 0) > 0:
                    print(f"Sending SMS to {patient.name}: {message}")  # Log the action
                else:
                    print(f"Failed to send SMS to {patient.name}: {response_data.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"Failed to send SMS to {patient.name}: {str(e)}")

    def send_current_message(self):
        """Send the current message content to the patient."""
        if self.patient_id and self.message_content:
            self.send_sms(self.patient_id, self.message_content)


class SmsSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sms_auth_token = fields.Char(string='SMS Auth Token')

    def set_values(self):
        super(SmsSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sms_auth_token', self.sms_auth_token)

    def get_values(self):
        res = super(SmsSettings, self).get_values()
        res.update({
            'sms_auth_token': self.env['ir.config_parameter'].sudo().get_param('sms_auth_token'),
        })
        return res
