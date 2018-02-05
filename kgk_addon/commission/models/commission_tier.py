# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_tier(models.Model):
    _name = 'commission.tier'
    _description = 'Define commission tiers'

    type = fields.Selection((('v','Value'), ('q','Quantity')), string='Calculation base', required = True)
    tierStart = fields.Integer(string='Start value', default=0)
    tierEnd = fields.Integer(string = 'Start value')
    amount = fields.Float(string = 'Commission amount')
    percent = fields.Float(string = 'Commission percent')
    trigger = fields.Selection((('s', 'Sales'), ('c', 'Commission')), string = 'Triggered by' )
    activeFrom = fields.Datetime(string = 'Start date')
    activeEnd = fields.Datetime(string = 'End date')
    scheme = fields.Many2one('commission.scheme')