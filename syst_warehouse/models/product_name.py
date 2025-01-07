from odoo import _, api, fields, models

class ProductName(models.Model):
    """Model untuk Nama Produk."""
    _name = 'product.name'
    _description = 'Product Name'
    _order = 'sequence'

    sequence = fields.Integer('')
    name = fields.Char('')
    # Foreign Key to Quantity Warehouse
    quantity_id = fields.Many2one('quantity.warehouse', string='Quantity')
    units = fields.Integer('')
    request_count = fields.Integer('Request Count', compute='_get_total_request')
    onhand_count = fields.Integer('Onhand Count', compute='_get_total_request')
    
    request_line_ids = fields.One2many('request.line', 'product_id', string='Request Line')

    def _get_total_request(self):
        """
        Menghitung total jumlah permintaan dan total unit yang tersedia.
        """
        self.request_count = len(self.request_line_ids)
        self.onhand_count = sum(self.request_line_ids.mapped('total_units'))

    def _compute_display_name(self):
        """
        Menghitung nama tampilan produk.
        """
        for product in self:
            if product.name:
                product.display_name = product.name + " [%s]" % (product.units)
            else:
                product.display_name = False

    def action_view_onhands(self):
        """Mengembalikan aksi untuk melihat jumlah unit yang tersedia dari produk."""
        return {
            'name': 'On Hands',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'current',
            'views': [(self.env.ref('syst_warehouse.request_line_ohands_view_tree').id, 'tree')],
            'res_model': 'request.line',
            'domain': [("product_id", "=", self.id)],
        }

