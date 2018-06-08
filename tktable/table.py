# tktable/table.py: The tktable package
#
# Copyright (c) 2018, Alex Horridge
# All rights reserved.
#

import tkinter as tk
import sqlite3


class _Cell:

    def __init__(self, widget, row, column, width=10, height=5, read_only=False, color='white', justify='center',
                 header=None):
        super().__init__()
        self.width = width  # Set the cell width
        self.height = height  # Set the cell height (N/A)
        self.read_only = read_only  # Set the cell state
        self.color = color  # Set the cell background color
        self.widget = widget  # Set the parent widget (Row)
        self.justify = justify  # Set the position of text in the cell
        self.col = column  # Set the column number
        self.row = row  # Set the row number
        self.header = header  # Set the header list
        self.cell_entry = None  # Set an empty cell variable

        self.create_cell()  # Creates the cell

        self.cell_entry.grid(column=self.col, row=1)  # Add cell to a grid inside the row object
        self.cell_entry.bind('<Button-1>', self.update)  # Add a binding to get cell value

    def create_cell(self):
        """Create entry widget. If header, set a different colour and make read only."""
        if self.header:
            self.cell_entry = tk.Entry(self.widget, width=self.width, name='cell' + str(self.col), state='readonly',
                                       readonlybackground=self.color, textvariable=self.header)
        else:
            self.cell_entry = tk.Entry(self.widget, width=self.width, name='cell' + str(self.col),
                                       bg=self.color)

    def get_xy(self):
        """Return x,y coordinates of cell"""
        return tuple([self.col, self.row])

    def update(self, event):
        row = event.widget.master  # Get the parent row
        if 'header' not in str(row).split(".")[-1]:  # If the row isn't the header
            for cell in row.winfo_children():
                pass


class _Row:

    def __init__(self, table, row_num, columns=3, header=None):
        super().__init__()
        self.cols = columns  # Set the number of columns
        self.master = table  # Set the parent widget (Table)
        self.row_num = row_num  # Set the current row number
        self.header = header  # Set the header to list
        self.row = None  # Set an empty row variable

        self.create_row_name()  # Creates the row name
        self.create_cells()  # Creates the child cells

        self.row.grid(row=self.row_num)  # Add row to a grid inside the table object

    def create_row_name(self):
        """Create a row widget and names it"""
        if self.header:
            self.row = tk.Frame(self.master, name='header')
        else:
            self.row = tk.Frame(self.master, name='row' + str(self.row_num))

    def create_cells(self):
        """For each column, create a cell object. Afterwards, add the row to a grid inside the table object"""
        for column in range(self.cols):
            if self.header:
                text = tk.StringVar()
                text.set(self.header[column])
                _Cell(self.row, self.row_num, column, color='grey50', read_only=True, header=text)
            else:
                _Cell(self.row, self.row_num, column)
            self.row.grid(row=self.row_num)

    def cell_list(self):
        """Returns a list of children (Cells)"""
        return self.row.winfo_children()


class Table:
    def __init__(self, master, sql_select, conn, rows=5, columns=3, name='', header=list):
        super().__init__()
        self.master = master  # Set the parent widget
        self.sql_select = sql_select  # Set the sql select statement
        self.conn = conn  # Set the sql connection object
        self.rows = rows  # Set the number of rows
        self.cols = columns  # Set the number of columns
        self.name = name.lower()  # Set the name and make it lowercase
        self.header = header  # Set whether the table has headers
        self.table = None  # Set an empty table variable

        self.used_cols = self.table_schema()
        self.rows_in_table = self.select_sql()
        self.check_name(name)  # Checks if a name was provided
        self.create_rows()  # Create the rows in the table

        self.table.pack()  # Pack the table

    def check_name(self, name):
        """If a name has been provided, name the widget with the provided name, otherwise leave default"""
        if name:
            self.table = tk.Frame(self.master, name=self.name)
        else:
            self.table = tk.Frame(self.master)

    def create_rows(self):
        """For each row provided create a row, if it is the first row, provide header details"""
        if not self.rows_in_table:
            table_height = 0
        else:
            table_height = len(self.rows_in_table)

        for row in range(table_height + 2):
            if row == 0:
                _Row(self.table, row, len(self.used_cols))  # , self.header)
            else:
                _Row(self.table, row, len(self.used_cols))

    def get_children(self):
        """Returns a list of children (Rows)"""
        return self.table.winfo_children()

    def get_grandchildren(self):
        """Returns a list of grandchildren (Cells)"""
        grandchildren_list = []
        for child in self.table.winfo_children():
            for grandchild in child.winfo_children():
                grandchildren_list.append(grandchild)
        return grandchildren_list

    def get_row(self, row_num):
        """Returns specific row"""
        return self.table.winfo_children()[row_num]

    def update_cell_in_row(self, row_num, data):
        """Get the row in question. Check whether the data has been provided in a list format or a dictionary. If the
        data provided is a list, col[n].value = list[n]. If the data provided is a dictionary, match the headers to the
        dictionary keys and set the values at the necessary columns."""
        row = self.get_row(row_num)
        if isinstance(data, list):
            if len(row.winfo_children()) == len(data):
                for i, cell in enumerate(row.winfo_children()):
                    cell.delete(0, tk.END)
                    cell.insert(0, data[i])
        elif isinstance(data, dict):
            print('Data provided in dictionary format')
            # ToDo Match key to column header
            for cell in row.winfo_children():
                cell.delete(0, tk.END)
                cell.insert(0, 'help')

    def select_sql(self):
        cursor = self.conn.cursor()
        cursor.execute(self.sql_select)
        rows = [x for x in cursor.fetchall()]
        cursor.close()
        if not rows:
            rows = None
        return rows

    def table_schema(self):
        sql = self.sql_select.lower().split(" ")  # create a list of words in sql select statement
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(" + str(sql[sql.index('from') + 1]) + ");")
        rows = [x for x in cursor.fetchall()]  # cid, name, type, nullable, default value, pk
        cursor.close()
        used_columns = self.get_columns(sql, rows)
        return used_columns

    def get_columns(self, sql, rows):
        """Checks what columns from a table are being used and returns a list of them."""
        beginning = sql.index('select')
        end = sql.index('from')
        col_names = []
        row_info = []
        for word in range(beginning + 1, end):
            if sql[word] == '*':
                return rows
            else:
                col_names.append(sql[word].replace(',', ''))
        for col in col_names:
            for row in rows:
                if col in row:
                    row_info.append(row)
        return row_info
