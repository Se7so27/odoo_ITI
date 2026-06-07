from odoo import models,fields
from datetime import date
class patient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'
    first_name = fields.Char(string= "First Name")
    last_name = fields.Char(string= "Last Name")
    birth_date = fields.Date(string= "Birth Date")
    history = fields.Html(string= "Medical History")
    cr_ratio = fields.Float(string = "Creatine Ratio")
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string="Blood Type")
    pcr = fields.Boolean(string = "PCR Test")
    image = fields.Binary(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age", compute="_compute_age")

    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0