import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import xml.etree.ElementTree as ET
from collections import namedtuple
from tkinter import ttk

# Define annotation formats and their corresponding file extensions
AnnotationFormat = namedtuple("AnnotationFormat", ["name", "extension"])

annotation_formats = [
    AnnotationFormat("XML", ".xml"),
    AnnotationFormat("YOLO", ".txt"),
    AnnotationFormat("COCO", ".json")  # Add the new format here
]

# Function to convert annotations to the specified format
def convert_annotations(input_dir, output_dir, input_format, output_format, class_names):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(input_dir):
            if filename.endswith(input_format.extension):
                input_file_path = os.path.join(input_dir, filename)

                # Parse the input annotation file based on the format
                if input_format.name == "XML":
                    tree = ET.parse(input_file_path)
                    root = tree.getroot()

                    # Extract image width and height from the XML
                    width = int(root.find('size/width').text)
                    height = int(root.find('size/height').text)

                    # Create the output annotation file path
                    output_filename = os.path.splitext(filename)[0] + output_format.extension
                    output_file_path = os.path.join(output_dir, output_filename)

                    with open(output_file_path, 'w') as output_file:
                        for obj in root.findall('object'):
                            class_name = obj.find('name').text
                            class_id = class_names.get(class_name)

                            if class_id is not None:
                                # Extract bounding box coordinates
                                xmin = float(obj.find('bndbox/xmin').text)
                                ymin = float(obj.find('bndbox/ymin').text)
                                xmax = float(obj.find('bndbox/xmax').text)
                                ymax = float(obj.find('bndbox/ymax').text)

                                # Calculate bounding box coordinates based on output format
                                if output_format.name == "YOLO":
                                    x_center = (xmin + xmax) / (2 * width)
                                    y_center = (ymin + ymax) / (2 * height)
                                    box_width = (xmax - xmin) / width
                                    box_height = (ymax - ymin) / height

                                    # Write annotation to the output file
                                    output_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

        messagebox.showinfo("Conversion Completed", f"{input_format.name} to {output_format.name} conversion completed.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to handle the "Convert" button click
def convert_click():
    # Ask the user to select the input directory
    input_dir = filedialog.askdirectory(title="Select the Input Directory")

    # Ask the user for the output folder name
    output_folder_name = simpledialog.askstring("Output Folder", "Enter the output folder name:")

    # Get class names as a comma-separated string from the user
    class_names_input = simpledialog.askstring("Class Names", "Enter class names (comma-separated):")
    class_names = {name.strip(): i for i, name in enumerate(class_names_input.split(','))}

    if input_dir and output_folder_name and class_names_input:
        output_dir = os.path.join(os.getcwd(), output_folder_name)
        input_format = input_format_var.get()
        output_format = output_format_var.get()

        convert_annotations(input_dir, output_dir, input_format, output_format, class_names)

# Create the main window
window = tk.Tk()
window.title("Annotation Converter")

# Apply styles to the GUI elements
style = ttk.Style()
style.configure("TButton", padding=(10, 5), font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

# Create and pack UI elements
ttk.Label(window, text="Select Input Format:").pack()
input_format_var = tk.StringVar()
input_format_dropdown = ttk.OptionMenu(window, input_format_var, annotation_formats[0], *annotation_formats)
input_format_dropdown.pack()

ttk.Label(window, text="Select Output Format:").pack()
output_format_var = tk.StringVar()
output_format_dropdown = ttk.OptionMenu(window, output_format_var, annotation_formats[1], *annotation_formats)
output_format_dropdown.pack()

convert_button = ttk.Button(window, text="Convert", command=convert_click)
convert_button.pack()

# Run the GUI application
window.mainloop()
