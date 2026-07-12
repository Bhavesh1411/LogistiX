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
    ],
    "application": True,
    "installable": True,
}
