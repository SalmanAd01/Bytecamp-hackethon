import requests
from bs4 import BeautifulSoup
url = "https://m.indiamart.com/impcat/potato.html"
ALL_PRODUCTS=["muskmelon","potato","onion","tomato","brinjal","cabbage","cauliflower","capsicum","carrot","chilli","garlic","ginger","green-chilli","green-peas","lemon","mushroom","okra","onion","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","radish","spinach","sweet-potato","tomato","turmeric","watermelon","beetroot","bitter-gourd","bottle-gourd","cucumber","drumstick","eggplant","green-beans","green-capsicum","green-chilli","green-peas","jackfruit","lemon","mango","mushroom","okra","onion","orange","papaya","peas","pineapple","potato","rice"]
REQ = "https://m.indiamart.com/ajaxrequest/unidentified/mcat?flName=567&cityFlName=&start=1&end=56&bizValue=&ecomValue=&in_country_iso=0&language=en&glusrid=&cityid"

# r = requests.get(url)
# soup = BeautifulSoup(r.content, 'html.parser')
# # print(soup)
# paras = soup.find_all('div')
# bgef = soup.find('div', class_="bgef")
# # uls =bgef.index('ul')
# print(bgef.find_all('div'))
# # ul name articles_1
# # li name article
# # a name article_title
# r.json()
 
# print response
# print(response)
 
# print json content
# dataDict = {
#     name:"",
#     price:"",
#     link:"",
#     image:"",
#     contact:"",
#     ownerName:"",
#     ownerLink:"",
#     city:"",
#     district:"",
#     unit:"",
#     standardPrice:"",

# }
dataList = []
for r in ALL_PRODUCTS:
    try:
        url = REQ.replace("567",r)
        response = requests.get(url)
        # print(url)
        data = response.json()
        # print(data['data'])
        for i,d in enumerate(data['firstListData']):
            # print(d)
            try:
                dataList.append({
                    "original":r,
                    "name":d[0]["productName"],
                    "price":d[0]["price"],
                    "link":d[0]["companyUrl"],
                    "image":d[0]["imgUrl"],
                    "contact":d[0]["companyContactNo"],
                    "ownerName":d[0]["companyName"],
                    "city":d[0]["city"],
                    "district":d[0]["district"],
                    "unit":d[0]["unit"],
                    "standardPrice":d[0]["standardPrice"],
                    
                })
            except:
                print(i,d[0])
    except:
        print("error")
import json
with open('data.json', 'w') as outfile:
    json.dump(dataList, outfile, indent=4)

# print(len(dataList))
