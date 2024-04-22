import re, json, os
from logger import setup_logger
from deletor import delete_log_file, delete_files_in_directory
from llm_checker import get_llm_help
from pdf_extractor import convert_pdf_img, extract_all_data
from string_processor import (
    req_to_sing,
    get_detaildescription,
    extract_data_between_words,
)

logger = setup_logger()


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
    
    logger.info(
        f"""
          Extracted Data:

          {complete_string}

        """
    )

    final_text = req_to_sing(complete_string)

    logger.info(
        f"""
          Extracted Data:

          {final_text}

        """
    )

    end_pattern = r"telephone\b"
    end_match = re.search(end_pattern, complete_string, flags=re.IGNORECASE)
    end_string = complete_string[: end_match.start()]

    logger.info(
        f"""
          Extracted Data:

          {end_string}

        """
    )
    first = get_llm_help(end_string)
    val = extract_data_between_words(final_text, "Purchase", "Detailed")

    logger.info(
        f"""
          Extracted Data:

          {val}

        """
    )

    answer.update(first)
    answer = make_dict(answer, val)
    d = get_detaildescription(final_text)
    answer.update(d)

    logger.info(
        f"""
          Extracted Data:

          {d}

        """
    )

    delete_files_in_directory(output_path)
    delete_log_file()
    return answer
