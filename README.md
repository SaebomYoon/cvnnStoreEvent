# 개발 환경
* VSCODE IDE를 사용하여 개발하였습니다.
* Window 환경을 사용했습니다.
* Oracle을 설치하여 진행하였습니다.
* Python 언어로 작성된 웹 프레임워크인 Flask를 사용하였습니다.
* Database 접속을 위해 다음과 같이 설정하였습니다. user_name = cvnnstore, user_passwd=cvnnstore 

# 실행 방법
1. Database 접속합니다.
 - 예) user_name = cvnnstore, user_passwd=cvnnsotre 
2. pip_list.txt 참고하여 개발 환경을 세팅합니다.
3. 코드에서 YOUR_APP_KEY(카카오 맵), app.secret_key, ORACLE_HOME, ORACLE_USER_ID, ORACLE_USER_PW, ORACLE_CONN_STR을 설정해야 합니다. 
3. apps/app.py 실행합니다.
   * updateEvents()를 실행시켜, 편의점 4곳의 행사정보를 크롤링하여 db에 저장합니다.
   * 이후, updateEvents()를 주석처리하여 scheduler.start() 설정하여 7일 간격으로 db가 업데이트 되도록 합니다.
4. http://127.0.0.1:5000 에 접속합니다.

# 시스템이 제공하는 서비스 소개
* 편의점에서는 매달마다 1+1, 2+1 행사를 진행합니다.
* '나는 오늘 저녁으로 진짬뽕을 먹고 싶은데, 내 주변 편의점들 중에서 진짬뽕을 1+1 또는 2+1 하는 곳이 어디일까?' 라는 일상 속 고민에서 이 서비스를 개발하게 되었습니다.
* 현재 위치에서 가장 가까운 편의점을 보여주는 기능을 통해 행사 정보를 바탕으로 가장 가까운 편의점으로 빨리 가서 구매할 수 있게 하였습니다.
* 특별히 먹고 싶은 게 없을 때, 원하는 가격대의 행사 상품을 구매할 수 있도록 가격대별 편의점 행사상품을 추천하였습니다.

# 데모 링크

 https://discovered-cold-37f.notion.site/_-bc54b243e9944643a54deb8ab793b6e1