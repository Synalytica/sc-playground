# coding: utf-8
"""
    :author: tichnas
    :brief: Shows usage of smart contract factory with other important stuff like type constraints, sub entry points, etc.
"""
import smartpy as sp

class Fund(sp.Contract):
    def __init__(self, admin, name = '', managers = []):
        self.init_type(sp.TRecord(
            admin = sp.TAddress,
            name = sp.TString,
            managers = sp.TList(sp.TAddress)
        ))
        
        self.init(
            admin = admin,
            name = name,
            managers = managers
        )
        
    @sp.sub_entry_point
    def is_authorized(self, _):
        authorized = sp.local('authorized', sp.sender == self.data.admin)
        
        sp.for manager in self.data.managers:
            sp.if sp.sender == manager:
                authorized.value = True
        
        
        sp.result(authorized.value)
        
    @sp.entry_point
    def update_name(self, name):
        sp.verify(self.is_authorized(sp.unit), message='Not authorized')
        
        sp.set_type(name, sp.TString)
        
        self.data.name = name
        
    @sp.entry_point
    def add_manager(self, manager):
        sp.verify(self.is_authorized(sp.unit), message='Not authorized')
        
        sp.set_type(manager, sp.TAddress)
        
        self.data.managers.push(manager)

class FundFactory(sp.Contract):
    def __init__(self, admin):
        self.init_type(sp.TRecord(
            admin = sp.TAddress,
            funds = sp.TList(sp.TAddress)
        ))
        
        self.init(
            admin = admin,
            funds = []
        )
        
        self.fund = Fund(admin = admin)
    
    @sp.entry_point
    def add_fund(self, name, managers):
        sp.verify(sp.sender == self.data.admin)
        
        sp.set_type(name, sp.TString)
        sp.set_type(managers, sp.TList(sp.TAddress))
        
        storage = sp.record(
            admin = self.data.admin,
            name = name,
            managers = managers
        )
        
        self.data.funds.push(sp.create_contract(contract=self.fund, storage=storage))


@sp.add_test(name = "Calculator")
def test():
    admin = sp.test_account('admin')
    manager1 = sp.test_account('manager1')
    manager2 = sp.test_account('manager2')
    
    scenario = sp.test_scenario()
    
    factory = FundFactory(admin=admin.address)
    scenario += factory
    scenario += factory.fund
    
    # non admin trying to create a new fund
    factory.add_fund(name='fund', managers=[]).run(sender=manager1.address, valid=False)
    
    # admin creates 2 new funds
    factory.add_fund(name='fund0', managers=[manager1.address]).run(sender=admin.address)
    factory.add_fund(name='fund1', managers=[]).run(sender=admin.address)
    
    scenario.verify(sp.len(factory.data.funds) == 2)
    
    fund0 = scenario.dynamic_contract(0, factory.fund)
    fund1 = scenario.dynamic_contract(1, factory.fund)
    
    # unauthorized trying to rename fund
    fund0.call('update_name', 'fundRenamed').run(sender=manager2.address, valid=False)
    
    # manager renaming
    fund0.call('update_name', 'renamedByManager').run(sender=manager1.address)
    scenario.verify(fund0.data.name == 'renamedByManager')
    
    # admin renaming
    fund0.call('update_name', 'renamedByAdmin').run(sender=admin.address)
    scenario.verify(fund0.data.name == 'renamedByAdmin')
    
    scenario.verify(fund1.data.name == 'fund1')
    
    # unauthorized trying to add new manager
    fund0.call('add_manager', manager2.address).run(sender=manager2.address, valid=False)
    
    # authorized adding new manager
    fund0.call('add_manager', manager2.address).run(sender=manager1.address)
    
    # new manager renaming fund
    fund0.call('update_name', 'fundRenamed').run(sender=manager2.address)
    scenario.verify(fund0.data.name == 'fundRenamed')
    