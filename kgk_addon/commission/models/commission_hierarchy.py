# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_hierarchy(models.Model):
    _name = 'commission.hierarchy'
    _description = 'sales person hierarchy'
    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_id'

    name = fields.Char(string = 'Node', required = True, size = 30, Translate = True)
    parent_id = fields.Many2one('commission.hierarchy', 'Parent node', index=True, ondelete='restrict')
    child_id = fields.One2many('commission.hierarchy', 'parent_id', 'Child nodes')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)