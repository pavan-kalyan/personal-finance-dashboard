from utils import format_time


class User:
    def __init__(self, id, name, email, password, created_at=None, updated_at=None, date_of_birth=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.date_of_birth = date_of_birth
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def to_json(self):
        return {"name": self.name,
                "email": self.email}

    def get_id(self):
        return str(self.id)

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        user = User(id=row['id'], name=row['name'], email=row['email'],
                    password='password', created_at=row['created_at'],
                    updated_at=format_time(row['updated_at']),
                    date_of_birth=row['date_of_birth']
                    )
        return user
