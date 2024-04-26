import re

def req_to_sing(text):
    pattern = r"REQUESTOR(.*?)SINGLE SOURCE JUSTIFICATION"
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    if matches:
        extracted_data = [match.strip() for match in matches][0]
        return extracted_data
    else:
        pattern = r"REQUESTOR(.*?)APPROVAL FOR EXCEPTIONS"
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            extracted_data = [match.strip() for match in matches][0]
            return extracted_data
        else:
            return text


def convert_list_values_to_string(input_dict):
    for key, value in input_dict.items():
        if isinstance(value, list):
            input_dict[key] = ",".join(map(str, value))
    return input_dict


def extract_data_between_words(text, word1, word2):
    pattern = re.compile(
        r"{}(.*?){}".format(re.escape(word1), re.escape(word2)), re.DOTALL
    )
    if pattern:
        matches = pattern.findall(text)
        if matches:
            return word1 + matches[0]
        else:
            return word1 + ''.join(matches)


def get_detaildescription(final_text):
    pattern = r"\bDetailed\s*(.*)"
    match = re.search(pattern, final_text)
    key = "Detailed Description"
    value=""
    if match:
        detailed_description = final_text[match.start() :]
        cleaned_string = re.sub(r"[^\w\s.,()\[\]]:", "", detailed_description)
        cleaned_string = cleaned_string.replace("\n", "")
        key, value = cleaned_string.split(":", 1)
    return {key: value}
