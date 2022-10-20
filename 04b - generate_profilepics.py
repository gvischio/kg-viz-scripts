import requests
from time import sleep
from csv import reader, writer

headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.5", "Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
    
def getImageURL():
    str = requests.request("GET", "https://source.unsplash.com/random/300x300/?portrait", headers=headers).url
    str = str[:str.index("?")]
    str = str + "?w=300&h=300&fit=crop"
    return str

with open("04 - Generated data\profile_pics.csv", "r") as inp:
    with open("04 - Generated data\profile_pics2.csv", "w", newline='') as outp:
        csv_reader = reader(inp)
        csv_writer = writer(outp)
        header = next(csv_reader)
        csv_writer.writerow(header)

        for row in csv_reader:
            row[2] = getImageURL()
            csv_writer.writerow(row)
            sleep(0.25)
