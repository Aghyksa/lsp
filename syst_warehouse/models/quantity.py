from odoo import _, api, fields, models

class QuantityWarehouse(models.Model):
    _name = 'quantity.warehouse'
    _description = 'Quantity Warehouse'
    _order = 'sequence'

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique!'),
        ('unique_code', 'unique(code)', 'The code must be unique!')
    ]
    
    sequence = fields.Integer('')
    name = fields.Char('')
    code = fields.Char('')