
# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
import datetime

class TestCommission(TransactionCase):
  prod_id1 = 1
  prod_id2 = 2
  agent_id1 = 5
  agent_id2 = 10
  manager_id1 = 1
  manager_id2 = 9

  # set basic data
  def setUp(self, *args, **kwargs):
    super(TestCommission, self).setUp(*args, **kwargs)
    # set all groups to inactive
    self.env['commission.group'] \
      .search([('active', '=', True)]) \
      .write({'active' : False})

    # set all schemes inactive
    self.env['commission.scheme'] \
      .search([('active', '=', True)]) \
      .write({'active': False})

  # test the setup of schmes
  def test_populate_scheme(self):
    self.populate_scheme()

    count = len(self.env['commission.group'].search([('name', '=', 'manager')]))
    self.assertEqual(count, 1, 'group assertions')

  # create the cimmission hierarchy
  def test_populate_hierarchy(self):
    self.populate_hierarchy()

  # create the tiers, schemes and groups
  def populate_scheme(self):
    # use demo user
    demo_user = self.env.ref('base.user_demo')

    # create two schemes for two products with two tiers each
    tier1 = {
      'type' : 'q',
      'tier_start' : 0,
      'tier_end' : 2,
      'trigger' : 's',
      'amount' : 20
    }
    tier2 = {
      'type' : 'q',
      'tier_start' : 3,
      'tier_end' : 9,
      'trigger' : 's',
      'amount' : 30
    }
    scheme = self.env['commission.scheme']
    self.scheme1 = scheme.create({
      'name' : 'scheme1',
      'active' : True,
      'product' : self.prod_id1,
      'tier_ids' : ((0, 0, tier1), (0, 0, tier2))
    })

    tier3 = {
      'type' : 'q',
      'tier_start' : 0,
      'tier_end' : 2,
      'trigger' : 's',
      'amount' : 20
    }
    tier4 = {
      'type' : 'q',
      'tier_start' : 3,
      'tier_end' : 9,
      'trigger' : 's',
      'amount' : 30
    }

    self.scheme2 = scheme.create({
      'name' : 'scheme2',
      'active' : True,
      'product' : self.prod_id2,
      'tier_ids' : ((0, 0, tier3), (0, 0, tier4))
    })

    tier = self.env['commission.tier']

    count = len(scheme.search([('active', '=', True)]))
    self.assertEqual(count, 2, 'error creating schemes')

    count = len(tier.search([('scheme.id', 'in', [self.scheme1.id, self.scheme2.id])]))
    self.assertEqual(count, 4, 'error creating agent tiers')

    # create manager commission scheme
    tier5 = {
      'type' : 'q',
      'tier_start' : 0,
      'tier_end' : 99,
      'trigger' : 'c',
      'percent' : 5.0
    }

    self.scheme3 = scheme.create({
      'name' : 'manager scheme',
      'active' : True,
      'product' : self.prod_id1,
      'tier_ids' : [(0, 0, tier5)]
    })

    # create two commission group
    group = self.env['commission.group']
    self.group1 = group.create({
      'name' : 'manager',
      'active' : True
    })
    self.group2 = group.create({
      'name' : 'agent',
      'active' : True,
    })

    self.group2.scheme_ids += self.scheme1
    self.group2.scheme_ids += self.scheme2
    self.group1.scheme_ids += self.scheme3

    count = len(scheme.search([('active', '=', True)]))
    self.assertEqual(count, 3, 'error creating manager schemes')

    count = len(tier.search([('scheme.id', 'in', [self.scheme3.id])]))
    self.assertEqual(count, 1, 'error creating manager tiers')

    count = len(group.search([('active', '=', True)]) )
    self.assertEqual(count, 2, 'wrong group count')

  # create the commission hierarchy
  def populate_hierarchy(self):
    hierarchy = self.env['commission.hierarchy']

    self.node1 = hierarchy.create({
      'name' : 'hq',
      'team' : 4
    })
    self.node2 = hierarchy.create({
      'name' : 'region1',
      'parent_id' : self.node1.id,
      'team' : 5
    })
    self.node3 = hierarchy.create({
      'name': 'team lead1',
      'parent_id' : self.node2.id,
      'team' : 6
    })
    self.node4 = hierarchy.create({
      'name' : 'team1',
      'parent_id' : self.node3.id,
      'team' : 1
    })

    count = len(hierarchy.search([('id', '>=', self.node1.id)]))
    self.assertEqual(count, 4, 'creating hierarchy')
