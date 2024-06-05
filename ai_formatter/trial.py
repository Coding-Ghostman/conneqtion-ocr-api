import re, string

months_dict = {
    "January": ["Jan"],
    "February": ["Feb"],
    "March": ["Mar"],
    "April": ["Apr"],
    "May": ["May"],
    "June": ["Jun"],
    "July": ["Jul"],
    "August": ["Aug"],
    "September": ["Sep", "Sept"],
    "October": ["Oct"],
    "November": ["Nov"],
    "December": ["Dec"]
}

def date_splitter(date_lst):
  dates = {
    "date1": {"list": []},
    "date2": {"list": []}
  }
  for index, date in enumerate(date_lst):
    special_characters = r' ,!:\.\-/\\|\`~*%#^\(\)\{\}\[\]'# Define the pattern to include all specified special characters and spaces
    pattern = r'[\w]+|[' + special_characters + r']' # Build the regex pattern to match either a word, a special character, or a space
    split_text = re.findall(pattern, date)         # Use re.findall() to find all matches based on the pattern
    dates[f"date{index+1}"]["list"] = split_text
  return dates

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def date_similarity_checker_algorithm(date_1, date_2):
  def check_lists_equal(list1, list2):
    if len(list1) != len(list2):
        return False
    return sorted(list1) == sorted(list2)
  dates = date_splitter([date_1, date_2])
  for i in dates.keys():
    for j in dates[i]["list"]:
      if j in date_codes:
        if "code" not in dates[i]:
          dates[i]["code"] = []
          dates[i]["code"].append(j)
        else:
          dates[i]["code"].append(j)
      elif j in date_symbols.keys():
        if "code" not in dates[i]:
          dates[i]["code"] = []
          dates[i]["code"].append(date_symbols[j])
        else:
          dates[i]["code"].append(date_symbols[j])
  return check_lists_equal(dates["date1"]["code"], dates["date2"]["code"])

def date_format_mapper(date_list):
  date_format = { "string" : "",
    "format" : {
    "date_code":  [],
    "date_symbol":  [],
    "special_character": [],
    "numerical_values": [],
    "string_val" : [],
    "space" : " "
  }}
  for i in date_list:
    if i in date_codes:
      date_format["format"]["date_code"].append(i)
      date_format["string"] += "{date_code}"
      # date_format["format"]["{date_code}"]["traversal"] += 1
    elif i in date_symbols.keys():
      date_format["format"]["date_symbol"].append(i)
      date_format["format"]["date_code"].append(date_symbols[i])
      date_format["string"] += "{date_symbol}"
    elif i in special_chars:
      date_format["format"]["special_character"].append(i)
      date_format["string"] += "{special_character}"
    elif i == " ":
      date_format["string"] += "{space}"
    elif is_number(i):
      date_format["format"]["numerical_values"].append(i)
      date_format["string"] += "{numerical_values}"
    else:
      date_format["format"]["string_val"].append(i)
      date_format["string"] += "{string_val}"
  return date_format

def date_format_checker_algorithm(date1, date2, format_similarity_metrics="strict"):
  if format_similarity_metrics == "strict":
    code = date_similarity_checker_algorithm(date1, date2)
    if code:
      dates = [date1, date2]
      dates = date_splitter(dates)
      for index, date in enumerate(dates):
        dates[f"date{index+1}"]["format"] = date_format_mapper(dates[f"date{index+1}"]["list"])
      if dates[f"date1"]["format"]["string"] == dates[f"date2"]["format"]["string"]:
        return True, dates
      else:
        return False, dates
    else:
      return False, []
  elif format_similarity_metrics == "partial":
    if date_similarity_checker_algorithm(date1, date2):
      return True, []
    else:
      return False, []

def date_exchange(from_date, to_date, amount):
    ticker = f"{from_date}{to_date}=X"
    data = yf.Ticker(ticker)
    exchange_rate = data.history(period="1d")['Close'].iloc[-1]
    converted_amount = float(amount) * exchange_rate
    formatted_value = "{:.2f}".format(converted_amount)
    return formatted_value

def date_format_convertor(dates, format = "strict"):
  date_format = dates["date2"]["format"]["string"]
  pattern = r'\{([^{}]*)\}'
  date_format = re.findall(pattern, date_format)
  final_date_string = ""
  for component in date_format:
    if component == "space":
      final_date_string += " "
    elif component == "date_code":
      final_date_string += str(dates["date2"]["format"]["format"]["date_code"][0])
    elif component == "date_symbol":
      final_date_string += str(dates["date2"]["format"]["format"]["date_symbol"].pop(0))
    elif component == "special_character":
      final_date_string += str(dates["date2"]["format"]["format"]["special_character"].pop(0))
    elif component == "numerical_values":
      if dates["date2"]["format"]["format"]["date_code"][0] == dates["date1"]["format"]["format"]["date_code"][0]:
        final_date_string += str(dates["date1"]["format"]["format"]["numerical_values"].pop(0))
      else:
        final_date_string += str(date_exchange(dates["date1"]["format"]["format"]["date_code"][0],dates["date2"]["format"]["format"]["date_code"][0], dates["date1"]["format"]["format"]["numerical_values"].pop(0)))
      if len(dates["date2"]["format"]["format"]["date_code"]) ==1 and dates["date2"]["format"]["format"]["numerical_values"] in [0,1]:
        dates["date2"]["format"]["format"]["date_code"].pop(0)
        dates["date1"]["format"]["format"]["date_code"].pop(0)
    elif component == "string_val" and format == "strict":
      final_date_string += str(dates["date2"]["format"]["format"]["string_val"].pop(0))
  return final_date_string


def date_check_change(date1, date2, new_date):
  similarity, dates = date_format_checker_algorithm(date1.strip(), date2.strip())
  if similarity:
    similarity, dates = date_format_checker_algorithm(new_date.strip(), date1.strip())
    if similarity:
      return False
    else:
      return date_format_convertor(dates) 
  else:
    return False
