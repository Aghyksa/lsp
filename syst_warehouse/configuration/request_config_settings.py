from odoo import _, api, fields, models


class RequestConfigSettings(models.TransientModel):
    _name = 'request.config.settings'
    _inherit = 'res.config.settings'
    _description = 'Request Config'

    confirmation_button = fields.Boolean('Confirmation Button',config_parameter="syst_warehouse.confirmation_button")
    set_to_draft_button = fields.Boolean('Set To Draft',config_parameter="syst_warehouse.set_to_draft_button")
    request_tooltip = fields.Text(compute="_compute_tooltip_request")
    
    @api.depends('confirmation_button', 'set_to_draft_button')
    def _compute_tooltip_request(self):
        self._onchange_button()

    @api.onchange('confirmation_button','set_to_draft_button')
    def _onchange_button(self):
        string = ""
        if self.confirmation_button:
            string = "- Every button for step up need confirmation." + "\n"
        if self.set_to_draft_button:
            string += "- Button Set To Draft will appear."
        self.request_tooltip = string 