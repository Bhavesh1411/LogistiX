from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    _sql_constraints = [
        ("unique_licence_no", "UNIQUE(licence_no)", "Driving Licence No. must be unique!")
    ]

    licence_no = fields.Char(
        string="Driving Licence No.",
        help="Indian Driving Licence number of the driver"
    )
    experience_years = fields.Integer(
        string="Experience (Years)",
        help="Years of experience the driver has"
    )
    blood_group = fields.Selection(
        [
            ("A+", "A+"),
            ("B+", "B+"),
            ("O+", "O+"),
            ("AB+", "AB+"),
            ("A-", "A-"),
            ("B-", "B-"),
            ("O-", "O-"),
            ("AB-", "AB-"),
        ],
        string="Blood Group",
        help="Blood group of the employee/driver"
    )
    safety_rating = fields.Float(
        string="Safety Rating",
        help="Driver safety rating based on operational history"
    )
    performance_score = fields.Float(
        string="Performance Score",
        help="Key Performance Indicator score for driver output"
    )
    risk_score = fields.Float(
        string="Risk Score",
        help="Driver risk factor calculation based on safety reports"
    )
    availability_status = fields.Selection(
        [
            ("available", "Available"),
            ("unavailable", "Unavailable"),
            ("leave", "On Leave"),
        ],
        string="Availability Status",
        default="available",
        help="Operational availability status of the driver"
    )
    emergency_contact = fields.Char(
        string="Emergency Contact",
        help="Emergency contact number and relationship"
    )
    license_expiry = fields.Date(
        string="Licence Expiry",
        help="Expiration date of the driver's driving licence"
    )
    trip_ids = fields.One2many(
        "logistix.trip",
        "driver_id",
        string="Trips",
        help="Trips driven by this employee"
    )
    document_ids = fields.One2many(
        "logistix.driver.document",
        "driver_id",
        string="Driver Documents",
        help="Compliance documents for this driver"
    )
    expense_ids = fields.One2many(
        "hr.expense",
        "driver_id",
        string="Expenses",
        help="Expenses logged by or for this driver"
    )
