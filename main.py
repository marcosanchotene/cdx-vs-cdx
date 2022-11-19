import json
import textwrap
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

files_loaded = {"file1": False, "file2": False}


def load_file_1():
    file_1_components_list_var.set([""])
    comparison_components_list_var.set([""])
    file1.config(text='')
    file1_details.config(text='')
    components1_text.config(text='')
    components3_text.config(text='')
    filename1 = browse_files()
    file_details = extract_file_details(filename1)
    file1.config(text=f'File 1 {filename1}', justify='left', anchor='nw')
    file1_details.config(text=file_details, justify='left', anchor='nw')
    global components_1
    components_1 = extract_components(filename1)
    files_loaded['file1'] = True
    change_compare_button_state()


def load_file_2():
    file_1_components_list_var.set([""])
    comparison_components_list_var.set([""])
    file2.config(text='')
    file2_details.config(text='')
    components3_text.config(text='')
    filename2 = browse_files()
    file_details = extract_file_details(filename2)
    file2.config(text=f'File2 {filename2}', justify='left', anchor='nw')
    file2_details.config(text=file_details, justify='left', anchor='nw')
    global components_2
    components_2 = extract_components(filename2)
    files_loaded['file2'] = True
    change_compare_button_state()


def browse_files():
    filename = filedialog.askopenfilename(
        initialdir="/home",
        title="Select a CycloneDX JSON file",
        filetypes=(("CycloneDX JSON files", "*.json"),)
    )
    return filename


def extract_file_details(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    details = textwrap.dedent(f"""\
    Tool
    Vendor: {data['metadata']['tools'][0]['vendor']}
    Name: {data['metadata']['tools'][0]['name']}
    Version: {data['metadata']['tools'][0]['version']}
     
    Component
    Type: {data['metadata']['component']['type']}
    Name: {data['metadata']['component']['name']}\
    """)
    return details


def extract_components(filename):
    components = set()
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    for component in data['components']:
        components.add(component['name'] + '@' + component['version'])
    return components


def change_compare_button_state():
    if all(files_loaded.values()):
        compare_files_button.config(state='normal')


def compare_files():
    file_1_components_list_var.set([""])
    difference1 = components_1 - components_2
    if difference1:
        components1_text.configure(text="Components found on file 1 but not on file 2", justify='left', anchor='nw')
        file_1_components_list_var.set(sorted(list(difference1)))
    else:
        components1_text.configure(text="Files contain the same components", justify='left', anchor='nw')

    file_2_components_list_var.set([""])
    difference2 = components_2 - components_1
    if difference2:
        components2_text.configure(text="Components found on file 2 but not on file 1", justify='left', anchor='nw')
        file_2_components_list_var.set(sorted(list(difference2)))
    else:
        components2_text.configure(text="Files contain the same components", justify='left', anchor='nw')

    intersection = components_1.intersection(components_2)
    if intersection:
        components3_text.configure(text="Components found on both files", justify='left', anchor='nw')
        comparison_components_list_var.set(sorted(list(intersection)))
    else:
        components3_text.configure(text="No components found on both files", justify='left', anchor='nw')


root = Tk()
root.title('CDX vs CDX')
content = Frame(root)
content.grid(column=0, row=0, padx=5, pady=5)

# Buttons
load_file_1_button = Button(content, text="Load file 1", command=load_file_1, height=1)
load_file_2_button = Button(content, text="Load file 2", command=load_file_2, height=1)
compare_files_button = Button(content, text="Compare files", command=compare_files, height=1, state='disabled')

load_file_1_button.grid(column=0, row=0, sticky='N')
load_file_2_button.grid(column=0, row=3, sticky='N')
compare_files_button.grid(column=0, row=5, sticky='N')

# File 1 details
file1 = ttk.Label(content, width=70, text='File 1')
file1_details = ttk.Label(content, width=30)

file1.grid(column=1, row=0, columnspan=6)
file1_details.grid(column=0, row=1, columnspan=2)

# File 2 details
file2 = ttk.Label(content, width=70, text='File 2')
file2_details = ttk.Label(content, width=30)

file2.grid(column=1, row=3, columnspan=6)
file2_details.grid(column=0, row=4, columnspan=2)

# Components text 1
components1_text = Label(content, height=1, width=40)
file_1_components_list = [""]
file_1_components_list_var = StringVar(value=file_1_components_list)
file_1_components_listbox = Listbox(
    content, width=40, height=15, relief=tkinter.GROOVE, listvariable=file_1_components_list_var, selectmode='extended'
)
file_1_scrollbar = ttk.Scrollbar(content, orient=VERTICAL, command=file_1_components_listbox.yview)
file_1_components_listbox.configure(yscrollcommand=file_1_scrollbar.set)

file_1_components_listbox.grid(column=4, row=1, columnspan=3)
file_1_scrollbar.grid(column=7, row=1, sticky=(N, S))
components1_text.grid(column=4, row=2, columnspan=3)

# # Components text 2
components2_text = Label(content, height=1, width=40)
file_2_components_list = [""]
file_2_components_list_var = StringVar(value=file_2_components_list)
file_2_components_listbox = Listbox(
    content, width=40, height=15, relief=tkinter.GROOVE, listvariable=file_2_components_list_var, selectmode='extended'
)
file_2_scrollbar = ttk.Scrollbar(content, orient=VERTICAL, command=file_2_components_listbox.yview)
file_2_components_listbox.configure(yscrollcommand=file_2_scrollbar.set)

file_2_components_listbox.grid(column=4, row=4, columnspan=3)
file_2_scrollbar.grid(column=7, row=4, sticky=(N, S))
components2_text.grid(column=4, row=5, columnspan=3)

# # Components text 3
components3_text = Label(content, height=1, width=40)
comparison_components_list = [""]
comparison_components_list_var = StringVar(value=comparison_components_list)
comparison_components_listbox = Listbox(
    content, width=40, height=30, relief=tkinter.GROOVE, listvariable=comparison_components_list_var,
    selectmode='extended'
)
comparison_scrollbar = ttk.Scrollbar(content, orient=VERTICAL, command=comparison_components_listbox.yview)
comparison_components_listbox.configure(yscrollcommand=comparison_scrollbar.set)

comparison_components_listbox.grid(column=8, row=1, columnspan=3, rowspan=4, sticky=(N, S))
comparison_scrollbar.grid(column=11, row=1, rowspan=4, sticky=(N, S))
components3_text.grid(column=8, row=5, columnspan=3)

root.mainloop()
