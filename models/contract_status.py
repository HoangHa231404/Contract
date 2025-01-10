from odoo import models, fields, api, exceptions

class Contract(models.Model):
    _inherit = 'contract.model'

    STATE_SELECTION = [
        ('draft', 'Nháp'),
        ('manager_approve', 'Chờ Quản lý phê duyệt'),
        ('director_approve', 'Chờ Giám đốc phê duyệt'),
        ('approved', 'Đã phê duyệt'),
    ]

    state = fields.Selection(
        selection=STATE_SELECTION,
        string='Trạng thái',
        default='draft',
        track_visibility='onchange',
    )

    manager_approved = fields.Boolean(string="Quản lý phê duyệt")
    director_approved = fields.Boolean(string="Giám đốc phê duyệt")
    

    def action_manager_approve(self):
        for contract in self:
            if contract.state != 'draft':
                raise exceptions.UserError("Hợp đồng không ở trạng thái Nháp.")
            if not self.env.user.has_group('sales_team.group_sale_manager'):
                raise exceptions.AccessError("Chỉ Quản lý Sale được phép phê duyệt.")
            contract.write({'state': 'manager_approve', 'manager_approved': True})

    def action_director_approve(self):
        for contract in self:
            if contract.state != 'manager_approve':
                raise exceptions.UserError("Hợp đồng không ở trạng thái Chờ Quản lý phê duyệt.")
            if not self.env.user.has_group('base.group_user'):
                raise exceptions.AccessError("Chỉ Giám đốc được phép phê duyệt.")
            contract.write({'state': 'director_approve', 'director_approved': True})

    def action_approve(self):
        for contract in self:
            if contract.state != 'director_approve':
                raise exceptions.UserError("Hợp đồng không ở trạng thái Chờ Giám đốc phê duyệt.")
            if not self.env.user.has_group('base.group_user'):
                raise exceptions.AccessError("Chỉ Giám đốc được phép phê duyệt cuối cùng.")
            contract.write({'state': 'approved'})



    @api.model
    def create(self, vals_list):
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            raise exceptions.AccessError("Chỉ Sale được phép tạo hợp đồng.")
        return super(Contract, self).create(vals_list)

    def write(self, vals):
        # Quy định quyền chỉnh sửa dựa trên trạng thái
        for contract in self:
            if contract.state in ['manager_approve', 'director_approve', 'approved']:
                raise exceptions.UserError("Không thể chỉnh sửa hợp đồng ở trạng thái này.")
            if contract.state == 'draft' and not self.env.user.has_group('sales_team.group_sale_salesman'):
                raise exceptions.AccessError("Chỉ Sale được phép chỉnh sửa hợp đồng ở trạng thái Nháp.")
        return super(Contract, self).write(vals)


