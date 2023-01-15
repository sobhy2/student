from odoo import api, fields, models

class RegistrationInvoice(models.Model):
    _inherit = 'account.move'

    registration_id = fields.Many2one('student.registration')
