from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests
import json

driver = webdriver.Chrome("/Users/edmundoogaz/sources/python/scrapping/chromedriver")

row=[]
array=[]
data = '{ "results" : [ { "address_components" : [ { "long_name" : "21", "short_name" : "21", "types" : [ "street_number" ] }, { "long_name" : "General Jofré", "short_name" : "Gral. Jofré", "types" : [ "route" ] }, { "long_name" : "Santiago", "short_name" : "Santiago", "types" : [ "locality", "political" ] }, { "long_name" : "Santiago", "short_name" : "Santiago", "types" : [ "administrative_area_level_3", "political" ] }, { "long_name" : "Santiago", "short_name" : "Santiago", "types" : [ "administrative_area_level_2", "political" ] }, { "long_name" : "Región Metropolitana", "short_name" : "Región Metropolitana", "types" : [ "administrative_area_level_1", "political" ] }, { "long_name" : "Chile", "short_name" : "CL", "types" : [ "country", "political" ] } ], "formatted_address" : "Gral. Jofré 21, Santiago, Región Metropolitana, Chile", "geometry" : { "location" : { "lat" : -33.4440938, "lng" : -70.63373659999999 }, "location_type" : "ROOFTOP", "viewport" : { "northeast" : { "lat" : -33.44274481970849, "lng" : -70.6323876197085 }, "southwest" : { "lat" : -33.44544278029149, "lng" : -70.6350855802915 } } }, "place_id" : "ChIJu2et93fFYpYR6Z2khdOkF9U", "plus_code" : { "compound_code" : "H948+9G Santiago, Chile", "global_code" : "47RFH948+9G" }, "types" : [ "street_address" ] } ], "status" : "OK" }'

# pages = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# pages = [5,6]
pages = range(11,14)
for page in pages:

    driver.get("https://codigoazul.ministeriodesarrollosocial.gob.cl/albergues?buscar=&region=&tipo_servicio=&page="+str(page))
    content = driver.page_source
    soup = BeautifulSoup(content)
    for tr in soup.findAll('tr', attrs={'class':'even'}):
        count = 1
        url = ""
        for td in tr.findAll('td'):
            row.append(td.text+";")
            if count == 5:
                replaced = td.text.replace(" ", "+")
                url = "https://maps.googleapis.com/maps/api/geocode/json?address="+replaced+"&key=AIzaSyBr8k58m1tkHh0QNc5S2KRzcpDYuMREu0A"
                # url = "https://run.mocky.io/v3/55df6ed3-d414-4941-b0ff-01639a0609a6"
                resp = requests.get(url)
                dictionary = resp.json()
                print (dictionary)
                # dictionary = json.loads(data)
                lat = dictionary["results"][0]["geometry"]["location"]["lat"]
                lng = dictionary["results"][0]["geometry"]["location"]["lng"]

            count+=1
        row.append(str(lat)+";")
        row.append(str(lng)+";")
        row.append(url+";")
        array.append(row)
        row=[]

    print (array)

with open('codigoAzulPag11y12y13.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(array)