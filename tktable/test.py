from tkinter import Tk, Canvas, BOTH, Entry
from tktable.table import *


class TestForm(Tk):

    def __init__(self):
        super().__init__()

        self.title('Test Table')
        self.test_frame = Canvas(self, width=400, height=400)
        self.test_frame.pack_propagate(0)
        self.test_frame.pack(fill=BOTH, expand=1)

        Tab = Table(self.test_frame, 10, 5, header=True)
        Tab.update_cell_in_row(2, [1, 2, 3, 4, 5])


if __name__ == '__main__':
    test_app = TestForm()
    test_app.mainloop()