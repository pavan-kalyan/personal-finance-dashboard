class Account:
    def __init__(self, id, type, name, balance, account_number, org_id, uid, created_at=None, updated_at=None, ):
        self.id = id
        self.type = type
        self.name = name
        self.balance = balance
        self.account_number = account_number
        self.org_id = org_id
        self.uid = uid
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {"name": self.name,
                "type": self.type,
                "balance": self.balance}

    def get_id(self):
        return str(self.id)

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        account = Account(id=row['id'],
                          type=row['type'],
                          name=row['name'],
                          balance=row['balance'],
                          account_number=row['account_number'],
                          org_id=row['org_id'],
                          uid=row['uid'],
                          created_at=row['created_at'],
                          updated_at=row['updated_at'],
                          )
        return account