from odoo import _, api, fields, models

class ProductName(models.Model):
    _name = 'product.name'
    _description = 'Product Name'
    _order ='sequence'

    sequence = fields.Integer('')
    name = fields.Char('')
    quantity_id = fields.Many2one('quantity.warehouse', string='Quantity')
    units = fields.Integer('')
    request_count = fields.Integer('Request Count',compute='_get_total_request')
    onhand_count = fields.Integer('Onhand Count',compute='_get_total_request')
    request_line_ids = fields.One2many('request.line', 'product_id', string='Request Line')

    def _get_total_request(self):
        self.request_count = len(self.request_line_ids)
        self.onhand_count = sum(self.request_line_ids.mapped('total_units'))

    def _compute_display_name(self):
        for product in self:
            if product.name:
                product.display_name = product.name + " [%s]" % (product.units)
            else:
                product.display_name = False

    def action_view_onhands(self):
        return {
            'name': 'On Hands',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'current',
            'views': [(self.env.ref('syst_warehouse.request_line_ohands_view_tree').id, 'tree')],
            'res_model': 'request.line',
            'domain': [("product_id", "=", self.id)],
        }    
        
