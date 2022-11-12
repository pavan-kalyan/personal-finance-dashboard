class Transaction:
    def __init__(self, id, amount, account_name, account_number, contact, category, memo, date=None, created_at=None, updated_at=None):
        self.id = id
        self.amount = amount
        self.account_name = account_name
        self.account_number = account_number
        self.contact = contact
        self.category = category
        self.memo = memo
        self.date = date
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {"account": self.account_name,
                "contact": self.contact,
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
                                  account_name=row['account_name'],
                                  account_number=row['account_number'],
                                  contact=(row['contact'] if row['contact'] is not None else ""),
                                  category=(row['category'] if row['category'] is not None else ""),
                                  memo=(row['memo'] if row['memo'] is not None else "")
                                  )
        return transaction
