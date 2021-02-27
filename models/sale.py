from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_task_id = fields.Many2one('project.task', string='Tâche', index=True)
