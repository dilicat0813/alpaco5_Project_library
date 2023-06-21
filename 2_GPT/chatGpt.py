import openai
import mysql.connector
import os
# REF https://platform.openai.com/docs/libraries

openai.api_key = os.getenv('API_KEY')
openai.organization = "org-hGPtZbB25DAWDQflBn094cUK" # https://platform.openai.com/account/org-settings
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# https://platform.openai.com/docs/models/gpt-3-5
model_engine = "text-davinci-003"
# 4,096 tokens or about 3,000 words. As a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text.
max_tokens = 1024

def chatGPTInput(text):
    response = openai.Completion.create(model=model_engine, prompt=text, temperature=0.6, max_tokens=max_tokens)
    return response.choices[0].text


if __name__ == '__main__':
    # Ref: https://community.openai.com/t/how-i-put-chatgpt-giving-recomendations-based-on-database/85115/4
    question = "onion soup has mushrooms?"
    table_structure = """ \"\"\" \n  TableName: food \n Field,Type,Null,Key,Default,Extra \n  name,varchar(45),YES,,NULL, \n  mushroom,tinyint,YES,,0, \n tomato,tinyint,YES,,0, \n  milk,tinyint,YES,,0, \n  egg,tinyint,YES,,0, \n  \"\"\" """
    prompt_asking_sql = " Given database schema: {} Write SQL query for question, only sql, no other text :{}".format(table_structure, question)

    print("SQL: ", prompt_asking_sql)
    answer_sql = chatGPTInput(prompt_asking_sql)
    # Establishing the connection
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=MYSQL_PASSWORD,
        database="alphaco"
    )
    print(answer_sql)
    # Checking if the connection was successful
    if not connection.is_connected():
        print("Not Connected to MySQL database")
        exit()

    # Creating a cursor
    cursor = connection.cursor()

    # Executing the query
    cursor.execute(answer_sql)
    query_result = cursor.fetchone()

    # Closing the connection
    cursor.close()
    connection.close()
    print(query_result)
    final_question = """
    Act as the manager of a restaurant, who wants to answer user queries about the restaurant and only about the restaurant. 
    Given the following user question and the related search results, respond to the user using only the results as context: 
    User question: {} 
    Given this database schema: {}
    Sql Query Used: {}
    Query Results: {}" 
    """.format(question, table_structure, answer_sql, query_result)
    final_answer = chatGPTInput(final_question)
    print("답변: ", final_answer)