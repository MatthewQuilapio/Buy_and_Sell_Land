
sell_header = ['ID', 'Seller Name', 'Price', 'Location', 'Contact']

def listbox_header(values_result, curr_tree):
    
    curr_tree.delete(*curr_tree.get_children())
    curr_tree["columns"] = ('1', '2', '3', '4', '5')

    curr_tree['show'] = 'headings'

    ctr = 0
    for no_columns in curr_tree['columns']:
        curr_tree.column(no_columns, width = 90, anchor ='c')
        curr_tree.heading(no_columns, text = sell_header[ctr])
        ctr+=1

    insert_data(values_result, curr_tree)
    return curr_tree

    
def insert_data(result, tree):
    ctr = 0

    for x in result:
        tree.insert("", 'end', values = (x))
        ctr+=1