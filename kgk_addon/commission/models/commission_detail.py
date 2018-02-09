# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_detail(models.Model):
    _name = 'commission.detail'
    _description = 'Detailed commission history'
    #track commssion calculation for each sold product with link to the tier used

    calc_datetime = fields.Datetime(string = 'Calculation date', required=True)
    sales_agent = fields.Many2one('res.users', required=True, string = 'Sales agent')
    product = fields.Many2one('sales.order.line', required=True)
    commission_group = fields.Many2one('commssion.group', required=True)
    commission_scheme = fields.Many2one('commission_scheme', required=True)
    commssion_tier = fields.Many2one('commission_tier', required=True)
    type = fields.Char(string ='Type')
    rate = fields.Float(string = 'Rate')
    amount = fields.Float(string = 'Amount')