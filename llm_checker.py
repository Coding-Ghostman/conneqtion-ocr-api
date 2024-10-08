import re, json, os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI


from dotenv import load_dotenv

load_dotenv()
llm = ChatMistralAI(
    model="open-mistral-nemo",
    api_key=os.getenv("MISTRAL_API_KEY"),
    model_kwargs={"response_format": {"type": "json_object"}},
)  # type: ignore

def convert_list_values_to_string(input_dict):
    for key, value in input_dict.items():
        if isinstance(value, list):
            input_dict[key] = ",".join(map(str, value))
    return input_dict


def get_llm_help(end_string):
    template = """

        You are a helpful invoice checker. OCR is performed on an invoice to get the details in it which will later be stored inkkkl
        a database, but some of the data is jumbled and is stringed up with other data. As such it is important to extract relevant
        details from the document.

        Here are the essential data that needs to be retireved in key value pairs. Here is the sample of the output that is required.
        Data enclosed in angular brackets <> are placeholders.

        Most of the data is nearby to the keys, do not miss out on data and string them intelligently

        'Requestor(s) Name' : '<Name>',
        'Department' : <Department>,
        'Company Name' : '<company_name>',
        'Contact Person': <person_name>,<person_name> (NOTE: There might be multiple persons within that range)

        Below is the data extracted from the OCR
        {end_string}

        Please map the relevant data given in the example output and return a json. DO NOT GIVE ANYTHING ELSE OTHER THAN A JSON
        """
    prompt = ChatPromptTemplate.from_template(template)
    chain = RunnablePassthrough.assign() | prompt | llm | StrOutputParser()

    s = chain.invoke({"end_string": end_string})
    pattern = r"\{(.+?)\}"
    matches = re.findall(pattern, s, re.DOTALL)
    json_data = "{" + matches[0] + "}"
    json_object = json.loads(json_data)
    json_object = convert_list_values_to_string(json_object)
    return json_object


def grammar_corrector(end_string):
    print("end stringgggg")
    print(end_string)
    template = """

        The below provided data has been extracted from a single source justification form, using tesseract OCR. 
        
        ```plaintext
        {end_string}
        ```
        You are a helpful assistant specializing in English grammar.
        Check all the data from the above given context and fix the errors accordingly. 
        If No Data is provided then return an empty string.
        RETURN THE DATA IN JSON FORMAT ONLY NOTHING ELSE
        """
    prompt = ChatPromptTemplate.from_template(template)


    chain = RunnablePassthrough.assign() | prompt | llm | StrOutputParser()
    try:
        s = chain.invoke({"end_string": end_string})
        pattern = r"\{(.+?)\}"
        matches = re.findall(pattern, s, re.DOTALL)
        json_data = "{" + matches[0] + "}"
        json_object = json.loads(json_data)
        json_object = convert_list_values_to_string(json_object)
        return json_object
    except Exception as e:
        print("###############################")
        print(f"Exception at grammar corrector:{e}")
        print("###############################")
        return None
