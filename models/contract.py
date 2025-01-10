# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class ContractModel(models.Model):
    _name = 'contract.model'
    _description = 'Contract'

    contract_name = fields.Char(string='Contract Name', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='End Date', store=True, compute='_compute_end_date')
    product_ids = fields.Many2many('product.product', string='Product')
    order_ids = fields.One2many('sale.order', 'contract_id', string='Orders')
    status = fields.Selection(
       [('draft', 'Nháp'),
        ('manager_approve', 'Chờ Quản lý phê duyệt'),
        ('director_approve', 'Chờ Giám đốc phê duyệt'),
        ('approved', 'Đã phê duyệt')],
        default='draft', string="Trạng thái")

    @api.depends('start_date')
    def _compute_end_date(self):
        for record in self:
            if record.start_date:
                record.end_date = record.start_date + timedelta(days=365)

    def action_open_contract(self):
        action = self.env.ref('contract.action_contract')
        if self.contract_name:
            action.name = self.contract_name
        return action


