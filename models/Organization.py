class Organization:
    def __init__(self, id, name, location, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.location = location
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {"name": self.name,
                "location": self.location}

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        org = Organization(id=row['id'],
                           name=row['name'],
                           location=row['location'],
                           created_at=row['created_at'],
                           updated_at=row['updated_at'],
                           )
        return org
