from odoo import _, api, fields, models

class OpnameStock(models.Model):
    _name = 'opname.stock'
    _description = 'opname.stock'
    
    name = fields.Char('')
    date = fields.Date('Date',default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
    ], string='state',default='draft')
    opname_template_id = fields.Many2one('opname.template', string='Opname Template')
    line_ids = fields.One2many('opname.stock.line','opname_id',string='Line')

    @api.onchange('opname_template_id')
    def _get_default_opname_line(self):
        self.line_ids = [(5, 0, 0)]  # Clear existing lines
        if self.opname_template_id:
            lines = []
            for template_line in self.opname_template_id.template_ids:
                line = {
                    'product_id': template_line.product_id.id,
                }
                lines.append((0, 0, line))
            self.line_ids = lines
    

class OpnameStockLine(models.Model):
    _name = 'opname.stock.line'
    _description = 'Opname Stock Line'

    opname_id = fields.Many2one('opname.stock', string='Opname ID')
    product_id = fields.Many2one('product.name', string='Product')
    quantity_id = fields.Many2one('quantity.warehouse', string='Packaging')
    product_qty = fields.Integer('Quantity')