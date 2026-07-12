from odoo import models, fields

class LogistixDriverDocument(models.Model):
    _name = "logistix.driver.document"
    _description = "Driver Compliance Document"
    _rec_name = "name"
    _order = "expiry_date asc"
    _inherit = ["mail.thread", "logistix.document.mixin"]

    _sql_constraints = [
        ("unique_driver_doc_name", "UNIQUE(name)", "The document reference must be unique!")
    ]

    name = fields.Char(
        string="Document Reference",
        required=True,
        copy=False,
        help="Unique reference number for this document"
    )

    driver_id = fields.Many2one(
        "hr.employee",
        string="Driver",
        required=True,
        help="Driver employee associated with this compliance document"
    )
    document_type = fields.Selection(
        [
            ("Driving Licence", "Driving Licence"),
            ("Medical Certificate", "Medical Certificate"),
            ("Training Certificate", "Training Certificate"),
            ("Identity Proof", "Identity Proof (Aadhar/PAN/etc.)"),
        ],
        string="Document Type",
        required=True,
        help="Category classification of this driver document"
    )
