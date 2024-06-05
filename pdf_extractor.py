import pytesseract, os, cv2
import numpy as np
from pdf2image import convert_from_bytes
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\AtmanMishra\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def convert_pdf_img(pdf_data, output_path):
    images = convert_from_bytes(pdf_data)
    for i in range(len(images)):
      image_path = os.path.join(output_path, 'page' + str(i) + '.jpg')
      images[i].save(image_path, 'JPEG')

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((1, 1), np.uint8)
    dilation = cv2.dilate(binary, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)
    return erosion

def extract_tables(image_path):
    preprocessed_image = preprocess_image(image_path)
    tess_config = r"--oem 3 --psm 12"
    extracted_text = pytesseract.image_to_string(preprocessed_image, config = tess_config)
    extracted_text = pytesseract.image_to_string(preprocessed_image)
    lines = extracted_text.split('\n')
    tables = []
    current_table = []
    for line in lines:
        if line.strip() == '':
            if current_table:
                tables.append(current_table)
                current_table = []
        else:
            current_table.append(line)
    if current_table:
        tables.append(current_table)
    return tables

def traverse_folder(folder_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

def extract_all_data(converted_images_path = "converted_images"):
  complete_data = []
  for image in traverse_folder(converted_images_path):
    temp_val = extract_tables(image)
    complete_data.append(temp_val)
  return complete_data

def merge_pngs(output_path):
    img1 = Image.open(f"{output_path}/page0.jpg")
# Open the second image
    img2 = Image.open(f"{output_path}/page1.jpg")
    # Create a new image with the combined size
    width = max(img1.width, img2.width)
    height = img1.height + img2.height
    combined_img = Image.new("RGB", (width, height))
    # Paste the first image onto the combined image
    combined_img.paste(img1, (0, 0))
    # Paste the second image onto the combined image
    combined_img.paste(img2, (0, img1.height))
    # Save the combined image
    combined_img.save(f"{output_path}/combined_image.jpg")
