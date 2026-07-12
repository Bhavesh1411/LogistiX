from odoo import models, fields

class LogistixNotification(models.Model):
    _name = "logistix.notification"
    _description = "LogistiX System Alert & Notification"
    _rec_name = "title"
    _order = "notification_date desc"

    notification_type = fields.Char(
        string="Notification Type",
        required=True,
        help="System key category of the notification"
    )
    title = fields.Char(
        string="Title",
        help="Display title of the notification alert"
    )
    message = fields.Text(
        string="Message",
        help="Detailed alert body text"
    )
    priority = fields.Selection(
        [("low", "Low"), ("medium", "Medium"), ("high", "High")],
        string="Priority",
        default="low",
        help="Critical tier of the notification alert"
    )
    is_read = fields.Boolean(
        string="Is Read",
        default=False,
        help="Read status of the alert"
    )
    related_model = fields.Char(
        string="Related Model",
        help="Technicall name of the associated database model (e.g. logistix.trip)"
    )
    related_record_id = fields.Char(
        string="Related Record ID",
        help="Identifier of the record that triggered this notification"
    )
    notification_date = fields.Datetime(
        string="Notification Date",
        default=fields.Datetime.now,
        help="Timestamp when the notification was created"
    )
