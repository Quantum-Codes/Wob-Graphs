import requests, os, base64, time, json
token = os.environ["Token"]
files = os.listdir("images")
files.remove("README.md")

def upload_img(filename):
  with open(f"images/{filename}", "rb") as image_file: 
    img = base64.b64encode(image_file.read())
  #print(img)
  x = requests.post("https://api.imgbb.com/1/upload", data={"key": token, "image":img, "expiration": 14*24*3600})
  #print(x.json()["data"]["expiration"])
  if x.status_code != 200:
    print(x.status_code)
    print(vars(x))
    time.sleep(2)
    x = requests.post("https://api.imgbb.com/1/upload", data={"key": token, "image":img, "expiration": 14*24*3600})
  return x.json()["data"]["url"]

url = {}
for item in files:
  print("wip", item)
  url[item] = upload_img(item)
  time.sleep(0.5)

with open("url.json", "r") as file:
  data = json.loads(file.read())
  
data.update(url)
with open("url.json", "w") as file:
  file.write(json.dumps(data, indent=2))

print("Success!")
