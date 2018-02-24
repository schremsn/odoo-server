# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class Commission(models.Model):
    _name="commission"

    @api.multi
    def calculate(self):
        arrAgents = []
        arrProducts = []
        arrSchemes = []
        arrSaleLine = []
        dicAgents = dict()
     
        m_group = self.env['commission.group']
        groups = m_group.search([('active', '=', True)])
    
        # find all sales people with commission configured
        for group in groups:
            for id in group.salesperson_ids:
                dicAgents.update({id.id : id.id})
                arrAgents = dicAgents.keys()
                self.calc_for_user(id.id)
        
       
        """
        for agent in arrAgents:
            print(agent)
            lines = self.env['sale.order.line'].search([('salesman_id', '=', agent), ('product_id', 'in', arrProducts)])
            for line in lines:
                print(line.product_uom_qty)

        tiers = self.env['commission.tier'].search([('activeFrom', '<=', today), ('activeEnd', '>=', today)])
        for tier in tiers:
            print(tier.type)
        """
        # m_orderline = self.pool['sale.order.line']
        

    @api.model
    def calc_for_user(self, user_id):
        today = datetime.date.today()
        calc_time = datetime.datetime.now()
        arr_scheme_ids = []
        arr_product_ids = []
        arr_tiers = []
        arr_triggers = [0, 0] # contains sales qty, total price pair for product
        dict_lines = dict()
        dict_schemes = dict()
        prod_id = 0

        print('user: %s' % (user_id))

        #last_summary = self.env['commission.summary'].search([('salesagent', '=', user_id)])
        self.env.cr.execute('select "end_date" from "commission_summary" order by "end_date" desc limit 1')
        start_time = self.env.cr.fetchone()
        print(start_time)

        # find schemes for the user
        groups = self.env['commission.group'].search([('active', '=', True), ('salesperson_ids', '=', user_id)])
        for group in groups:
            for id in group.scheme_ids:
                arr_scheme_ids.append(id.id)
                dict_schemes.update({id.id : group.id})

         # find all product with commission configured
        schemes = self.env['commission.scheme'].search([('active', '=', True), ('id', 'in', arr_scheme_ids)])
        for scheme in schemes:
            arr_product_ids.append(scheme.product.id)
            for id in scheme.tier_ids:
                arr_tiers.append(id.id)

        # find order lines with product applicable for commssion
        lines = self.env['sale.order.line'].search([('salesman_id', '=', user_id), ('product_id', 'in', arr_product_ids), ('write_date', '>', start_time)])
        for line in lines:
            prod_id = line.product_id.id
            if prod_id in dict_lines.keys():
                arr_triggers = dict_lines.get(prod_id)
                qty = arr_triggers[0]
                value = arr_triggers[1]
                qty += line.product_uom_qty
                value += line.price_total
                arr_triggers[0] = qty
                arr_triggers[1] = value
                dict_lines.update({prod_id : arr_triggers})
            else:
                arr_triggers[0] = line.product_uom_qty
                arr_triggers[1] = line.price_total
                dict_lines.update({prod_id : arr_triggers})

        # all commssion schemes/tiers for sold product
        for key in dict_lines.keys():
            arr_triggers = dict_lines.get(key)
            arr_tiers = []
            arr_details = []
            amount = 0.0

            schemes = self.env['commission.scheme'].search([('active', '=', True), ('product', '=', key)])
            for scheme in schemes:     
                arr_schemes = [] 
                rate = 0.0
                tiers = scheme.tier_ids
                # find eligable tiers based on type and sales qty/price
                for tier in tiers:
                    # if commission based skip
                    if(tier.trigger == 'c'):
                        continue

                    start_date = fields.Date.from_string(tier.active_from)
                    end_date = fields.Date.from_string(tier.active_end) 
                    # replace empty date fields (false)
                    if (start_date == None):
                        start_date = today
                    if (end_date == None):
                        end_date = today

                    if tier.type == 'q':
                        qty = arr_triggers[0]
                        if (qty >= tier.tier_start) and (qty <= tier.tier_end) and (start_date >= today) and (end_date <= today):
                            arr_tiers.append(tier)
                            rate = tier.amount
                            amount += qty * tier.amount
                    elif tier.type == 'v':
                        value = arr_triggers[1]
                        if (value >= tier.tier_start) and (value <= tier.tier_end) and (start_date >= today) and (end_date <= today):
                            arr_tiers.append(tier)
                            rate = tier.percent
                            amount += value * tier.percent / 100

                    dict_detail = dict()
                    dict_detail.update({'calc_datetime' : calc_time})
                    dict_detail.update({'sales_agent' : user_id})
                    dict_detail.update({'product' : key})
                    dict_detail.update({'commission_group' : dict_schemes.get(scheme.id)})
                    dict_detail.update({'commission_scheme' : scheme.id})
                    dict_detail.update({'commission_tier' : tier.id})
                    dict_detail.update({'type' : tier.type})
                    dict_detail.update({'rate' : rate})
                    dict_detail.update({'amount' : amount})
                    arr_details.append((0, 0, dict_detail))

            dict_summary = dict()
            dict_summary.update({'start_date' : calc_time})
            dict_summary.update({'end_date' : calc_time})
            dict_summary.update({'sales_agent' : user_id})
            dict_summary.update({'amount' : amount})
            dict_summary.update({'detail' : arr_details})
            
            self.env['commission.summary'].create(dict_summary)
            
            print('amount: %d for product %d ' % (amount, key))
            print('==============================')