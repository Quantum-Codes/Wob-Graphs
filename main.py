import requests, os
import base64
import matplotlib.pyplot as plt

def upload_img(filename):
  with open(filename, "rb") as image_file: 
    img = base64.b64encode(image_file.read())

  x = requests.post("https://api.imgbb.com/1/upload", data={"key":os.environ['key'], "image":img})
  print(x.json()["data"]["url"])

x = [1,"",2," ",3]#time
y = [0,50,60,75,80]#follow
plt.plot(x, y, "o--", c = '#4CAF50')
plt.grid()
plt.xlabel('Timestamp')
plt.ylabel('Followers')
plt.title("{User}'s follow graph")
plt.savefig('images/graph.svg')