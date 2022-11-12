class Transaction:
    def __init__(self, id, amount, account_id, account_name, account_number, contact, contact_id, category, category_id, memo, date=None, created_at=None, updated_at=None):
        self.id = id
        self.amount = amount
        self.account_id = account_id
        self.account_name = account_name
        self.account_number = account_number
        self.contact = contact
        self.contact_id = contact_id
        self.category = category
        self.category_id = category_id
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
                                  updated_at=row['updated_at'] if row['updated_at'] is not None else "",
                                  account_id=row['account_id'],
                                  account_name=row['account_name'],
                                  account_number=row['account_number'],
                                  contact=(row['contact'] if row['contact'] is not None else ""),
                                  contact_id=(row['contact_id'] if row['contact_id'] is not None else ""),
                                  category=(row['category'] if row['category'] is not None else ""),
                                  category_id=(row['category_id'] if row['category_id'] is not None else ""),
                                  memo=(row['memo'] if row['memo'] is not None else "")
                                  )
        return transaction
