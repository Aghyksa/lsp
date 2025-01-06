from odoo import _, api, fields, models

class DivisionWarehouse(models.Model):
    _name = 'division.warehouse'
    _description = 'Division Warehouse'
    _order = 'sequence'

    sequence = fields.Integer('')
    name = fields.Char('')
    color = fields.Integer('')