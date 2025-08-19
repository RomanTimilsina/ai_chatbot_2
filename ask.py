import chromadb
# from openai import OpenAI
import openai
from dotenv import load_dotenv

import dateparser
from datetime import datetime
import re



load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "Your_open_Api_key"

# client = OpenAI()



def validate_phone(phone: str) -> bool:
    pattern = r"^\+?\d{7,15}$"
    return re.match(pattern, phone) is not None

def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


import dateparser

def parse_relative_date(text: str) -> str:
    dt = dateparser.parse(
        text,
        settings={
            'PREFER_DATES_FROM': 'future',   # pick future date if ambiguous
            'RETURN_AS_TIMEZONE_AWARE': False
        }
    )
    if dt:
        return dt.strftime("%Y-%m-%d")
    return "Could not parse date"


# setting the environment

DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="growing_vegetables")

while True:
    user_query = input("What do you want to know about?\n\n")

    if user_query.lower() in ["call", "appointment"]:
        user_phone_no = input("Please provide your phone number first? ")
        if(validate_phone(user_phone_no)):
            print(user_phone_no)
        user_email = input("Please also provide your email?")
        if validate_email(user_email):
            print(user_email)
        user_name = input("And what might be your name?")
        date_input = input("When would you like the appointment? ")
        date_parsed = parse_relative_date(date_input)
        print(date_parsed)

        if date_parsed:
            print(date_parsed)
                    
    else:
        results = collection.query(
            query_texts=[user_query],
            n_results=4
        )

        print(results['documents'])
        #print(results['metadatas'])


        system_prompt = """
        You are a helpful assistant. You answer questions about growing vegetables in Florida. 
        But you only answer based on knowledge I'm providing you. You don't use your internal 
        knowledge and you don't make thins up.
        If you don't know the answer, just say: I don't know
        --------------------
        The data:
        """+str(results['documents'])+"""
        """

        #print(system_prompt)

        # response = openai.ChatCompletion.create(
        #     model="gpt-4o-mini",
        #     messages=[{"role": "user", "content": user_query}]
        # )

        response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
        {"role": "system", "content": system_prompt},  # inject your context
        {"role": "user", "content": user_query}
        ]
        )


        print("\n\n---------------------\n\n")

        print(response.choices[0].message.content)

