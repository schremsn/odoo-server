
class CommissionData():
  prod_id1 = 1
  prod_id2 = 2
  agent_id1 = 5
  agent_id2 = 10
  manager_id1 = 1
  manager_id2 = 9
  
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

  scheme_a1 = {
    'name' : 'scheme1',
    'active' : True,
    'product' : prod_id1,
    'tier_ids' : ((0, 0, tier1), (0, 0, tier2))
  }

  scheme_a2 = {
    'name' : 'scheme2',
    'active' : True,
    'product' : prod_id2,
    'tier_ids' : ((0, 0, tier3), (0, 0, tier4))
  }

  tier5 = {
    'type' : 'q',
    'tier_start' : 0,
    'tier_end' : 99,
    'trigger' : 'c',
    'percent' : 5.0
  }

  scheme_m1 = {
    'name' : 'manager scheme',
    'active' : True,
    'product' : prod_id1,
    'tier_ids' : [(0, 0, tier5)]
  }