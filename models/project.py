from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    is_montant_commande_client      = fields.Float(string='Ventes'   , copy=False, readonly=True, help="Commandes clients"     )
    is_montant_commande_fournisseur = fields.Float(string='Achats'   , copy=False, readonly=True, help="Commandes fournisseurs")
    is_marge                        = fields.Float(string='Marge (€)', copy=False, readonly=True)
    is_taux_marge                   = fields.Float(string='Marge (%)', copy=False, readonly=True)


    @api.model
    def _calculer_marge_ir_cron(self):
        self.env['project.project'].search([]).calculer_marge()
        return True


    def _calculer_marge_action(self):
        self.browse(self.env.context['active_ids']).calculer_marge()
 

    def calculer_marge(self):
        for obj in self:
            achats=ventes=marge=taux=0
            for task in obj.task_ids:
                task.calculer_marge()
                achats+=task.is_montant_commande_fournisseur
                ventes+=task.is_montant_commande_client
            marge = ventes-achats
            taux_marge=0
            if achats>0:
                taux_marge = 100*(ventes/achats-1)
            obj.is_montant_commande_client = ventes
            obj.is_montant_commande_fournisseur = achats
            obj.is_marge = marge
            obj.is_taux_marge = taux_marge


class ProjectTask(models.Model):
    _inherit = "project.task"


    def calculer_marge(self):
        for obj in self:
            commande_client=0
            sql = """
                SELECT sum(l.price_subtotal) 
                FROM sale_order_line l join sale_order o on l.order_id=o.id
                WHERE o.state not in ('cancel') and l.is_task_id=%s
            """
            self.env.cr.execute(sql,[obj.id])
            res = self._cr.fetchall()
            for line in res:
                commande_client=line[0] or 0

            commande_fournisseur=0
            sql = """
                SELECT sum(l.price_subtotal) 
                FROM purchase_order_line l join purchase_order o on l.order_id=o.id
                WHERE o.state not in ('cancel') and l.is_task_id=%s
            """
            self.env.cr.execute(sql,[obj.id])
            res = self._cr.fetchall()
            for line in res:
                commande_fournisseur=line[0] or 0

            marge = commande_client-commande_fournisseur
            obj.is_montant_commande_client      = commande_client
            obj.is_montant_commande_fournisseur = commande_fournisseur
            obj.is_marge                        = marge

            taux_marge=0
            if commande_fournisseur>0:
                taux_marge = 100*(commande_client/commande_fournisseur-1)
            obj.is_taux_marge = taux_marge


    is_montant_commande_client      = fields.Float(string='Ventes'   , copy=False, readonly=True, help="Commandes clients"     )
    is_montant_commande_fournisseur = fields.Float(string='Achats'   , copy=False, readonly=True, help="Commandes fournisseurs")
    is_marge                        = fields.Float(string='Marge (€)', copy=False, readonly=True)
    is_taux_marge                   = fields.Float(string='Marge (%)', copy=False, readonly=True)
