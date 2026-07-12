from odoo import models, fields

class LogistixTimestampMixin(models.AbstractModel):
    _name = "logistix.timestamp.mixin"
    _description = "Timestamp Mixin"

    created_on = fields.Datetime(
        string="Created On",
        default=fields.Datetime.now,
        help="Timestamp when the record was created"
    )
    updated_on = fields.Datetime(
        string="Updated On",
        default=fields.Datetime.now,
        help="Timestamp when the record was last updated"
    )
