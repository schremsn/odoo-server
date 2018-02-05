# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_scheme(models.Model):
    _name = 'commission.scheme'
    _description = 'Define commission scheme'

    name = fields.Char(string = 'Name of scheme', required = True, size = 30)
    active = fields.Boolean(string = 'Active?', required = True, default=True)
    product = fields.Many2one('product.product', required = True, string = 'Product')
    tier_ids = fields.Many2one('commission.tier', string = 'Commission tiers')