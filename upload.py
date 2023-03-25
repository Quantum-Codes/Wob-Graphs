import requests, os, base64, time, json

delay = 1 #bruh imgbb why 0.5 doesnt work
token = os.environ["Token"]
files = os.listdir("images")
files_light = os.listdir("lightimages")
files.remove("README.md")
files_light.remove("README.md")

def upload_img(filename, folder):
  with open(f"{folder}/{filename}", "rb") as image_file: 
    img = base64.b64encode(image_file.read())
    
  x = requests.post("https://api.imgbb.com/1/upload", data={"key": token, "image":img, "expiration": 14*24*3600}) #expire in 2 weeks
  if x.status_code != 200:
    print(x.status_code)
    print(vars(x))
    time.sleep(2)
    x = requests.post("https://api.imgbb.com/1/upload", data={"key": token, "image":img, "expiration": 14*24*3600})
  return x.json()["data"]["url"]

url = {}
for item in files: #dark mode
  print("wip dark", item)
  url["dark_" + item] = upload_img(item, "images")
  time.sleep(delay)

for item in files: #light mode
  print("wip light", item)
  url["light_" + item] = upload_img(item, "lightimages")
  time.sleep(delay)

with open("url.json", "r") as file:
  data = json.loads(file.read())
  
data.update(url)
with open("url.json", "w") as file:
  file.write(json.dumps(data, indent=2))

print("Success!")
