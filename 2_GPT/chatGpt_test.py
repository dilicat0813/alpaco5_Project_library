import openai
import mysql.connector
import os
# REF https://platform.openai.com/docs/libraries

openai.api_key = os.getenv('API_KEY')
openai.organization = "org-zIWpEpAT5tC5laOYXQgh16Vl" # https://platform.openai.com/account/org-settings #min
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
    question = "학습에 관련된 책을 추천해줘"
    table_structure = """ \"\"\" \n  TableName: csvjson
            Field,Type,Null,Key,Default,Extra
            ISBN_NO,bigint,YES,,NULL,
            MUMM_LON_HALFLIFE_CO,int,YES,,NULL,
            TITLE_NM,text,YES,,NULL,
            AUTHR_NM,text,YES,,NULL,
            PUBLISHER_NM,text,YES,,NULL,
            BOOK_INTRCN_CN,text,YES,,NULL,
            Combined,text,YES,,NULL,
            KDC_1,int,YES,,NULL,           
            \"\"\"
        """
    """  KDC_1,int,YES,,NULL,
    KDC_1: 책 분류 코드  {
        '0': '총류',
        '1': '철학',
        '2': '종교',
        '3': '사회과학',
        '4': '자연과학',
        '5': '기술과학',
        '6': '예술',
        '7': '언어',
        '8': '문학',
        '9': '역사',
    }
    """
    column_description = """
    TITLE_NM: 책 제목 
    AUTHR_NM: 저자 이름 
    PUBLISHER_NM: 출판사 
    BOOK_INTRCN_CN: 책 소개 
    Combined: 도서 연관 키워드 (비어 있는 경우가 많음)
    """
    prompt_asking_sql = """ 데이터 테이블 구조: {}
    데이터 테이블 열의 자세한 정보: {}
    질문:{}  
    SQL 쿼리를 써야하고 다음과 같은 조건을 만족해야함, 
    1. 'BOOK_INTRCN_CN'이란 열을 포함해야됨
    2. 질문에 연관성 있는 정보도 추출해야함
    3. 실행가능하도록 SQL만 적어주고 다른 글자는 적지 않을 것
    4. 테이블에서 타입이 text 으로 되어 있는 것은 한국어로 적혀있음
    """.format(table_structure, column_description, question)

    print("SQL: ", prompt_asking_sql)
    answer_sql = chatGPTInput(prompt_asking_sql)
    # Establishing the connection
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=MYSQL_PASSWORD,
        database="library"
    )
    print(answer_sql)
    # Checking if the connection was successful
    if not connection.is_connected():
        print("데이터베이스에 연결되어 있지 않습니다")
        exit()

    # Creating a cursor
    cursor = connection.cursor(buffered=True)

    # Executing the query
    cursor.execute(answer_sql)
    query_result = cursor.fetchone()

    # Closing the connection
    cursor.close()
    connection.close()
    print(query_result)
    final_question = """
    사서라고 생각하고 행동해. 
    아래와 같은 질문에 답변을 하기 위해서 데이터베이스에 검색을해서 결과가 나왔을 때
    사용자에게 결과를 알려줘 
    사용자 질문: {} 
    데이터베이스 구조: {}
    데이터 테이블 열의 자세한 정보: {}
    사용한 Sql 쿼리: {}
    쿼리 결과: {}" 
    """.format(question, table_structure,column_description, answer_sql, query_result)
    final_answer = chatGPTInput(final_question)
    print("답변: ", final_answer)