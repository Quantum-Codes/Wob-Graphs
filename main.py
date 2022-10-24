import requests, json, datetime
import matplotlib.pyplot as plt
#from matplotlib.ticker import AutoMinorLocator
plt.style.use(['dark_background'])


def graph(user, type, multi=False):
  if multi:
    global lines
  plt.figure()
  if multi:
    for item in lines[type]:
      plt.plot(item[0], item[1], "o--", linewidth=3)
    name = "Wasteof"
    plt.title(f"wasteof.money's aggregate {type} graph")
  else:
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
    plt.plot(x, y, "o--", c = "yellow", linewidth=3)
    name = data['name']
    plt.title(f"{name}'s {type} graph")

  #minor_locator = AutoMinorLocator(5)
  #plt.axes().yaxis.set_yticklabels(tick_labels.astype(int))
  plt.grid(c="#7a7a7a")
  plt.xlabel('Timestamp')
  plt.ylabel(type.title())
  #plt.ticklabel_format(style='sci')
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig(f"images/{user}-{type}.png", dpi=100)
  plt.close()
  if not multi:
    return (x, y)

#print(tracklist)

def graph_all():
  global lines
  try:
    tracklist = requests.get("https://Wasteof-api-test.quantumcodes.repl.co/track", headers={ "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).json()
  except Exception:
    with open("tracklist.json", "r") as file:
      tracklist = json.loads(file.read())

  for item in tracklist:
    print(item)
    lines["followers"].append(graph(item, "followers"))
    lines["following"].append(graph(item, "following"))
    lines["posts"].append(graph(item, "posts"))

#graph("60db0c5a956cdbbd0489eff6", "posts")
lines = {"following": [], "followers": [], "posts": []}
graph_all()
graph("Wasteof", "posts", True)
graph("Wasteof", "followers", True)
graph("Wasteof", "following", True)
