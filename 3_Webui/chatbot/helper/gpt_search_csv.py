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
                ISBN_NO, TITLE_NM,AUTHR_NM,PUBLISHER_NM,BOOK_INTRCN_CN
                \"\"\"
            """

    column_description = """
        TITLE_NM: 책 제목 
        AUTHR_NM: 저자 이름 
        PUBLISHER_NM: 출판사 
        BOOK_INTRCN_CN: 책 소개 
        ISBN_NO: ISBN
        """
    """0. pandas 쿼리를 써야한다 다음과 같은 코드에서 answer_sql에 들어갈 값 ( pd.read_csv(csv_path); csv_data.query(answer_sql))"""
    prompt_asking_sql = """ 
        csv header: {}
        csv header 설명: {}
        사용자입력:{}  
        다음과 같은 조건을 만족해야함, 
        1. 사용자입력을 받아 그에 관련된 책을 찾아야한다
        2. pandas 쿼리를 써야한다 - 다음과 같은 코드에서 query 에 들어갈 값 ( pd.read_csv(csv_path); csv_data.query(query); )
        3. 사용할 수 있는 column는 TITLE_NM, AUTHR_NM, PUBLISHER_NM, BOOK_INTRCN_CN 4개이다
        4. 쿼리에 'BOOK_INTRCN_CN'이란 열을 포함해야 됨
        5. 질문에 연관성 있는 정보도 추출해야 함
        6. 값만 적어주고 다른 글자는 적지 않을 것 ex) column_name.str.contains("keyword")
        7. 검색하는 단어는 질문에 들어간 또는 연관된 단어를 사용할 것, 영문자로 된 단어를 쓰지 않는다
        8. just code, no other text needed
        """.format(csv_header, column_description, question)

    print("SQL: ", prompt_asking_sql)
    answer_sql = chat_gpt_input(prompt_asking_sql)
    # Establishing the connection

    print('answer_sql raw:', answer_sql)
    answer_sql = answer_sql.replace("query", "").replace('Query', "").replace("QUERY", "").replace("쿼리", "")\
        .replace("정답", "").replace(":", "").replace("=", "").strip().strip('"').strip('\'')
    print("striped: ", answer_sql)
    # Checking if the connection was successful
    query_result = csv_data.query(answer_sql)[['TITLE_NM', 'AUTHR_NM', 'PUBLISHER_NM','BOOK_INTRCN_CN','ISBN_NO']].sample(n=8)
    print("query_result:", query_result)
    final_question = """
        책을 추천하는 사서라고 생각하고 말을 해야해
        아래 데이터프레임을 파싱해서
        데이터 프레임 column은 다음과 같이 파싱할 수 있다
        1. 데이터프레임 헤더 정보: {}
        2. 데이터프레임: {}
        
        책 제목, 저자, 출판사, ISBN을 알려주고
        간단한 책 내용을 요약해서 알려준다
        알려줄 정보는 데이터프레임에 있는 것만 알려줄 것
        가독성이 좋도록 줄바꿈을 넣어 줄 것
        """.format(column_description, query_result)
    final_answer = chat_gpt_input(final_question)
    return final_answer


if __name__ == '__main__':
    # Ref: https://community.openai.com/t/how-i-put-chatgpt-giving-recomendations-based-on-database/85115/4
    user_question = "학습에 관련된 책을 추천해줘"
    answer_to_question = ask_librarian(user_question)
    print("답변: ", answer_to_question)