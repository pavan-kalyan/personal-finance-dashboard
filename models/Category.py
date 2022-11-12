class Category:
    def __init__(self, id, uid, name, group, created_at=None, updated_at=None):
        self.id = id
        self.uid = uid
        self.name = name
        self.group = group
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return {"name": self.name,
                "group": self.group}

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        category = Category(id=row['id'],
                            uid=row['uid'],
                            name=row['name'],
                            group=row['group'],
                            created_at=row['created_at'],
                            updated_at=row['updated_at'],
                            )
        return category
