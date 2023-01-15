from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class StudentPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Is Student ?",default=False)
    birth_date = fields.Date(string="Birth Date",tracking=True,required=True)

    @api.constrains('birth_date','to_day')
    def validation_past_date(self):
        for partner in self:
            today_date=fields.Date.today()
            if partner.birth_date > today_date:
                raise ValidationError(_("your birth date must be in the past."))



