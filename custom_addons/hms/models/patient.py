from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email address must be unique.'),
    ]

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date(string="Birth Date")
    email = fields.Char(string="Email")
    history = fields.Html(string="Medical History")
    cr_ratio = fields.Float(string="Creatine Ratio")
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string="Blood Type")
    pcr = fields.Boolean(string="PCR Test")
    image = fields.Binary(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age", compute="_compute_age")

    department_id = fields.Many2one('hms.department', string="Department")
    department_capacity = fields.Integer(string="Department Capacity", related='department_id.capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctors', string="Doctors")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string="State", default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Log History")

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
            if age < 30 and not self.pcr:
                self.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Auto-checked',
                        'message': 'PCR test has been automatically checked because the patient is under 30 years old.',
                    }
                }

    @api.constrains('email')
    def _check_email_valid(self):
        for record in self:
            if record.email:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.email):
                    raise ValidationError("Please enter a valid email address.")

    @api.constrains('email')
    def _check_email_unique(self):
        for record in self:
            if record.email:
                existing = self.search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id),
                ], limit=1)
                if existing:
                    raise ValidationError("Email address must be unique.")

    @api.constrains('department_id')
    def _check_department_opened(self):
        for record in self:
            if record.department_id and not record.department_id.is_opened:
                raise ValidationError("Cannot select a closed department.")

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR test is checked.")

    def action_add_patient(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'res_model': 'hms.patient',
            'view_mode': 'list,form',
            'target': 'current',
        }

    def action_update_patient(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patients',
            'res_model': 'hms.patient',
            'view_mode': 'list,form',
            'target': 'current',
        }

    def write(self, vals):
        if 'state' in vals:
            old_states = {r.id: r.state for r in self}
            result = super().write(vals)
            for record in self:
                old_state = old_states[record.id]
                if old_state != record.state:
                    self.env['hms.patient.log'].create({
                        'patient_id': record.id,
                        'description': f"State changed to {record.state}",
                    })
            return result
        return super().write(vals)