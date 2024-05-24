import re
from fuzzywuzzy import fuzz

# def extract_data_between_words(text, word1, word2, threshold=80):
#     # Find the best match for word1 in the text
#     print("lessssss gooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
#     best_match_word1 = max([(fuzz.ratio(word1, w), w) for w in text.split()], key=lambda x: x[0])
#     if best_match_word1[0] < threshold:
#         return f"{word1} not found in the text"

#     # Find the best match for word2 after the best match for word1
#     start_index = text.index(best_match_word1[1]) + len(best_match_word1[1])
#     remaining_text = text[start_index:]
#     best_match_word2 = max([(fuzz.ratio(word2, w), w) for w in remaining_text.split()], key=lambda x: x[0])
#     if best_match_word2[0] < threshold:
#         return f"{word2} not found in the text after {best_match_word1[1]}"

#     # Extract the data between the best matches
#     end_index = remaining_text.index(best_match_word2[1]) + start_index + len(best_match_word2[1])
#     extracted_data = text[start_index:end_index]

#     return f"{best_match_word1[1]} {extracted_data} {best_match_word2[1]}"

def req_to_sing(text):
    pattern = r"REQUESTOR(.*?)VENDOR SELECTION"
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


def get_detaildescription(final_text,pattern= r"\bDetailed\s*(.*)"):
    
    match = re.search(pattern, final_text)
    key = "Detailed Description"
    value=""
    if match:
        detailed_description = final_text[match.start() :]
        cleaned_string = re.sub(r"[^\w\s.,()\[\]]:", "", detailed_description)
        cleaned_string = cleaned_string.replace("\n", "")
        key, value = cleaned_string.split(":", 1)
    return {key: value}
