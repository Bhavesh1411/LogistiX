{
    "name": "LogistiX",
    "summary": "Smart Transport & Fleet Operations Platform",
    "description": "LogistiX is a production-grade Odoo ERP platform for Transport & Fleet Operations.",
    "version": "18.0.1.0.0",
    "author": "Chief Odoo Solution Architect",
    "license": "LGPL-3",
    "depends": [
        "base",
        "web",
        "contacts",
        "mail",
        "fleet",
        "hr",
        "maintenance",
        "hr_expense"
    ],
    "data": [
        # Phase 3 - Security Layer
        # Load order matters: groups → ACL → record rules
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/record_rules.xml",
        # Actions
        "views/actions.xml",
        # Custom & Inherited Form/Tree Views
        "views/trip_views.xml",
        "views/vehicle_views.xml",
        "views/employee_views.xml",
        "views/vehicle_document_views.xml",
        "views/driver_document_views.xml",
        "views/notification_views.xml",
        "views/audit_log_views.xml",
        # Search & Analytical Views
        "views/search_views.xml",
        "views/graph_views.xml",
        "views/pivot_views.xml",
        "views/calendar_views.xml",
        # Menus
        "views/menu_views.xml",
    ],
    "application": True,
    "installable": True,
}
