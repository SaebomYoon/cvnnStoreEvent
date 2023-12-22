import os, sys
from flask import Flask, render_template, request, url_for
import connect_db 
import oracledb
from flask import session
from urllib.parse import quote
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
conn = None  # 전역 변수로 선언

scheduler = BackgroundScheduler()
#app.secret_key = 'YOUR_SECRET_KEY'

# 한 페이지에 표시할 항목 수
ITEMS_PER_PAGE = 5

@app.route('/')
def home1():
    global conn

    os.chdir('C:\oracle\instantclient_21_12')
    os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')

    #USER_ID = "YOUR_USER_ID"
    #USER_PW = "YOUR_USER_PW"
    CONN_STR = "localhost:1521/orcl"

    lib_dir = "C:\\oracle\\instantclient_21_12"
    try:
        print("\n >> Oracle client initiatization starts ... \n")
        oracledb.init_oracle_client(lib_dir=lib_dir)
    except Exception as err:
        print("Error connecting: cx_Oracle.init_oracle_client()")
        print(err)
        sys.exit(1)

    print("\n <<< Oracle client initiatiatization ended ...\n")

    # Make a connection
    try:
        conn = oracledb.connect(user=USER_ID, password=USER_PW, dsn=CONN_STR)
        cursor = conn.cursor()
    except:
        print('Cannot get a connection.')

    return render_template('index.html')

@app.route('/index2')
def home2():
    
    return render_template('index2.html')

def updateEvents():
    # fetch from each convience store
    connect_db.connect()

# 스케줄러에 updateEvents 함수를 7일 간격으로 실행하도록 추가
scheduler.add_job(updateEvents, 'interval', days=7)

@app.route('/search', methods=['POST', 'GET'])  # GET 메서드 추가
def search():
    if request.method == 'POST':
        product = request.form.get('product')  # 제품 이름 가져오기
    else:
        product = request.args.get('product')  # GET 요청의 경우, query string에서 제품 이름 가져오기

    cursor = conn.cursor()

    # 페이지 번호 가져오기. POST 요청에서도 페이지 번호를 받을 수 있도록 수정
    page = request.form.get('page', 1, type=int) if request.method == 'POST' else request.args.get('page', 1, type=int)
    
    # 결과를 저장할 리스트 생성
    results = []

    # 여러 테이블에서 제품 검색
    tables = ['CU_11', 'CU_21', 'EMART24_11', 'EMART24_21', 'GS25_11', 'GS25_21', 'SEVEN11_11', 'SEVEN11_21']
    for table in tables:
        cursor.execute(f"SELECT IMAGE_PATH, ITEM_NAME, ITEM_PRICE FROM (SELECT DISTINCT ITEM_NAME, IMAGE_PATH, ITEM_PRICE FROM {table}) WHERE ITEM_NAME LIKE :ITEM_NAME", {'ITEM_NAME': '%%' + product + '%%'})
        result = cursor.fetchall()
        if result:
            # 결과가 있으면 테이블 이름을 추가하고 리스트에 추가
            for res in result:
                if 'CU_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/cu_logo.jpg')))
                elif 'CU_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/cu_logo.jpg')))
                elif 'GS25_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/gs25_logo.jpg')))
                elif 'GS25_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/gs25_logo.jpg')))
                elif 'EMART24_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/emart24_logo.jpg')))
                elif 'EMART24_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/emart24_logo.jpg')))
                elif 'SEVEN11_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/seven11_logo.jpg')))
                elif 'SEVEN11_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/seven11_logo.jpg')))


    # 페이지네이션 구현
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_products = results[start:end]

    # 총 페이지 수 계산
    total_pages = (len(results) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # 결과가 없을 때 메시지 설정
    if not results:
        return render_template('search_results_no.html', message="검색 결과가 없습니다.")

    # 결과를 HTML로 전달
    return render_template('search_results.html', products=page_products, total_pages=total_pages, product=product, page=page)


@app.route('/search2', methods=['POST', 'GET'])
def search2():
    page = request.form.get('page', 1, type=int) if request.method == 'POST' else request.args.get('page', 1, type=int)

    cursor = conn.cursor()
    products = []
    total_count = 0

    if request.method == 'POST':
        event_type = request.form.get('event_type')
        store_name = request.form.get('store_name')
        session['event_type'] = event_type
        session['store_name'] = store_name
    else:
        event_type = session.get('event_type')
        store_name = session.get('store_name')

    if event_type and store_name:
        table_name = f"{store_name}_{event_type.replace('+','')}"
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_count = cursor.fetchone()[0]

        start = (page - 1) * 7 + 1
        end = start + 7 - 1
        sql = f"""
        SELECT * FROM (
            SELECT t.*, ROW_NUMBER() OVER (ORDER BY NULL) as rn
            FROM (
                SELECT DISTINCT *
                FROM {table_name}
            ) t
        ) WHERE rn BETWEEN {start} AND {end}
        """ 
        cursor.execute(sql)
        products = cursor.fetchall()

    total_page = (total_count - 1) // 7 + 1

    image_url = url_for('static', filename=f'images/{event_type.replace("+", "_")}.jpg')

    return render_template('search_results2.html', products=products, page=page, total_page=total_page, image_url=image_url)


@app.route('/index3')
def home3():
    return render_template('index3.html')

@app.route('/index4')
def home4():
    return render_template('index4.html')

@app.route('/index5')
def home5():
    return render_template('index5.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/search3', methods=['POST'])
def search3():
    convenience_store = request.form['convenience_store']
    location = request.form['location']

    # 사용자가 위치 정보를 입력하지 않았다면 적절한 메시지 반환
    if not location:
        return "위치 정보를 입력해주세요."

    # 카카오 API를 활용해 주소를 좌표로 변환
    url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + location
    headers = {"Authorization": "KakaoAK YOUR_APP_KEY"}
    response = requests.get(url, headers=headers)
    data = response.json()

    print(data)  # 응답 출력

    if 'documents' in data and len(data['documents']) > 0:
        latitude = data["documents"][0]["y"]
        longitude = data["documents"][0]["x"]

        # 카카오 API를 활용해 주변의 편의점 검색
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?y={latitude}&x={longitude}&radius=1000&query={convenience_store}"
        response = requests.get(url, headers=headers)
        store_data = response.json()

        print(store_data)  # 응답 출력

        if 'documents' in store_data and len(store_data['documents']) > 0:
            stores = store_data['documents']
        else:
            print('검색 결과가 없습니다.')
            stores = []
    else:
        print('검색 결과가 없습니다.')
        latitude, longitude, stores = None, None, []

    return render_template('search_results3.html', latitude=latitude, longitude=longitude, store=convenience_store, stores=stores)

@app.route('/search_price', methods=['GET', 'POST'])
def search_price():

    cursor = conn.cursor()

    # POST 메서드로 요청이 왔을 때 가격 범위 설정
    if request.method == 'POST':
        price_range = request.form.get('price_range')
        session['price_range'] = price_range
    else:
        price_range = session.get('price_range')

    lower, upper = price_range.split('~') if '~' in price_range else (0, price_range[:-1])
    lower = int(lower)
    upper = int(upper) if upper else 99999999

    # 결과를 저장할 리스트 생성
    results = []

    # 여러 테이블에서 가격 범위에 해당하는 제품 검색
    tables = ['CU_11', 'CU_21', 'EMART24_11', 'EMART24_21', 'GS25_11', 'GS25_21', 'SEVEN11_11', 'SEVEN11_21']
    for table in tables:
        cursor.execute(f"SELECT IMAGE_PATH, ITEM_NAME, ITEM_PRICE FROM {table} WHERE TO_NUMBER(REPLACE(REPLACE(ITEM_PRICE, ' 원', ''), ',', '')) BETWEEN :lower AND :upper", {'lower': lower, 'upper': upper})
        result = cursor.fetchall()
        if result:
            # 결과가 있으면 테이블 이름을 추가하고 리스트에 추가
            for res in result:
                if 'CU_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/cu_logo.jpg')))
                elif 'CU_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/cu_logo.jpg')))
                elif 'EMART24_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/emart24_logo.jpg')))
                elif 'EMART24_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/emart24_logo.jpg')))
                elif 'GS25_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/gs25_logo.jpg')))
                elif 'GS25_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/gs25_logo.jpg')))
                elif 'SEVEN11_11' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/1_1.jpg'), url_for('static', filename='images/seven11_logo.jpg')))
                elif 'SEVEN11_21' in table:
                    results.append((res[0], res[1], res[2], url_for('static', filename='images/2_1.jpg'), url_for('static', filename='images/seven11_logo.jpg')))
    
    # 페이지 번호 가져오기. GET 메서드로 요청이 왔을 때 페이지 번호를 가져옴
    page = request.args.get('page', 1, type=int) if request.method == 'GET' else 1

    # 페이지네이션 구현
    ITEMS_PER_PAGE = 7
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    page_products = results[start:end]

    # 총 페이지 수 계산
    total_pages = (len(results) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # 결과를 HTML로 전달
    return render_template('search_results4.html', products=page_products, total_pages=total_pages, page=page)

if __name__ == '__main__':
    #updateEvents()
    # 스케줄러 시작
    scheduler.start()
    
    app.run(port=5000)