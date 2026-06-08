from odoo import models, fields, api

class HmsDashboard(models.Model):
    _name = 'hms.dashboard'
    _description = 'HMS Dashboard'

    name = fields.Char(string='Name', default='Dashboard')

    patient_ids = fields.Many2many('hms.patient', string='Patients', compute='_compute_patient_ids')
    department_ids = fields.Many2many('hms.department', string='Departments', compute='_compute_department_ids')
    doctor_ids = fields.Many2many('hms.doctors', string='Doctors', compute='_compute_doctor_ids', groups='hms.group_hms_manager')
    patient_log_ids = fields.Many2many('hms.patient.log', string='Logs', compute='_compute_patient_log_ids')

    patient_count = fields.Integer(string='Patient Count', compute='_compute_counts')
    department_count = fields.Integer(string='Department Count', compute='_compute_counts')
    doctor_count = fields.Integer(string='Doctor Count', compute='_compute_counts', groups='hms.group_hms_manager')

    def _compute_patient_ids(self):
        for record in self:
            record.patient_ids = self.env['hms.patient'].search([])

    def _compute_department_ids(self):
        for record in self:
            record.department_ids = self.env['hms.department'].search([])

    def _compute_doctor_ids(self):
        for record in self:
            record.doctor_ids = self.env['hms.doctors'].search([])

    def _compute_patient_log_ids(self):
        for record in self:
            record.patient_log_ids = self.env['hms.patient.log'].search([], limit=50)

    def _compute_counts(self):
        for record in self:
            record.patient_count = self.env['hms.patient'].search_count([])
            record.department_count = self.env['hms.department'].search_count([])
            record.doctor_count = self.env['hms.doctors'].search_count([])

    def action_refresh_dashboard(self):
        self.invalidate_recordset()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hospital Management',
            'res_model': 'hms.dashboard',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.id,
        }
