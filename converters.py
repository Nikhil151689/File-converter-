import os
import json
import yaml
import pandas as pd
from PIL import Image
import markdown

def convert_file(filepath, conversion_type, output_folder):
    """
    Converts a file based on the conversion type.
    
    Args:
        filepath (str): Path to the input file.
        conversion_type (str): Type of conversion (e.g., 'png_to_jpg', 'csv_to_json').
        output_folder (str): Folder to save the converted file.
        
    Returns:
        str: Filename of the converted file.
    """
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    output_filename = ""
    output_path = ""

    # Image Conversions
    if conversion_type == 'png_to_jpg':
        if ext != '.png': raise ValueError("Input file must be PNG")
        img = Image.open(filepath)
        rgb_img = img.convert('RGB')
        output_filename = name + '.jpg'
        output_path = os.path.join(output_folder, output_filename)
        rgb_img.save(output_path)
        
    elif conversion_type == 'jpg_to_png':
        if ext not in ['.jpg', '.jpeg']: raise ValueError("Input file must be JPG or JPEG")
        img = Image.open(filepath)
        output_filename = name + '.png'
        output_path = os.path.join(output_folder, output_filename)
        img.save(output_path)

    elif conversion_type == 'to_webp':
        if ext not in ['.png', '.jpg', '.jpeg', '.bmp']: raise ValueError("Input file must be an image")
        img = Image.open(filepath)
        output_filename = name + '.webp'
        output_path = os.path.join(output_folder, output_filename)
        img.save(output_path, 'WEBP')

    elif conversion_type == 'webp_to_png':
        if ext != '.webp': raise ValueError("Input file must be WEBP")
        img = Image.open(filepath)
        output_filename = name + '.png'
        output_path = os.path.join(output_folder, output_filename)
        img.save(output_path)

    elif conversion_type == 'image_to_pdf':
        if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']: raise ValueError("Input file must be an image")
        img = Image.open(filepath)
        rgb_img = img.convert('RGB')
        output_filename = name + '.pdf'
        output_path = os.path.join(output_folder, output_filename)
        rgb_img.save(output_path, 'PDF')

    # Data Conversions
    elif conversion_type == 'csv_to_json':
        if ext != '.csv': raise ValueError("Input file must be CSV")
        df = pd.read_csv(filepath)
        output_filename = name + '.json'
        output_path = os.path.join(output_folder, output_filename)
        df.to_json(output_path, orient='records', indent=4)

    elif conversion_type == 'json_to_csv':
        if ext != '.json': raise ValueError("Input file must be JSON")
        df = pd.read_json(filepath)
        output_filename = name + '.csv'
        output_path = os.path.join(output_folder, output_filename)
        df.to_csv(output_path, index=False)

    elif conversion_type == 'csv_to_excel':
        if ext != '.csv': raise ValueError("Input file must be CSV")
        df = pd.read_csv(filepath)
        output_filename = name + '.xlsx'
        output_path = os.path.join(output_folder, output_filename)
        df.to_excel(output_path, index=False)

    elif conversion_type == 'excel_to_csv':
        if ext not in ['.xlsx', '.xls']: raise ValueError("Input file must be Excel")
        df = pd.read_excel(filepath)
        output_filename = name + '.csv'
        output_path = os.path.join(output_folder, output_filename)
        df.to_csv(output_path, index=False)
    
    elif conversion_type == 'json_to_excel':
        if ext != '.json': raise ValueError("Input file must be JSON")
        df = pd.read_json(filepath)
        output_filename = name + '.xlsx'
        output_path = os.path.join(output_folder, output_filename)
        df.to_excel(output_path, index=False)

    elif conversion_type == 'excel_to_json':
        if ext not in ['.xlsx', '.xls']: raise ValueError("Input file must be Excel")
        df = pd.read_excel(filepath)
        output_filename = name + '.json'
        output_path = os.path.join(output_folder, output_filename)
        df.to_json(output_path, orient='records', indent=4)

    # YAML Conversions
    elif conversion_type == 'json_to_yaml':
        if ext != '.json': raise ValueError("Input file must be JSON")
        with open(filepath, 'r') as f:
            data = json.load(f)
        output_filename = name + '.yaml'
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)

    elif conversion_type == 'yaml_to_json':
        if ext not in ['.yaml', '.yml']: raise ValueError("Input file must be YAML")
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        output_filename = name + '.json'
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)

    # Document Conversions
    elif conversion_type == 'md_to_html':
        if ext != '.md': raise ValueError("Input file must be Markdown (.md)")
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        html = markdown.markdown(text)
        output_filename = name + '.html'
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
    else:
        raise ValueError(f"Unsupported conversion type: {conversion_type}")

    return output_filename
