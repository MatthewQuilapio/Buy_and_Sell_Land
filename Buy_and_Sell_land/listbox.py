"""
    Module: listbox.py
    Description: Utility functions for displaying property
                 listings inside a Tkinter Treeview widget.
    Author: Angelo Matthew Quilapio
    License: All Rights Reserved
"""

# Column headers for the property selling list
sell_header = ['ID', 'Seller Name', 'Price', 'Location', 'Contact']

def listbox_header(values_result, curr_tree):
    """
    Configure and populate a Tkinter Treeview widget 
    to display real estate selling records.

    Parameters:
        values_result (list[tuple]): List of tuples containing 
                                     rows fetched from the database.
        curr_tree (ttk.Treeview): Tkinter Treeview widget where 
                                  the data will be displayed.

    Returns:
        ttk.Treeview: Configured Treeview widget with inserted data.
    """

    # Clear any existing rows in the Treeview
    curr_tree.delete(*curr_tree.get_children())

    # Define 5 columns for the Treeview
    curr_tree["columns"] = ('1', '2', '3', '4', '5')

    # Hide the default first column
    curr_tree['show'] = 'headings'

    # Set up column headers and properties
    ctr = 0
    for no_columns in curr_tree['columns']:
        curr_tree.column(no_columns, width = 90, anchor ='c')
        curr_tree.heading(no_columns, text = sell_header[ctr])
        ctr+=1

    # Insert rows of data from the database query
    insert_data(values_result, curr_tree)

    return curr_tree

    
def insert_data(result, tree):
    """
    Insert rows of data into a Treeview widget.

    Parameters:
        result (list[tuple]): List of tuples representing records 
                              from the database.
        tree (ttk.Treeview): Treeview widget to insert data into.
    """

    ctr = 0

    for x in result:
        tree.insert("", 'end', values = (x))
        ctr+=1