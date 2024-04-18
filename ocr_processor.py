import re, json, os
from llm_checker import get_llm_help
from pdf_extractor import convert_pdf_img, extract_all_data
from string_processor import req_to_sing, get_detaildescription, extract_data_between_words

def make_dict(dict,val):
  
  key,value = val.split(":",1)
  dict[key] = value
  return dict

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")


def extract_data_(pdf_data):
    answer = {}
    output_path = "converted_images"
    convert_pdf_img(pdf_data, output_path)
    complete_data = extract_all_data()
    
    complete_string = ""
    for tables in complete_data:
      for i, table in enumerate(tables):
        for row in table:
            complete_string += str(row) + "\n"

    final_text = req_to_sing(complete_string)
    end_pattern = r"telephone\b"
    end_match = re.search(end_pattern, complete_string, flags=re.IGNORECASE)
    end_string = complete_string[:end_match.start()]

    first = get_llm_help(end_string)
    print(final_text)
    val = extract_data_between_words(final_text,"Purchase","Detailed")
    answer.update(first)
    answer = make_dict(answer, val)
    d = get_detaildescription(final_text)
    answer.update(d)

    delete_files_in_directory(output_path)
    return answer



    
  