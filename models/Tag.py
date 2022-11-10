class Tag:
    def __init__(self, id, name, uid):
        self.id = id
        self.uid = uid
        self.name = name

    def to_json(self):
        return {"name": self.name}

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        tag = Tag(id=row['id'],
                  uid=row['uid'],
                  name=row['name']
                  )
        return tag
