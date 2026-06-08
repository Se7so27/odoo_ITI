from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('related_patient_id')
    def _check_patient_email_unique(self):
        for record in self:
            if record.related_patient_id and record.email:
                patient = self.env['hms.patient'].search([
                    ('email', '=', record.email),
                    ('id', '!=', record.related_patient_id.id),
                ], limit=1)
                if patient:
                    raise ValidationError(
                        "Cannot link this customer to a patient because the email already exists in the patient model."
                    )

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError(
                    "Cannot delete a customer that is linked to a patient."
                )
        return super().unlink()

    @api.constrains('vat', 'is_company')
    def _check_vat_required(self):
        for record in self:
            if record.is_company and not record.vat:
                raise ValidationError("Tax ID is required for company customers.")
