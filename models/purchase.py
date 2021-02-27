from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    is_task_id = fields.Many2one('project.task', string='Tâche', index=True)

