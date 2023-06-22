import pymysql
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, State
import datetime


ALLOWED_TYPES = ("email", "text")
subscribe = pd.DataFrame(columns=["EMAIL", "KDC", "SRCHWRD","DATE"])

app = dash.Dash(__name__)

kdc_dict_total = {
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

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Input(
                    id="input_{}".format("email"),
                    type="email",
                    placeholder="{} 입력하세요".format("등록할 Email을"),
                    style={"height": "30px", "font-size": "16px", "margin-right": "15px"}
                ),
                dcc.Input(
                    id="input_{}".format("text"),
                    type="text",
                    placeholder="{} 입력하세요".format("검색어를"),
                    style={"height": "30px", "font-size": "16px"}
                ),
            ],
            style={"margin-bottom": "20px"},
        ),
        
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": kdc_dict_total[kdc], "value": kdc}
                for kdc in kdc_dict_total
            ],
            value='0',  # 기본 선택값을 '총류'로 설정
            placeholder="분류를 선택하세요",
            style={"height": "30px", "width": "420px", "font-size": "16px"},
        ),
        html.Button(
            "구독하기",
            id="button",
            n_clicks=0,
            style={"height": "30px", "font-size": "16px", "margin-left": "150px", "margin-top": "30px"}
        ),
        html.Div(id="out-all-types"),
    ],
    style={"margin-top": "50px"},
)


@app.callback(
    Output("out-all-types", "children"),
    [Input("button", "n_clicks")],
    [
        State("input_email", "value"),
        State("input_text", "value"),
        State("dropdown", "value"),
    ],
)
def cb_render(n_clicks, email_value, text_value, dropdown_value):
    global subscribe  # 전역 변수로 선언
    if n_clicks > 0:
        if not email_value:
            return html.Div("이메일을 입력하세요.", style={"color": "red", "margin-left": "120px"})
        
        data = {
            "EMAIL": email_value,
            "KDC": dropdown_value,
            "SRCHWRD": text_value,
            "DATE": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        df = pd.DataFrame(data, index=[0])
        subscribe = pd.concat([subscribe, df], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f"subscribe_{current_date}.csv"  # 매 날짜마다 새로운 csv 추가 생성 (불필요하면 삭제 예정)
        subscribe.to_csv(file_name, index=False)  # 데이터프레임을 CSV 파일에 추가
        print(subscribe)
        
        # Connect to MySQL
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            db='library',
            charset='utf8'
        )
        tablename ="Subscribe"

        # Create table if it doesn't exist
        sql = f'''CREATE TABLE IF NOT EXISTS {tablename} (  
                EMAIL varchar(255),
                KDC varchar(255),
                SRCHWRD varchar(255),
                DATE date
                )
              '''
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()

        # Insert data into the table
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                email = row['EMAIL']
                kdc = row['KDC']
                srchwrd = row['SRCHWRD']
                date = row['DATE']
                sql = f"INSERT INTO {tablename} (EMAIL, KDC, SRCHWRD, DATE) VALUES ('{email}', '{kdc}', '{srchwrd}', '{date}')"
                cur.execute(sql)
            conn.commit()

        # Close the connection
        conn.close()
        return html.Div("구독을 신청하였습니다.", style={"color": "red", "margin-left": "120px"})
  
if __name__ == "__main__":
    app.run_server(debug=True)


