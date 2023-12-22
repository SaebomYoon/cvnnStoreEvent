import os, sys
from crawl_stores import emart24_11, emart24_21, emart24_bonus, gs25_11, gs25_21, gs25_bonus, seven11_11, seven11_21, cu_11, cu_21
import oracledb

def connect():
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

    print("\n >>> Successfully connected to Oracle Database <<< \n")

    def create_table(table_name):
        try:
            cursor = conn.cursor()
            sql = f"drop table {table_name}" 
            #print(sql)
            cursor.execute(sql)
            sql = f"CREATE TABLE {table_name} (image_path VARCHAR(256), item_name VARCHAR(128), item_price VARCHAR(128))"
            print(sql)
            cursor.execute(sql)
            print(">>> Created TABLE " + table_name + " Successfully")
            conn.commit()
        except:
            print('[ERROR]: Create table')

    table_names = ["emart24_11" , "emart24_21", "emart24_bonus", "gs25_11", "gs25_21", "gs25_bonus", "seven11_11", "seven11_21", "cu_21", "cu_11"]

    for _, table_name in enumerate(table_names):
        create_table(table_name)


    print("\n >>> Query starts ....\n")
    try:
        print("\n emart24의 1+1 행사 상품을 db의 emart24_11 테이블에 insert 수행.... \n")

        emart24_11_images, emart24_11_items = emart24_11()
        cursor = conn.cursor()
        for idx, img_path in enumerate(emart24_11_images):
            sql = "INSERT INTO emart24_11 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': emart24_11_items[idx][0],
                'item_price': emart24_11_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into emart24_11 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n emart24의 2+1 행사 상품을 db의 emart24_21 테이블에 insert 수행.... \n")
        
        emart24_21_images, emart24_21_items = emart24_21()
        cursor = conn.cursor()
        for idx, img_path in enumerate(emart24_21_images):
            sql = "INSERT INTO emart24_21 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': emart24_21_items[idx][0],
                'item_price': emart24_21_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into emart24_21 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n emart24의 덤증정 상품을 db의 emart24_bonus 테이블에 insert 수행.... \n")
        
        emart24_bonus_images, emart24_bonus_items = emart24_bonus()
        cursor = conn.cursor()
        for idx, img_path in enumerate(emart24_bonus_images):
            sql = "INSERT INTO emart24_bonus (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': emart24_bonus_items[idx][0],
                'item_price': emart24_bonus_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into emart24_bonus Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n gs25의 1+1 행사상품을 db의 gs25_11 테이블에 insert 수행.... \n")

        gs25_11_items = gs25_11()
        cursor = conn.cursor()
        for item in gs25_11_items:
            sql = "INSERT INTO gs25_11 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': item[0],
                'item_name': item[1],
                'item_price': item[2]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into gs25_11 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n gs25의 2+1 행사상품을 db의 gs25_21 테이블에 insert 수행.... \n")

        gs25_21_items = gs25_21()
        cursor = conn.cursor()
        for item in gs25_21_items:
            sql = "INSERT INTO gs25_21 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': item[0],
                'item_name': item[1],
                'item_price': item[2]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into gs25_21 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n gs25의 덤증정 품을 db의 gs25_bonus 테이블에 insert 수행.... \n")

        gs25_bonus_items = gs25_bonus()
        cursor = conn.cursor()
        for item in gs25_bonus_items:
            sql = "INSERT INTO gs25_bonus (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': item[0],
                'item_name': item[1],
                'item_price': item[2]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into gs25_bonus Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n 세븐일레븐의 1+1 행사상품을 db의 seven11_11 테이블에 insert 수행.... \n")

        seven11_11_images, seven11_11_items = seven11_11()
        cursor = conn.cursor()
        for idx, img_path in enumerate(seven11_11_images):
            sql = "INSERT INTO seven11_11 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': seven11_11_items[idx][0],
                'item_price': seven11_11_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into seven11_11 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n 세븐일레븐의 2+1 행사상품을 db의 seven11_21 테이블에 insert 수행.... \n")

        seven11_21_images, seven11_21_items = seven11_21()
        cursor = conn.cursor()
        for idx, img_path in enumerate(seven11_21_images):
            sql = "INSERT INTO seven11_21 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': seven11_21_items[idx][0],
                'item_price': seven11_21_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into seven11_21 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n CU의 1+1 행사상품을 db의 cu_11 테이블에 insert 수행.... \n")

        cu_11_images, cu_11_items = cu_11()
        cursor = conn.cursor()
        for idx, img_path in enumerate(cu_11_images):
            sql = "INSERT INTO cu_11 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': cu_11_items[idx][0],
                'item_price': cu_11_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into cu_11 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    try:
        print("\n CU의 2+1 행사상품을 db의 cu_21 테이블에 insert 수행.... \n")

        cu_21_images, cu_21_items = cu_21()
        cursor = conn.cursor()
        for idx, img_path in enumerate(cu_21_images):
            sql = "INSERT INTO cu_21 (image_path, item_name, item_price) VALUES (:img_path, :item_name, :item_price)"
            params = {
                'img_path': img_path,
                'item_name': cu_21_items[idx][0],
                'item_price': cu_21_items[idx][1]
            }
            cursor.execute(sql, params)
        conn.commit()
        print(">>> Data inserted into cu_21 Successfully")
    except Exception as e:
        print(f"Insert ERROR: {e}")
        conn.rollback()

    # Release database resources.
    try:
        print("\n >>> Cursor/connection closing...\n")
        cursor.close()
        conn.close()
        print("\n <<< Cursor/connection closed.\n")
    except:
        print('Quit ERROR.')
