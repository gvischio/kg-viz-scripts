import requests
from time import sleep
from csv import writer

headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
    
def getImageURL():
    str = requests.request("GET", "https://source.unsplash.com/random/1200x675/", headers=headers).url
    str = str[:str.index("?")]
    str = str + "?w=1200&h=675&fit=crop"
    return str

with open("04 - Generated data\pictures_of_events.csv", "w", newline='') as outp:
    csv_writer = writer(outp)
    csv_writer.writerow(["pictureID", "url", "of_person", "of_location", "of_event"])

    for i in range(2300, 3000):
        row = ["P"+str(i), getImageURL(), "", "", ""]
        csv_writer.writerow(row)
        sleep(0.25)
