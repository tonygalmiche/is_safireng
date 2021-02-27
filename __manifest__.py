# Copyright 2021 Tony Galmiche / InfoSaône (https://infosaone.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Module Odoo 14 pour Safireng",
    "summary": "Module Odoo 14 pour Safireng",
    "version": "14.0.1.0.0",
    "author": "InfoSaône",
    "license": "AGPL-3",
    "maintainer": "InfoSaône",
    "category": "InfoSaône",
    "website": "https://infosaone.com",
    "depends": [
        "sale_management",
        "purchase",
        "project",
    ],
    "data": [
        "views/sale_views.xml",
        "views/purchase_views.xml",
        "views/project_views.xml",
        "views/project_data.xml",
    ],
    "auto_install": False,
    "installable": True,
    "application": True,
}
