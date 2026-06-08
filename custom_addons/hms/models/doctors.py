from odoo import models, fields, api

class Doctors(models.Model):
    _name = 'hms.doctors'
    _description = 'Hospital Doctors'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Binary(string="Image")

    def action_add_doctor(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Doctors',
            'res_model': 'hms.doctors',
            'view_mode': 'list,form',
            'target': 'current',
        }

    def action_update_doctor(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Doctors',
            'res_model': 'hms.doctors',
            'view_mode': 'list,form',
            'target': 'current',
        }
