from odoo import http
from odoo.http import request

class StockOpnameController(http.Controller):

    @http.route('/get/request-warehouse', type='json', auth='user', methods=['POST'])
    def get_stock_opname(self):
        stock_opname = request.env['request.warehouse'].sudo().search([])
        result = []
        for opname in stock_opname:
            result.append({
                'id': opname.id,
                'name': opname.name,
                'request_date': opname.request_date,
                'received_date': opname.received_date,
                'state': opname.state,
            })
        
        return {'stock_opname': result}

    @http.route('/get/request-warehouse/<int:id>', type='json', auth='user', methods=['POST'])
    def get_request_warehouse_detail(self, id):
        request_warehouse = request.env['request.warehouse'].sudo().search([('id', '=', id)], limit=1)
        result = {
            'id': request_warehouse.id,
            'name': request_warehouse.name,
            'request_date': request_warehouse.request_date,
            'received_date': request_warehouse.received_date,
            'required_date': request_warehouse.required_date,
            'state': request_warehouse.state,
            'request_line': 
            [
                {
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'division': [
                                    {
                                        dvs.name,
                                    } for dvs in line.division_ids
                                ],
                    'product_qty': line.quantity_id.name,
                    'units': line.units,
                    'total_units': line.total_units,
                    'is_received': line.is_received,
                    'received_qty': line.received_qty,
                } for line in request_warehouse.request_line_ids
            ]
            # ...other fields as needed...
        }
        
        return {'request_warehouse': result}
