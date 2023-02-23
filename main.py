import requests, json, datetime
import matplotlib.pyplot as plt
plt.style.use('dark_background')


def graph(user, type1, multi=False, light=False):
  if light:
    c = None #use default
  else:
    c = "yellow"
  if multi:
    global lines
  fig = plt.figure()
  if multi:
    for item in lines[type1]:
      plt.plot(item[0], item[1], "o--", linewidth=3)
    name = "Wasteof"
    plt.title(f"wasteof.money's aggregate {type1} graph")
  else:
    try:
      with open(f"stats/{user}.json", "r") as file:
        data = json.load(file)
    except FileNotFoundError:
      return "no file"
    y = data[type1]
    x = []
    for item in data["timestamp"]:
      date = datetime.datetime.utcfromtimestamp(item).strftime('%d-%m-%Y')
      x.append(date[:-4] + date[-2:])
    plt.plot(x, y, "o--", c = c, linewidth=3)
    name = data['name']
    plt.title(f"{name}'s {type1} graph")
  

  plt.grid(c="#7a7a7a")
  plt.xlabel('Timestamp')
  plt.ylabel(type1.title())
  fig.canvas.draw() #to update x labels, stuff
  axes = plt.gca()
  label_x = axes.get_xticklabels()
  ##x = axes.get_ticks()
  #label_x = [item.get_text() for item in label_x]
  if len(label_x) > 25:
    #label_x[1::2] = len(label_x[1::2]) * [""] #alternate position blank. leaves the first item
    for label in label_x[::2]: #remove slice and add if enumerate label % 3 = 0 for every 3rd label remove
      label.set_visible(False)
  #axes.set_xticklabels(label_x, rotation=45)
  plt.xticks(rotation=45)
  plt.tight_layout()
  print(f"Created for {name}")
  folder = "images"
  if light:
    folder = "lightimages"
  plt.savefig(f"{folder}/{user}-{type1}.png", dpi=100)
  plt.close()
  if not multi:
    return (x, y)


def graph_all(first=True):
  global lines
  try:
    tracklist = requests.get("https://Wasteof-api-test.quantumcodes.repl.co/track", headers={ "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).json()
  except Exception:
    with open("tracklist.json", "r") as file:
      tracklist = json.loads(file.read())

  tracklist = tuple(set(tracklist))
  for item in tracklist:
    print(item)
    ab, bc, ac = graph(item, "followers"), graph(item, "following"), graph(item, "posts") #yes I know good var names
    if ab == "no file":
      continue
    if first: #collect data only first time
      lines["followers"].append(ab)
      lines["following"].append(bc)
      lines["posts"].append(ac)

plt.style.use("default")
plt.style.use("bmh")
graph("60db0c5a956cdbbd0489eff6", "posts", light=True)
#"""
lines = {"following": [], "followers": [], "posts": []}
#graph_all()
#with open("stats/wasteof.json", "w") as file:
#  json.dump(lines, file, indent=2)

with open("stats/wasteof.json", "r") as file:
  lines = json.load(file)
graph("Wasteof", "posts", True, True)
graph("Wasteof", "followers", True, True)
graph("Wasteof", "following", True, True)
#"""
