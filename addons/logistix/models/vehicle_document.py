from odoo import models, fields

class LogistixVehicleDocument(models.Model):
    _name = "logistix.vehicle.document"
    _description = "Vehicle Compliance Document"
    _rec_name = "name"
    _order = "expiry_date asc"
    _inherit = ["mail.thread", "logistix.document.mixin"]

    _sql_constraints = [
        ("unique_vehicle_doc_name", "UNIQUE(name)", "The document reference must be unique!")
    ]

    name = fields.Char(
        string="Document Reference",
        required=True,
        copy=False,
        help="Unique reference number for this document"
    )

    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehicle",
        required=True,
        help="Vehicle associated with this compliance document"
    )
    document_type = fields.Selection(
        [
            ("RC", "Registration Certificate (RC)"),
            ("Insurance", "Insurance Policy"),
            ("PUC", "Pollution Under Control (PUC)"),
            ("Fitness", "Fitness Certificate"),
            ("Permit", "National/State Permit"),
            ("Road Tax", "Road Tax Receipt"),
        ],
        string="Document Type",
        required=True,
        help="Category classification of this vehicle document"
    )
