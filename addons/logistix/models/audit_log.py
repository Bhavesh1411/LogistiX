from odoo import models, fields

class LogistixAuditLog(models.Model):
    _name = "logistix.audit.log"
    _description = "LogistiX System Audit Log"
    _rec_name = "action_type"
    _order = "performed_at desc"

    action_type = fields.Char(
        string="Action",
        required=True,
        help="Operational action name performed in the system"
    )
    model_name = fields.Char(
        string="Model Name",
        required=True,
        help="Technical model identifier associated with this audit entry"
    )
    record_id = fields.Char(
        string="Record ID",
        required=True,
        help="Technical database primary record key"
    )
    performed_by = fields.Char(
        string="Performed By",
        help="Operator or system agent executing the action"
    )
    performed_at = fields.Datetime(
        string="Performed At",
        default=fields.Datetime.now,
        help="Timestamp of the audited transaction"
    )
    remarks = fields.Text(
        string="Remarks",
        help="Detail operational notes regarding this audit"
    )
