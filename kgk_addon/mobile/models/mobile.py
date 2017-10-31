# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customer(models.Model):
    _name = "mobile.customer"
    _inherits = "res.partner, crm.lead"

