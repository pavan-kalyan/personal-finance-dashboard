from utils import format_time
class Contact:
    def __init__(self, id, uid, name, email, created_at=None, updated_at=None):
        self.id = id
        self.uid = uid
        self.name = name
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {"name": self.name,
                "email": self.email}

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        contact = Contact(id=row['id'],
                          uid=row['uid'],
                          name=row['name'],
                          email=row['email'],
                          created_at=format_time(row['created_at']),
                          updated_at=format_time(row['updated_at'])
                          )
        return contact
