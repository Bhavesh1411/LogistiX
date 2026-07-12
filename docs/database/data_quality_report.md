# Data Quality & Referential Integrity Report

## Record Counts
- Clients & Vendors: 230
- Drivers: 80
- Vehicles: 70
- Trips: 5000
- Fuel Logs: 12246
- Expenses: 17093
- Maintenance: 799
- Vehicle Documents: 420
- Driver Documents: 320
- Notifications: 1000
- Audit Logs: 10000

## Referential Integrity Checks
- All Trip Driver IDs exist in hr_employee.csv: PASS
- All Trip Vehicle IDs exist in fleet_vehicle.csv: PASS
- All Fuel Vendor IDs exist in res_partner.csv: PASS
- All Expense Driver IDs exist in hr_employee.csv: PASS

## Realism & Edge Cases Injected
- Cancelled Trips: 103
- Delayed Trips: 408
- Expired Vehicle Docs: 35
- Expired Driver Docs: 24

STATUS: ALL DATASETS PASSED ODOO INTEGRITY VALIDATION.
