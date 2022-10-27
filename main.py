import json
import textwrap
import tkinter
from tkinter import *
from tkinter import filedialog


def load_file_1():
    filename1 = browse_files()
    text_for_file_1.delete('1.0', 'end')
    file_details = extract_file_details(filename1)
    file1_text.delete('1.0', 'end')
    file1_text.insert('1.0', file_details)
    global components_1
    components_1 = extract_components(filename1)


def load_file_2():
    filename2 = browse_files()
    text_for_file_2.delete('1.0', 'end')
    file_details = extract_file_details(filename2)
    file2_text.delete('1.0', 'end')
    file2_text.insert('1.0', file_details)
    global components_2
    components_2 = extract_components(filename2)


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
    File: {filename}
    
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


def compare_files():
    text_for_file_1.delete('1.0', 'end')
    difference1 = components_1 - components_2
    if difference1:
        components1_text.configure(text="Components found on file 1 but not on file 2:")
        for dependency in difference1:
            text_for_file_1.insert('end -1 chars', dependency + '\n')
    else:
        components1_text.configure(text="Files contain the same components.")

    text_for_file_2.delete('1.0', 'end')
    difference2 = components_2 - components_1
    if difference2:
        components2_text.configure(text="Components found on file 2 but not on file 1:")
        for dependency in difference2:
            text_for_file_2.insert('end -1 chars', dependency + '\n')
    else:
        components2_text.configure(text="Files contain the same components.")


root = Tk()
root.title('CDX vs CDX')
content = Frame(root)

# Load buttons
load_file_button_1_frame = Frame(content, width=50)
load_file_button_2_frame = Frame(content, width=50)
load_file_1_button = Button(load_file_button_1_frame, text="Load file 1", command=load_file_1)
load_file_2_button = Button(load_file_button_2_frame, text="Load file 2", command=load_file_2)

# File 1 details
file1_text_frame = Frame(content, width=50)
file1_text = Text(file1_text_frame, width=50, height=15, relief=tkinter.GROOVE)

# File 2 details
file2_text_frame = Frame(content, width=50)
file2_text = Text(file2_text_frame, width=50, height=15, relief=tkinter.GROOVE)

# Components text 1
components1_text_frame = Frame(content, width=50, height=500)
components1_text = Label(components1_text_frame, width=50)
text_for_file_1 = Text(components1_text_frame, width=50)

# Components text 2
components2_text_frame = Frame(content, width=50, height=500)
components2_text = Label(components2_text_frame, width=50)
text_for_file_2 = Text(components2_text_frame, width=50)

# Comparison frame
compare_frame = Frame(content, width=10, height=10)
compare_files_button = Button(compare_frame, text="Compare files", command=compare_files)

# # Geometry
content.pack()

# Load buttons
load_file_button_1_frame.grid(column=0, row=0, pady=5)
load_file_1_button.grid(column=0, row=0, sticky='W')

load_file_button_2_frame.grid(column=2, row=0, pady=5)
load_file_2_button.grid(column=2, row=0, sticky='E')

# File text
file1_text_frame.grid(column=0, row=1)
file1_text.grid(column=0, row=1)

file2_text_frame.grid(column=2, row=1)
file2_text.grid(column=2, row=1)

# Components text
components1_text_frame.grid(column=0, row=3, pady=10)
components1_text.grid(column=0, row=3)
text_for_file_1.grid(column=0, row=4)

components2_text_frame.grid(column=2, row=3, pady=10)
components2_text.grid(column=2, row=3)
text_for_file_2.grid(column=2, row=4)

# Comparison
compare_frame.grid(column=1, row=3)
compare_files_button.grid(column=1, row=3)

root.mainloop()
