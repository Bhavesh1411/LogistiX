from odoo import models, fields

class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    capacity_tons = fields.Float(
        string="Payload Capacity (Tons)",
        help="Maximum payload capacity of the vehicle in metric tons"
    )
    mileage_kmpl = fields.Float(
        string="Mileage (KMPL)",
        help="Fuel efficiency of the vehicle in kilometers per liter"
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        help="Currency used for monetary records of this vehicle"
    )
    purchase_cost = fields.Monetary(
        string="Purchase Cost",
        currency_field="currency_id",
        help="Acquisition cost of the vehicle"
    )
    fleet_health_score = fields.Float(
        string="Fleet Health Score",
        help="Health score indicator based on service history and age"
    )
    current_odometer_snapshot = fields.Float(
        string="Odometer Snapshot",
        help="Odometer reading snapshot for performance tracking"
    )
    availability_status = fields.Selection(
        [
            ("available", "Available"),
            ("unavailable", "Unavailable"),
            ("maintenance", "Under Maintenance"),
        ],
        string="Availability Status",
        default="available",
        help="Current operational availability status of the vehicle"
    )
    trip_ids = fields.One2many(
        "logistix.trip",
        "vehicle_id",
        string="Trips",
        help="Trips performed by this vehicle"
    )
    document_ids = fields.One2many(
        "logistix.vehicle.document",
        "vehicle_id",
        string="Vehicle Documents",
        help="Registration, fitness, insurance and other documents of the vehicle"
    )
    fuel_log_ids = fields.One2many(
        "fleet.vehicle.log.fuel",
        "vehicle_id",
        string="Fuel Logs",
        help="Fuel refilling logs associated with this vehicle"
    )
    maintenance_ids = fields.One2many(
        "fleet.vehicle.log.services",
        "vehicle_id",
        string="Maintenance Logs",
        help="Maintenance and service logs associated with this vehicle"
    )
