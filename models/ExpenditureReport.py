class ExpenditureReport:
    def __init__(self, year, month, category_name, total_expenditure,
                 most_expensive_transaction):
        self.year = year
        self.month = month
        self.category_name = category_name
        self.total_expenditure = total_expenditure
        self.most_expensive_transaction = most_expensive_transaction

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        report_row = ExpenditureReport(
            category_name=row['category_name'],
            year=int(row['year']),
            month=int(row['month']),
            total_expenditure=row['total_expenditure'],
            most_expensive_transaction=row['most_expensive_transaction']
        )
        return report_row
