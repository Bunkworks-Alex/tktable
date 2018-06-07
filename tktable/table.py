# -*- coding: utf-8 -*-
# Copyright (c) 2018, Alex Horridge
# All rights reserved.

import tkinter as tk


class _Cell:

    def __init__(self, widget, row, column, width=10, height=5, read_only=False, color='white', justify='center'):
        super().__init__()
        self.width = width  # Set the cell width
        self.height = height  # Set the cell height (N/A)
        self.read_only = read_only  # Set the cell state
        self.color = color  # Set the cell background color
        self.widget = widget  # Set the parent widget (Row)
        self.justify = justify  # Set the position of text in the cell
        self.col = column  # Set the column number
        self.row = row  # Set the row number

        if read_only:
            self.cell_entry = tk.Entry(self.widget, width=self.width, name='cell' + str(self.col),
                                       state='readonly', readonlybackground=self.color)  # Create entry widget
        else:
            self.cell_entry = tk.Entry(self.widget, width=self.width, name='cell' + str(self.col),
                                       bg=self.color)  # Create entry widget

        self.cell_entry.grid(column=self.col, row=1)  # Add cell to a grid inside the row object
        self.cell_entry.bind('<Button-1>', self.test_bind)  # Add a binding to get cell value

    def get_xy(self):
        return tuple([self.col, self.row])

    def test_bind(self, event):
        print(self.get_xy())


class _Row:

    def __init__(self, table, row_num, columns=3, header=False):
        super().__init__()
        self.cols = columns  # Set the number of columns
        self.master = table  # Set the parent widget (Table)
        self.row_num = row_num  # Set the current row number
        self.header = header

        row = tk.Frame(self.master, name='row' + str(self.row_num))  # Create a row widget with a name

        for column in range(self.cols):  # For each column, create a cell object
            if self.header:
                _Cell(row, self.row_num, column, color='grey50', read_only=True)
                row.grid(row=self.row_num)  # Add row to a grid inside the table object
            else:
                _Cell(row, self.row_num, column)

        row.grid(row=self.row_num)  # Add row to a grid inside the table object


class Table:
    def __init__(self, master, rows=5, columns=3, name='', header=False):
        super().__init__()
        self.master = master  # Set the parent widget
        self.rows = rows  # Set the number of rows
        self.cols = columns  # Set the number of columns
        self.name = name.lower()  # Set the name and make it lowercase
        self.header = header  # Set whether the table has headers

        if name:  # If a name has been provided, name the widget with the provided name, otherwise leave default
            self.table = tk.Frame(self.master, name=self.name)
        else:
            self.table = tk.Frame(self.master)

        for row in range(self.rows):  # For each row requested, create a row object
            if row == 0:
                _Row(self.table, row, self.cols, self.header)
            else:
                _Row(self.table, row, self.cols)

        self.table.pack()  # Pack the table

    def get_children(self):
        return self.table.winfo_children()  # Returns a list of children (Rows)

    def get_grandchildren(self):
        grandchildren_list = []
        for child in self.table.winfo_children():
            for grandchild in child.winfo_children():
                grandchildren_list.append(grandchild)
        return grandchildren_list  # Returns a list of grandchildren (Cells)

    def get_row(self, row_num):
        return self.table.winfo_children()[row_num]  # Returns specific row

    def update_cell_in_row(self, row_num, data):
        row = self.get_row(row_num)  # Gets the row in question
        if isinstance(data, list):  # Do if data is list
            if len(row.winfo_children()) == len(data):
                for i, cell in enumerate(row.winfo_children()):
                    cell.delete(0, tk.END)  # Delete text in entry
                    cell.insert(0, data[i])  # Insert new text in entry
        elif isinstance(data, dict):
            print('Data provided in dictionary format')
            # ToDo Match key to column header
            for cell in row.winfo_children():
                cell.delete(0, tk.END)
                cell.insert(0, 'help')

