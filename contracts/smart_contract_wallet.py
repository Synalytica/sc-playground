import smartpy as sp


class ErrorMessages:
    ZERO_DEPOSIT = "can not deposit zero tez"
    UNAVAILABLE_USER = "user unavailable"
    INSUFFICIENT_FUNDS = "insufficient funds"
    ZERO_WITHDRAWL = "can not withdraw zero tez"


class LedgerKey:
    def make(user):
        sp.set_type(user, sp.TAddress)
        return user


class LedgerValue:
    def get_type():
        return sp.TRecord(balance=sp.TNat)

    def make(balance):
        sp.set_type(balance, sp.TNat)
        return sp.record(balance=balance)


class Withdraw:
    def get_type():
        return sp.TRecord(amount=sp.TNat)
    
    def make(amount):
        sp.set_type(amount, sp.TNat)
        return sp.record(amount=amount)


class TezWallet(sp.Contract):
    def __init__(self):
        self.init(
            ledger = sp.Map(tvalue = LedgerValue.get_type())
        )

    def _verify_user_available(self, user):
        key = LedgerKey.make(user)
        sp.verify(self.data.ledger.contains(key), message=ErrorMessages.UNAVAILABLE_USER)

    def _get_balance(self, user):
        key = LedgerKey.make(user)
        sp.result(self.data.ledger[key].balance)

    def _deposit(self, user, amount):
        key = LedgerKey.make(user)
        sp.if self.data.ledger.contains(key):
            self.data.ledger[key].balance += amount
        sp.else:
            self.data.ledger[key] = LedgerValue.make(amount)
    
    def _withdraw(self, user, amount):
        key = LedgerKey.make(user)
        self.data.ledger[key].balance -= amount

    @sp.entry_point
    def deposit(self):
        sp.verify(sp.amount > 0, message=ErrorMessages.ZERO_DEPOSIT)

        self._deposit(sp.sender, sp.amount)

    @sp.entry_point
    def withdraw(self, params):
        sp.set_type(params, Withdraw.get_type())

        self._verify_user_availability(sp.sender)
        sp.verify(sp.amount > 0, message=ErrorMessages.ZERO_WITHDRAWL)
        sp.verify(self._get_balance(sp.sender) >= params.amount, message=ErrorMessage.INSUFFICIENT_FUNDS)

        self._withdraw(sp.sender, params.amount)
        sp.send(sp.sender, params.amount)


    @sp.utils.view(sp.TNat)
    def get_balance(self):
        self._verify_user_availability(sp.sender)

        sp.result(self._get_balance(sp.sender))
