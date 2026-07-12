from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    _sql_constraints = [
        ("unique_gstin", "UNIQUE(gstin)", "GSTIN must be unique!"),
        ("unique_pan", "UNIQUE(pan)", "PAN must be unique!")
    ]

    partner_type = fields.Selection(
        [
            ("client", "Client"),
            ("vendor_fuel", "Fuel Vendor"),
            ("vendor_maint", "Maintenance Vendor"),
            ("vendor_general", "General Vendor"),
        ],
        string="Partner Type",
        help="Categorization of the partner within LogistiX operations"
    )
    gstin = fields.Char(
        string="GSTIN",
        help="Indian Goods and Services Tax Identification Number"
    )
    pan = fields.Char(
        string="PAN",
        help="Indian Permanent Account Number"
    )
    trip_ids = fields.One2many(
        "logistix.trip",
        "partner_id",
        string="Trips",
        help="Trips associated with this partner"
    )
