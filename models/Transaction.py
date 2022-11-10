class Transaction:
    def __init__(self, id, amount,  account_id, contact_id, category_id, memo, date=None, created_at=None, updated_at=None):
        self.id = id
        self.amount = amount
        self.account_id = account_id
        self.contact_id = contact_id
        self.category_id = category_id
        self.memo = memo
        self.date = date
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {"account": self.account_id,
                "contact": self.contact_id,
                "amount": self.amount,
                "memo": self.memo}

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        transaction = Transaction(id=row['id'],
                                  amount=row['amount'],
                                  date=row['date'],
                                  created_at=row['created_at'],
                                  updated_at=row['updated_at'],
                                  account_id=row['account_id'],
                                  contact_id=row['contact_id'],
                                  category_id=row['category_id'],
                                  memo=row['memo']
                                  )
        return transaction
