from odoo import models, fields
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contract_id = fields.Many2one('contract.model', string='Contract')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if not order.contract_id: 
                contract = self.env['contract.model'].create({
                    'contract_name': f'Hợp đồng {order.name}',
                    'start_date': fields.Date.today(),
                    'end_date': fields.Date.today() + timedelta(days=365),
                    'product_ids': [(6, 0, order.order_line.mapped('product_id').ids)],
                    'order_ids': [(4, order.id)],
                })
                order.contract_id = contract.id
        return res


    def action_view_contract(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('contract.action_contract')
        if self.contract_id:
            form_view = [(self.env.ref('contract.view_contract_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = self.contract_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action