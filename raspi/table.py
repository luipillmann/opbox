class Table(object):
    """A class that makes the table."""
    def __init__(self, name, rows=None):
        self.name = name
        self.rows = rows or []

    def add_row(self, row):
        self.rows.append(row)
        # if row.parent != self:
        #     row.parent = self

    def add_rows(self, rows):
        for row in rows:
            self.add_row(row)
        # if row.parent != self:
        #     row.parent = self

    def remove_row(self, row):
        self.rows.remove(row)
        # if row.parent == self:
        #     row.parent = None