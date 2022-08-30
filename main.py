import requests, os, json, datetime
import base64
import matplotlib.pyplot as plt
#from matplotlib.ticker import AutoMinorLocator
plt.style.use(['dark_background'])

def upload_img(filename):
  with open(filename, "rb") as image_file: 
    img = base64.b64encode(image_file.read())

  x = requests.post("https://api.imgbb.com/1/upload", data={"key":os.environ['key'], "image":img})
  print(x.json()["data"]["url"])

def graph(user, type):
  try:
    with open(f"stats/{user}.json", "r") as file:
      data = json.loads(file.read())
  except FileNotFoundError:
    return
  y = data[type]
  x = []
  for item in data["timestamp"]:
   date = datetime.datetime.utcfromtimestamp(item).strftime('%d-%m-%Y')
   x.append(date[:-4] + date[-2:])
  plt.figure()
  plt.plot(x, y, "o--", c = "yellow", linewidth=3)
  #minor_locator = AutoMinorLocator(5)
  #plt.axes().yaxis.set_yticklabels(tick_labels.astype(int))
  plt.grid(c="#7a7a7a")
  plt.xlabel('Timestamp')
  plt.ylabel(type.title())
  plt.ticklabel_format(style='sci')
  plt.xticks(rotation=45)
  plt.title(f"{data['name']}'s {type} graph")
  plt.tight_layout()
  plt.savefig(f"images/{user}-{type}.svg")
  plt.close()

#print(tracklist)

def graph_all():
  tracklist = requests.get("https://Wasteof-api-test.quantumcodes.repl.co/track", headers={ "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).json()

  for item in tracklist:
    print(item)
    graph(item, "followers")
    graph(item, "following")
    graph(item, "posts")

graph("60db0c5a956cdbbd0489eff6", "posts")