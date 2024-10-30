# path/to/your/module/models/models.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'  # Inherit from the existing partner model

    is_ncd_patient = fields.Boolean(string='NCD Patient', default=False)  # Indicates if the customer is an NCD patient
    ncd_history = fields.Text(string='NCD History')  # Store NCD history
    current_treatment = fields.Text(string='Current Treatment')  # Current treatments


class ProductTemplate(models.Model):
    _inherit = 'product.template'  # Inherit from the existing product model

    ncd_capable = fields.Boolean(string='NCD Capable', default=False)  # Indicates if the product is for NCDs
    expiration_date = fields.Date(string='Expiration Date')  # Track expiration date
    ncd_notes = fields.Text(string='NCD Specific Notes')  # Additional notes related to NCDs


class PosOrder(models.Model):
    _inherit = 'pos.order'  # Inherit from the existing POS order model

    ncd_patient_id = fields.Many2one('res.partner', string='NCD Patient')  # Link to the NCD patient
    ncd_product_ids = fields.Many2many('product.template', string='NCD Products')  # Link to NCD products purchased