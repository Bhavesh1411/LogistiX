from odoo import models, fields

class LogistixAuditMixin(models.AbstractModel):
    _name = "logistix.audit.mixin"
    _description = "Audit Mixin"

    remarks = fields.Text(
        string="Remarks",
        help="Audit remarks or operational notes"
    )
    action_type = fields.Char(
        string="Action Type",
        help="Type of action performed on the record"
    )
