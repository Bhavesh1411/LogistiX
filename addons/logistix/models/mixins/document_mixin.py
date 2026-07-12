from odoo import models, fields

class LogistixDocumentMixin(models.AbstractModel):
    _name = "logistix.document.mixin"
    _description = "Document Mixin"

    issue_date = fields.Date(
        string="Issue Date",
        help="Date when the document was issued"
    )
    expiry_date = fields.Date(
        string="Expiry Date",
        help="Date when the document expires"
    )
    document_status = fields.Selection(
        [("active", "Active"), ("expired", "Expired")],
        string="Document Status",
        default="active",
        tracking=True,
        help="Current status of the document"
    )
