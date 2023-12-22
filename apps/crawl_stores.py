from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import json

def no_space(text):
  text1 = re.sub('\n\n\n', '', text)
  text2 = re.sub('\n\n', '', text1)
  return text2

def no_space2(text):
  text1 = re.sub('\n', '', text)
  text2 = re.sub('\n', '', text1)
  return text2


# emart24 편의점 1+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def emart24_11():
    event_11_url = 'https://www.emart24.co.kr/goods/event?search=&page={}&category_seq=1&align='
    
    emart_event_11_items = []
    emart_event_11_images = []
    i = 1
    maxNum=0
    while(i):
        a = urlopen(event_11_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_tag = soup.find_all("div", "itemTxtWrap")
        itemCount = 0
        for txt in div_tag:
            itemCount += 1
            lst = []
            text = no_space(txt.text)
            lst = text.split('\n')
            emart_event_11_items.append(lst)
                    
        img_tag = soup.find_all("div", "itemImg")
        for images in img_tag:
            image = images.find("img")
            image = image.get("src")
            emart_event_11_images.append(image)
        
        if (maxNum == 0):
            maxNum  = itemCount
        elif (maxNum != itemCount):
            break        
        i=i+1

    # print("emart_24 1+1 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(emart_event_11_items), len(emart_event_11_images)))
    # print(emart_event_11_items)
    # print(emart_event_11_images)

    return emart_event_11_images, emart_event_11_items

# emart24 편의점 2+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def emart24_21():
    event_21_url = 'https://www.emart24.co.kr/goods/event?search=&page={}&category_seq=2&align='

    emart_event_21_items = []
    emart_event_21_images = []

    i = 1
    maxNum=0
    while(i):
        a = urlopen(event_21_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_tag = soup.find_all("div", "itemTxtWrap")
        itemCount = 0
        for txt in div_tag:
            itemCount += 1
            lst = []
            text = no_space(txt.text)
            lst = text.split('\n')
            emart_event_21_items.append(lst)   

        img_tag = soup.find_all("div", "itemImg")
        for images in img_tag:
            image = images.find("img")
            image = image.get("src")
            emart_event_21_images.append(image)   

        if (maxNum == 0):
            maxNum  = itemCount
        elif (maxNum != itemCount):
            break        
        i=i+1

    # print("emart_24 2+1 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(emart_event_21_items), len(emart_event_21_images)))
    # print(emart_event_21_items)
    # print(emart_event_21_images)

    return emart_event_21_images, emart_event_21_items

# emart24 편의점 덤증정 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def emart24_bonus():
    event_bonus_url = 'https://www.emart24.co.kr/goods/event?search=&page={}&category_seq=5&align='
    
    emart_bonus_items = []
    emart_bonus_images = []

    i = 1
    maxNum=0
    while(i):
        a = urlopen(event_bonus_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_tag = soup.find_all("div", "itemTxtWrap")
        itemCount = 0
        for txt in div_tag:
            itemCount += 1
            lst = []
            text = no_space(txt.text)
            lst = text.split('\n')
            emart_bonus_items.append(lst)   

        img_tag = soup.find_all("div", "itemImg")
        for images in img_tag:
            image = images.find("img")
            image = image.get("src")
            emart_bonus_images.append(image)     
        
        if (maxNum == 0):
            maxNum  = itemCount
        elif (maxNum != itemCount):
            break        
        i=i+1

    # print("emart_24 덤증정 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(emart_bonus_items), len(emart_bonus_images)))
    # print(emart_bonus_items)
    # print(emart_bonus_images)
    
    return emart_bonus_images, emart_bonus_items

# gs25 편의점 1+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def gs25_11():
    event_11_url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search?CSRFToken=fb5deca3-2d04-4f1a-949f-c851477891c1&pageNum={}&pageSize=8&searchType=&searchWord=&parameterList=ONE_TO_ONE'
    
    gs25_event_11_items = []
    
    i = 1
    while(i):
        headersList = {"Accept": "*/*", "User-Agent": "Thunder Client (https://www.thunderclient.com)"}
        payload = ""
        reqUrl = event_11_url.format(i)
        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        data= response.json()
        data_json = json.loads(data)
        pageSize = len(data_json['results'])
        for j in range(0, pageSize):
            lst = []
            lst.append(data_json['results'][j]['attFileNmOld'])
            lst.append(data_json['results'][j]['goodsNm'])
            price = data_json['results'][j]['price']
            formatted_price = "{:.0f} 원".format(price)
            lst.append(formatted_price)
            gs25_event_11_items.append(lst)
            
        if (pageSize == 8):
            i = i+1
        else:
            break

    # print("gs25 1+1 행사 상품 수 {}개".format(len(gs25_event_11_items)))
    # print(gs25_event_11_items)
    
    return gs25_event_11_items 

# gs25 편의점 2+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def gs25_21():
    event_21_url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search?CSRFToken=051b5da6-8f00-4a17-9bb0-c425ae1c7065&pageNum={}&pageSize=8&searchType=&searchWord=&parameterList=TWO_TO_ONE'
    
    gs25_event_21_items = []
    
    i = 1
    while(i):
        headersList = {"Accept": "*/*", "User-Agent": "Thunder Client (https://www.thunderclient.com)"}
        payload = ""
        reqUrl = event_21_url.format(i)
        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        data= response.json()
        data_json = json.loads(data)
        pageSize = len(data_json['results'])
        for j in range(0, pageSize):
            lst = []
            lst.append(data_json['results'][j]['attFileNmOld'])
            lst.append(data_json['results'][j]['goodsNm'])
            price = data_json['results'][j]['price']
            formatted_price = "{:.0f} 원".format(price)
            lst.append(formatted_price)
            gs25_event_21_items.append(lst)
            
        if (pageSize == 8):
            i = i+1
        else:
            break

    # print("gs25 2+1 행사 상품 수 {}개".format(len(gs25_event_21_items)))
    # print(gs25_event_21_items)
    
    return gs25_event_21_items 

# gs25 편의점 덤증정 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def gs25_bonus():
    event_bonus_url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods-search?CSRFToken=051b5da6-8f00-4a17-9bb0-c425ae1c7065&pageNum={}&pageSize=8&searchType=&searchWord=&parameterList=GIFT'
    
    gs25_bonus_items = []
    
    i = 1
    while(i):
        headersList = {"Accept": "*/*", "User-Agent": "Thunder Client (https://www.thunderclient.com)"}
        payload = ""
        reqUrl = event_bonus_url.format(i)
        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        data= response.json()
        data_json = json.loads(data)
        pageSize = len(data_json['results'])
        for j in range(0, pageSize):
            lst = []
            lst.append(data_json['results'][j]['attFileNmOld'])
            lst.append(data_json['results'][j]['goodsNm'])
            price = data_json['results'][j]['price']
            formatted_price = "{:.0f} 원".format(price)
            lst.append(formatted_price)
            gs25_bonus_items.append(lst)
            
        if (pageSize == 8):
            i = i+1
        else:
            break

    # print("gs25 덤증정 상품 수 {}개".format(len(gs25_bonus_items)))
    # print(gs25_bonus_items)
    
    return gs25_bonus_items 

# 세븐일레븐 편의점 1+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def seven11_11():
    event_11_url = 'https://www.7-eleven.co.kr/product/listMoreAjax.asp?intPageSize=10&intCurrPage={}&cateCd1=&cateCd2=&cateCd3=&pTab=1'
    
    seven11_event_11_items_name = []
    seven11_event_11_items_price = []
    seven11_event_11_images = []

    i = 0
    while(True):
        a = urlopen(event_11_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_name = soup.find_all("div", "name")
        pageSize = len(div_name)
        for name in div_name:
            name_txt = no_space(name.text)
            seven11_event_11_items_name.append(name_txt)
        
        div_price = soup.find_all("div", "price")
        
        for price in div_price:
            price_txt = no_space(price.text)
            price_txt = no_space2(price_txt)
            formatted_price = f'{price_txt} 원'
            seven11_event_11_items_price.append(formatted_price)
                        
        img_tag = soup.find_all("img")
        for images in img_tag:
            image = images.get("src")
            new_url = 'https://www.7-eleven.co.kr' + image
            seven11_event_11_images.append(new_url)
        
        if (i!=0 and pageSize < 10):
            break
        i = i + 1

    seven11_event_11_items = []
    for j in range(len(seven11_event_11_items_name)):
        seven11_event_11_items.append([])
        seven11_event_11_items[j].append(seven11_event_11_items_name[j])
        seven11_event_11_items[j].append(seven11_event_11_items_price[j])

    # print("세븐일레븐 1+1 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(seven11_event_11_items), len(seven11_event_11_images)))
    # print(seven11_event_11_images)
    # print(seven11_event_11_items)


    return seven11_event_11_images, seven11_event_11_items

# 세븐일레븐 편의점 2+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def seven11_21():
    event_21_url = 'https://www.7-eleven.co.kr/product/listMoreAjax.asp?intPageSize=10&intCurrPage={}&cateCd1=&cateCd2=&cateCd3=&pTab=2'
    
    seven11_event_21_items_name = []
    seven11_event_21_items_price = []
    seven11_event_21_images = []

    i=0
    while(True):
        a = urlopen(event_21_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_name = soup.find_all("div", "name")
        pageSize = len(div_name)
        for name in div_name:
            name_txt = no_space(name.text)
            seven11_event_21_items_name.append(name_txt)
        
        div_price = soup.find_all("div", "price")
        
        for price in div_price:
            price_txt = no_space(price.text)
            price_txt = no_space2(price_txt)
            formatted_price = f'{price_txt} 원'
            seven11_event_21_items_price.append(formatted_price)
                        
        img_tag = soup.find_all("img")
        for images in img_tag:
            image = images.get("src")
            new_url = 'https://www.7-eleven.co.kr' + image
            seven11_event_21_images.append(new_url)
        
        if (i!=0 and pageSize < 10):
            break
        i = i + 1

    seven11_event_21_items = []
    for j in range(len(seven11_event_21_items_name)):
        seven11_event_21_items.append([])
        seven11_event_21_items[j].append(seven11_event_21_items_name[j])
        seven11_event_21_items[j].append(seven11_event_21_items_price[j])

    # print("세븐일레븐 2+1 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(seven11_event_21_items), len(seven11_event_21_images)))
    # print(seven11_event_21_images)
    # print(seven11_event_21_items)


    return seven11_event_21_images, seven11_event_21_items
    
# CU 편의점 1+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def cu_11():

    event_11_url = 'https://cu.bgfretail.com/event/plusAjax.do?pageIndex={}&listType=1&searchCondition=23&user_id='
    
    cu_event_11_items_name = []
    cu_event_11_items_price = []
    cu_event_11_images = []

    maxItem=0
    i = 1
    while(i):
        a = urlopen(event_11_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_name = soup.find_all("div", "name")
        itemCount = len(div_name)
        for name in div_name:
            name_txt = no_space(name.text)
            cu_event_11_items_name.append(name_txt)
        
        div_price = soup.find_all("div", "price")
        for price in div_price:
            price_txt = no_space(price.text)
            price_txt = no_space2(price_txt)
            formatted_price = price_txt.replace('원', ' 원')
            cu_event_11_items_price.append(formatted_price)
                        
        img_tag = soup.find_all("img", "prod_img")
        for images in img_tag:
            image = images.get("src")
            new_url = 'https:' + image
            cu_event_11_images.append(new_url)
        
        if (maxItem==0):
            maxItem=itemCount
        elif (maxItem > itemCount):
            break
        i = i + 1

    cu_event_11_items = []
    for j in range(len(cu_event_11_items_name)):
        cu_event_11_items.append([])
        cu_event_11_items[j].append(cu_event_11_items_name[j])
        cu_event_11_items[j].append(cu_event_11_items_price[j])

    # print("CU 편의점 1+1 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(cu_event_11_items), len(cu_event_11_images)))
    # print(cu_event_11_images)
    # print(cu_event_11_items)


    return cu_event_11_images, cu_event_11_items

# CU 편의점 2+1 행사 상품 상품 이미지, 상품 이름, 가격 정보 리스트에 저장.
def cu_21():

    event_21_url = 'https://cu.bgfretail.com/event/plusAjax.do?pageIndex={}&listType=1&searchCondition=24&user_id='
    
    cu_event_21_items_name = []
    cu_event_21_items_price = []
    cu_event_21_images = []

    maxItem=0
    i = 1
    while(i):
        a = urlopen(event_21_url.format(i))
        soup = BeautifulSoup(a.read(), 'html.parser')
        div_name = soup.find_all("div", "name")
        itemCount = len(div_name)
        for name in div_name:
            name_txt = no_space(name.text)
            cu_event_21_items_name.append(name_txt)
        
        div_price = soup.find_all("div", "price")
        for price in div_price:
            price_txt = no_space(price.text)
            price_txt = no_space2(price_txt)
            formatted_price = price_txt.replace('원', ' 원')
            cu_event_21_items_price.append(formatted_price)
                        
        img_tag = soup.find_all("img", "prod_img")
        for images in img_tag:
            image = images.get("src")
            new_url = 'https:' + image
            cu_event_21_images.append(new_url)
        
        if (maxItem==0):
            maxItem=itemCount
        elif (maxItem > itemCount):
            break
        i = i + 1

    cu_event_21_items = []
    for j in range(len(cu_event_21_items_name)):
        cu_event_21_items.append([])
        cu_event_21_items[j].append(cu_event_21_items_name[j])
        cu_event_21_items[j].append(cu_event_21_items_price[j])

    # print("CU 편의점 2+1 행사 상품 수 {}개 (이미지 파일 {}개)".format(len(cu_event_21_items), len(cu_event_21_images)))
    # print(cu_event_21_images)
    # print(cu_event_21_items)

    return cu_event_21_images, cu_event_21_items


# emart24_11()
# print('\n')
# emart24_21()
# print('\n')
# emart24_bonus()
# print('\n')
# gs25_11()
# print('\n')
# gs25_21()
# print('\n')
# gs25_bonus()
# print('\n')
# seven11_11()
# print('\n')
# seven11_21()
# print('\n')
# cu_11()
# print('\n')
# cu_21()
