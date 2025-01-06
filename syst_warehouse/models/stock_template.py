from odoo import _, api, fields, models

    
class OpnameTemplate(models.Model):
    _name = 'opname.template'
    _description = 'Opname Template'

    name = fields.Char('')
    template_ids = fields.One2many('opname.template.line', 'opname_template_id', string='Template')
    

class OpnameTemplateLine(models.Model):
    _name = 'opname.template.line'
    _description = 'Opname Template Line'
    
    opname_template_id = fields.Many2one('opname.template', string='Opname ID')
    product_id = fields.Many2one('product.name', string='Product')