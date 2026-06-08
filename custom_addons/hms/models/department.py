from odoo import models, fields, api

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened", default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")

    def action_add_department(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Departments',
            'res_model': 'hms.department',
            'view_mode': 'list,form',
            'target': 'current',
        }

    def action_update_department(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Departments',
            'res_model': 'hms.department',
            'view_mode': 'list,form',
            'target': 'current',
        }
