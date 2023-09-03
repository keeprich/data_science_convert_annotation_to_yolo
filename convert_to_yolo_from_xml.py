import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
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
    # Ask the user to select the XML directory
    xml_dir = filedialog.askdirectory(title="Select the XML Directory")

    # Get class names as a comma-separated string from the user
    class_names_input = simpledialog.askstring("Class Names", "Enter class names (comma-separated):")
    class_names = {name.strip(): i for i, name in enumerate(class_names_input.split(','))}

    # Ask the user for the output folder name
    output_folder_name = simpledialog.askstring("Output Folder", "Enter the output folder name:")

    if xml_dir and class_names_input and output_folder_name:
        output_dir = os.path.join(os.getcwd(), output_folder_name)
        convert_to_yolo(xml_dir, output_dir, class_names)
        print("Output directory:", output_dir)

# Create the main window
window = tk.Tk()
window.title("XML to YOLO Converter")

# Create and pack UI elements
convert_button = tk.Button(window, text="Convert", command=convert_click)
convert_button.pack()

# Run the GUI application
window.mainloop()
