import re, json, os
from deletor import delete_files_in_directory
from llm_checker import get_llm_help, grammar_corrector
from pdf_extractor import convert_pdf_img, extract_all_data
from string_processor import (
    req_to_sing,
    get_detaildescription,
    extract_data_between_words,
)

def make_dict(dict, val):

    key, value = val.split(":", 1)
    dict[key] = value
    return dict

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

    start_pattern = r"single\b"
    start_match = re.search(start_pattern, complete_string, flags=re.IGNORECASE)

    end_pattern = r"telephone\b"
    end_match = re.search(end_pattern, complete_string, flags=re.IGNORECASE)
    end_string = complete_string[start_match.end(): end_match.start()]

    first = get_llm_help(end_string)
    val = extract_data_between_words(final_text, "Purchase", "Detailed")

    if first:
      answer.update(first)
    # answer = make_dict(answer, val)
    d = get_detaildescription(final_text)
    final_string = val + "\n"+ str(d)
    detailed_desc = grammar_corrector(final_string)
    if detailed_desc:
      answer.update(detailed_desc)

    delete_files_in_directory(output_path)
    return answer
