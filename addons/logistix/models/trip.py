from odoo import models, fields

class LogistixTrip(models.Model):
    _name = "logistix.trip"
    _description = "Transport Trip Operations"
    _rec_name = "name"
    _order = "dispatch_time desc"
    _inherit = ["mail.thread", "mail.activity.mixin", "logistix.timestamp.mixin"]

    _sql_constraints = [
        ("unique_trip_name", "UNIQUE(name)", "The trip reference must be unique!")
    ]

    name = fields.Char(
        string="Trip Reference",
        required=True,
        copy=False,
        readonly=True,
        default="New",
        help="Unique reference identifier for the trip"
    )
    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehicle",
        required=True,
        tracking=True,
        help="Fleet vehicle assigned to this trip"
    )
    driver_id = fields.Many2one(
        "hr.employee",
        string="Driver",
        required=True,
        tracking=True,
        help="Driver assigned to this trip"
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Client Partner",
        required=True,
        tracking=True,
        help="Client partner associated with this trip"
    )
    origin = fields.Char(
        string="Origin City",
        required=True,
        help="Starting city of the trip"
    )
    destination = fields.Char(
        string="Destination City",
        required=True,
        help="Destination city of the trip"
    )
    distance_km = fields.Float(
        string="Distance (KM)",
        help="Total trip distance in kilometers"
    )
    dispatch_time = fields.Datetime(
        string="Dispatch Time",
        help="Actual timestamp when the vehicle was dispatched"
    )
    eta = fields.Datetime(
        string="Estimated Arrival (ETA)",
        help="Estimated time of arrival at the destination"
    )
    actual_arrival = fields.Datetime(
        string="Actual Arrival Time",
        help="Actual timestamp when the vehicle arrived at the destination"
    )
    trip_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_transit", "In Transit"),
            ("completed", "Completed"),
            ("delayed", "Delayed"),
            ("cancelled", "Cancelled"),
        ],
        string="Trip Status",
        default="draft",
        tracking=True,
        help="Current operational status of the trip"
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        help="Currency used for revenue metrics"
    )
    revenue = fields.Monetary(
        string="Trip Revenue",
        currency_field="currency_id",
        help="Revenue generated from the trip execution"
    )
    cargo_weight = fields.Float(
        string="Cargo Weight (Tons)",
        help="Weight of the transported cargo in metric tons"
    )
    vehicle_capacity_used = fields.Float(
        string="Capacity Utilization (%)",
        help="Percentage of the vehicle payload capacity used"
    )
    expected_duration = fields.Float(
        string="Expected Duration (Hours)",
        help="Expected travel duration in hours"
    )
    trip_type = fields.Selection(
        [
            ("hub_to_hub", "Hub to Hub"),
            ("local_distribution", "Local Distribution"),
        ],
        string="Trip Type",
        default="hub_to_hub",
        help="Type classification of the trip route"
    )
    fuel_log_ids = fields.One2many(
        "fleet.vehicle.log.fuel",
        "trip_id",
        string="Fuel Logs",
        help="Fuel consumption logs registered during this trip"
    )
    expense_ids = fields.One2many(
        "hr.expense",
        "trip_id",
        string="Trip Expenses",
        help="Operating expenses incurred during this trip"
    )


class FleetVehicleLogFuel(models.Model):
    _inherit = "fleet.vehicle.log.fuel"

    trip_id = fields.Many2one(
        "logistix.trip",
        string="Associated Trip",
        help="The specific trip context during which this fuel log was created"
    )


class HrExpense(models.Model):
    _inherit = "hr.expense"

    trip_id = fields.Many2one(
        "logistix.trip",
        string="Associated Trip",
        help="The specific trip context during which this expense was logged"
    )
    driver_id = fields.Many2one(
        "hr.employee",
        string="Associated Driver",
        help="The driver who logged or incurred this expense"
    )
