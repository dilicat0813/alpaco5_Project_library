import openai
import pandas as pd
import os

# REF https://platform.openai.com/docs/libraries
csv_path = './helper/data/db.csv'

csv_data = pd.read_csv(csv_path,low_memory=False,
                       dtype={
                           # "ISBN_NO": int,
                           # "MUMM_LON_HALFLIFE_CO": int,
                           'TITLE_NM': str,
                           'AUTHR_NM': str,
                           'PUBLISHER_NM': str,
                           'BOOK_INTRCN_CN': str,
                           # 'KDC_1': int
                       })
csv_data['TITLE_NM'] = csv_data['TITLE_NM'].astype("string")
csv_data['AUTHR_NM'] = csv_data['AUTHR_NM'].astype("string")
csv_data['PUBLISHER_NM'] = csv_data['PUBLISHER_NM'].astype("string")
csv_data['BOOK_INTRCN_CN'] = csv_data['BOOK_INTRCN_CN'].astype("string")


openai.api_key = os.getenv('API_KEY')
openai.organization = "org-hGPtZbB25DAWDQflBn094cUK"  # https://platform.openai.com/account/org-settings

# https://platform.openai.com/docs/models/gpt-3-5
model_engine = "text-davinci-003"
# 4,096 tokens or about 3,000 words. As a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text.
max_tokens = 1024


def chat_gpt_input(text):
    response = openai.Completion.create(model=model_engine, prompt=text, temperature=0, max_tokens=max_tokens)
    return response.choices[0].text


def ask_librarian(question):
    csv_header = """ \"\"\" 
                ,ISBN_NO,MUMM_LON_HALFLIFE_CO,TITLE_NM,AUTHR_NM,PUBLISHER_NM,BOOK_INTRCN_CN,Combined,KDC_1
                \"\"\"
            """

    column_description = """
        TITLE_NM: 책 제목 
        AUTHR_NM: 저자 이름 
        PUBLISHER_NM: 출판사 
        BOOK_INTRCN_CN: 책 소개 
        """
    """0. pandas 쿼리를 써야한다 다음과 같은 코드에서 answer_sql에 들어갈 값 ( pd.read_csv(csv_path); csv_data.query(answer_sql))"""
    prompt_asking_sql = """ 
        csv header: {}
        csv header 설명: {}
        질문:{}  
        다음과 같은 조건을 만족해야함, 
        0. pandas 쿼리를 써야한다 다음과 같은 코드에서 query 에 들어갈 값 ( pd.read_csv(csv_path); csv_data.query(query); )
        1. 사용할 수 있는 column는 TITLE_NM, AUTHR_NM, PUBLISHER_NM, BOOK_INTRCN_CN 4개이다
        2. 쿼리에 'BOOK_INTRCN_CN'이란 열을 포함해야 됨
        3. 질문에 연관성 있는 정보도 추출해야 함
        4. 값만 적어주고 다른 글자는 적지 않을 것 ex) column_name.str.contains("keyword")
        5. csv 검색시 한국어 키워드로 검색할 것
        6. just code, no other text needed
        """.format(csv_header, column_description, question)

    print("SQL: ", prompt_asking_sql)
    answer_sql = chat_gpt_input(prompt_asking_sql)
    # Establishing the connection

    print('answer_sql', answer_sql)
    answer_sql = answer_sql.replace("query", "").replace('Query', "").replace("QUERY", "").replace("쿼리", "")\
        .replace("정답", "").replace(":", "").replace("=", "").strip().strip('"').strip('\'')
    print( answer_sql)
    # Checking if the connection was successful
    query_result = csv_data.query(answer_sql)

    final_question = """
        사서라고 생각하고 행동해. 
        아래와 같은 질문에 답변을 하기 위해서 pandas에 검색을해서 아래와 같은 결과가 나왔을 때
        사용자에게 결과를 알려줘 
        사용자 질문: {} 
        csv header: {}
        csv header 설명: {}
        사용한 pandas 쿼리: {}
        쿼리 결과: {}" 
        """.format(question, csv_header, column_description, answer_sql, query_result)
    final_answer = chat_gpt_input(final_question)
    return final_answer


if __name__ == '__main__':
    # Ref: https://community.openai.com/t/how-i-put-chatgpt-giving-recomendations-based-on-database/85115/4
    user_question = "학습에 관련된 책을 추천해줘"
    answer_to_question = ask_librarian(user_question)
    print("답변: ", answer_to_question)