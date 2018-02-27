
# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase

class TestCommission(TransactionCase):
  def setUp(self, *args, **kwargs):
    super(TestCommission, self).setUp(*args, **kwargs)
    # set all groups to inactive
    results = self.env['commission.group'].search([('active', '=', True)]) 
    for result in results:
      result.write({'active' : False})

    # use demo user
    demo_user = self.env.ref('base.user_demo')

    # create two commission group
    """
    group = self.env['commission.group']
    self.group1 = group.create({
      'name' : 'manager',
      'active' : True
    })
    self.group2 = group.create({
      'name' : 'agent',
      'active' : true
    })

    count = len(self.group.id)
    self.asserEqual(count, 3, 'wrong group count')
    """
    print('setup')


  def test_populate_group(self):
    #create two commission groups
    print('test')
    # create two commission group
    group = self.env['commission.group']
    self.group1 = group.create({
      'name' : 'manager',
      'active' : True
    })
    self.group2 = group.create({
      'name' : 'agent',
      'active' : True
    })

    count = len(group.search([('active', '=', True)]) )
    self.assertEqual(count, 2, 'wrong group count')
    
