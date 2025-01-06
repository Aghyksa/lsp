from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class RequestWarehouse(models.Model):
    _name = 'request.warehouse'
    _description = 'Request Order'
    _inherit = ['mail.thread','mail.activity.mixin','analytic.mixin']


    name = fields.Char('',tracking=True)
    state = fields.Selection([
    ('draft', 'Draft'),
    ('delivery', 'On Delivery'),
    ('received', 'Received'),
    ], string='State',default="draft",tracking=True)
    request_date = fields.Date('Request Date',default=fields.Date.today(),tracking=True)
    required_date = fields.Date('Required Date',tracking=True)
    received_date = fields.Date('Received Date',tracking=True)
    request_line_ids = fields.One2many('request.line', 'request_warehouse_id', string='Warehouse')
    is_confirmation = fields.Boolean(compute="_compute_config_request")
    is_set_to_draft = fields.Boolean(compute="_compute_config_request")

    @api.depends('is_confirmation','is_set_to_draft')
    def _compute_config_request(self):
        ir_config = self.sudo().env['ir.config_parameter']
        self.is_confirmation = ir_config.get_param('syst_warehouse.confirmation_button')
        self.is_set_to_draft = ir_config.get_param('syst_warehouse.set_to_draft_button')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('request.warehouse')
        return super().create(vals)


    def action_delivery(self):
        if not self.request_line_ids: raise UserError("There's no item on request")
        self.write({
            'state': 'delivery',
        })

    def action_draft(self):
        self.write({
            'state': 'draft',
        })

    def action_receive(self):
        self.write({
            'state': 'received',
            'received_date':fields.Date.today(),
        })
        for line in self.request_line_ids:
            line.received_qty = line.total_units
class RequestLine(models.Model):
    _name = 'request.line'
    _description = 'Request Line'
    _order = 'sequence'

    sequence = fields.Integer('')
    name = fields.Char('')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('delivery', 'On Delivery'),
        ('received', 'Received'),
    ], string='State',related="request_warehouse_id.state")

    product_id = fields.Many2one('product.name', string='Product Name')
    division_ids= fields.Many2many('division.warehouse', string='Division')
    quantity_id = fields.Many2one('quantity.warehouse', string='Quantity')
    units = fields.Integer('Units')
    total_units = fields.Integer('Total Units')
    request_warehouse_id = fields.Many2one('request.warehouse', string='Request Order', ondelete='cascade')
    request_date = fields.Date('Request Date',related='request_warehouse_id.request_date',store=True)
    is_received = fields.Boolean('Received',default=True)
    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
    ], default=False)
    received_qty = fields.Integer('Received Qty')

    @api.onchange('product_id','units')
    def _onchange_quantity_prdct(self):
        self.quantity_id = self.product_id.quantity_id
        self.total_units = self.product_id.units * self.units
        self.request_date = self.request_warehouse_id.request_date

    def open_request(self):
        return {
            'name': 'Request Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.request_warehouse_id.id,
            'res_model': 'request.warehouse',
            'context': {'default_index': self.id, 'default_model': self._name}
        }    
    def action_check(self):
        self.write({
            'is_received': True
        })