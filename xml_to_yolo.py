import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import xml.etree.ElementTree as ET

# Function to convert XML annotations to YOLO format
def convert_to_yolo(xml_dir, output_dir, class_names):
    try:
        # Create the YOLO annotation folder if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(xml_dir):
            if filename.endswith('.xml'):
                xml_file_path = os.path.join(xml_dir, filename)

                # Parse the XML file
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # Extract image width and height from the XML
                width = int(root.find('size/width').text)
                height = int(root.find('size/height').text)

                # Create the YOLO annotation file path
                yolo_filename = os.path.splitext(filename)[0] + '.txt'
                yolo_file_path = os.path.join(output_dir, yolo_filename)

                with open(yolo_file_path, 'w') as yolo_file:
                    for obj in root.findall('object'):
                        class_name = obj.find('name').text
                        class_id = class_names.get(class_name)

                        if class_id is not None:
                            # Extract bounding box coordinates
                            xmin = float(obj.find('bndbox/xmin').text)
                            ymin = float(obj.find('bndbox/ymin').text)
                            xmax = float(obj.find('bndbox/xmax').text)
                            ymax = float(obj.find('bndbox/ymax').text)

                            # Calculate YOLO bounding box coordinates (normalized)
                            x_center = (xmin + xmax) / (2 * width)
                            y_center = (ymin + ymax) / (2 * height)
                            box_width = (xmax - xmin) / width
                            box_height = (ymax - ymin) / height

                            # Write YOLO annotation to the file
                            yolo_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

        messagebox.showinfo("Conversion Completed", "XML to YOLO conversion completed.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to handle the "Convert" button click
def convert_click():
    xml_directory = xml_dir_entry.get()
    output_directory = output_dir_entry.get()
    classes = class_names_entry.get().split(',')

    # Create class_names dictionary from user input
    class_names_dict = {}
    for i, class_name in enumerate(classes):
        class_names_dict[class_name.strip()] = i

    convert_to_yolo(xml_directory, output_directory, class_names_dict)

# Create the main window
window = tk.Tk()
window.title("XML to YOLO Converter")

# Create and pack UI elements
tk.Label(window, text="XML Directory:").pack()
xml_dir_entry = tk.Entry(window)
xml_dir_entry.pack()

tk.Label(window, text="Output Directory:").pack()
output_dir_entry = tk.Entry(window)
output_dir_entry.pack()

tk.Label(window, text="Class Names (comma-separated):").pack()
class_names_entry = tk.Entry(window)
class_names_entry.pack()

convert_button = tk.Button(window, text="Convert", command=convert_click)
convert_button.pack()

# Run the GUI application
window.mainloop()
