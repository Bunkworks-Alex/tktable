from tkinter import Tk, Canvas, BOTH, Entry
from tktable.table import *
import sqlite3


class TestForm(Tk):

    def __init__(self):
        super().__init__()

        self.title('Test Table')
        self.test_frame = Canvas(self, width=400, height=400)
        self.test_frame.pack_propagate(0)
        self.test_frame.pack(fill=BOTH, expand=1)
        self.conn = sqlite3.connect('local.db')
        self.create_table()

        tab = Table(self.test_frame, 'SELECT * FROM test', self.conn)

        # Tab = Table(self.test_frame, 10, 5, header=['ID', 'First Name', 'Last Name', 'Phone', 'Email'])
        # Tab.update_cell_in_row(1, ['ID', 'First Name', 'Last Name', 'Phone', 'Email'])
        # print(Tab.get_children())
    def create_table(self):
        cursor = self.conn.cursor()
        create_version_sql = """ CREATE TABLE IF NOT EXISTS test (
                                        test_id integer PRIMARY KEY,
                                        test_name TEXT NOT NULL,
                                        test_location TEXT NOT NULL
                                        ); """
        cursor.execute(create_version_sql)
        cursor.close()


if __name__ == '__main__':
    test_app = TestForm()
    test_app.mainloop()
