import requests, os, base64, time, json

delay = 1 #bruh imgbb why 0.5 doesnt work
token_dark = os.environ["token_dark"]
token_light = os.environ["token_light"]
files = os.listdir("images")
files_light = os.listdir("lightimages")
files.remove("README.md")
files_light.remove("README.md")

def upload_img(filename, folder, mode):
  with open(f"{folder}/{filename}", "rb") as image_file: 
    img = base64.b64encode(image_file.read())
    
  if mode = "dark":
    token = token_dark #interchanging tokens does nothing special. the point is to reside image uploaded per token to not be ratelimited.
  else:
    token = token_light
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
  url["dark_" + item] = upload_img(item, "images", "dark")
  time.sleep(delay)

for item in files: #light mode
  print("wip light", item)
  url["light_" + item] = upload_img(item, "lightimages", "light")
  time.sleep(delay)

with open("url.json", "r") as file:
  data = json.loads(file.read())
  
data.update(url)
with open("url.json", "w") as file:
  file.write(json.dumps(data, indent=2))

print("Success!")
