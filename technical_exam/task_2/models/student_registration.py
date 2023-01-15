from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    _name = 'student.registration'
    _description = 'StudentRegistration'

    name = fields.Char()
    date = fields.Date(string="Date", required=True, )
    student_id = fields.Many2one('res.partner', required=True, domain="[('is_student', '=', True)]")
    phone_id = fields.Char(related="student_id.phone")
    age = fields.Integer(Readonly=True, Stored=False, compute='age_of_student')
    to_day = fields.Date(default=datetime.today())
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id,string="Currency")
    amount = fields.Monetary(string="Amount", required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('invoiced', 'Invoiced'),
                              ('canceled', 'Canceled')])


    @api.model
    def create(self, vals):
        res = super(StudentRegistration, self).create(vals)
        res['name'] = self.env['ir.sequence'].next_by_code('student.registration.sequence')
        return res
    def age_of_student(self):
        for record in self:
            if record.student_id.birth_date:
                record.age = record.to_day.year - record.student_id.birth_date.year - 1

    @api.constrains('amount')
    def validation_positive_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Amount Must Be More Than Zero."))


    def registration_confirm(self):
        for confirm in self:
            confirm.state='confirmed'

    def registration_create_invoice(self):
        for crea in self:
            crea.state='invoiced'
            create_invoice = crea.env['account.move']
            create_invoice.create({
                'move_type': 'out_invoice',
                'partner_id':crea.student_id.id,
                'invoice_date':crea.date,
                'registration_id':crea.id,
            })
            return create_invoice

    def get_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'context': "{'create': False}"
        }




    def registration_canceled(self):
        for confirm in self:
            confirm.state='canceled'



