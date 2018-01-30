# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"


    @api.model
    def pipeline_count(self):
        #self.env.cr.execute('SELECT stage_id, count(stage_id) from crm_lead where active=true group by stage_id')
        #return self.env.cr.fetchall()
        result = dict();
        crmstage = self.pool['crm.stage']
        stages = self.env['crm.stage'].search([])
        for stage in stages:
            id = stage.id
            domain = [('stage_id', '=', id), ('active', '=', 't')]
            count = self.env['crm.lead'].search_count(domain)
            result[id] = count;

        return result