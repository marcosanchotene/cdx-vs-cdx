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

    intersection = components_1.intersection(components_2)
    if intersection:
        components3_text.configure(text="Components found on both files:")
        for dependency in intersection:
            text_for_file_3.insert('end -1 chars', dependency + '\n')
    else:
        components3_text.configure(text="No components found on both files.")


root = Tk()
root.title('CDX vs CDX')

# Left and right frames
left_frame = Frame(root, width=200, height=500)
left_frame.grid(column=0, row=0, padx=10, pady=5, sticky='N')

right_frame = Frame(root, width=650, height=500)
right_frame.grid(column=1, row=0, padx=10, pady=5, sticky='N')

# Left frame
# Buttons
load_file_1_button = Button(left_frame, text="Load file 1", command=load_file_1, height=1)
load_file_2_button = Button(left_frame, text="Load file 2", command=load_file_2, height=1)
compare_files_button = Button(left_frame, text="Compare files", command=compare_files, height=1)

load_file_1_button.grid(column=0, row=0)
load_file_2_button.grid(column=1, row=0)
compare_files_button.grid(column=2, row=0)

# File 1 details
file1_text = Text(left_frame, width=40, height=12, relief=tkinter.GROOVE)

file1_text.grid(column=0, row=2, columnspan=3)

# File 2 details
file2_text = Text(left_frame, width=40, height=12, relief=tkinter.GROOVE)

file2_text.grid(column=0, row=3, columnspan=3)

# Right frame
# Components text 1
components1_text = Label(right_frame, height=1)
text_for_file_1 = Text(right_frame, width=50, height=12)

components1_text.grid(column=0, row=0)
text_for_file_1.grid(column=0, row=1)

# # Components text 2
components2_text = Label(right_frame, height=1)
text_for_file_2 = Text(right_frame, width=50, height=12)

components2_text.grid(column=0, row=2)
text_for_file_2.grid(column=0, row=3)

# # Components text 3
components3_text = Label(right_frame)
text_for_file_3 = Text(right_frame, width=50, height=24)

components3_text.grid(column=1, row=0)
text_for_file_3.grid(column=1, row=1, rowspan=3)

root.mainloop()
