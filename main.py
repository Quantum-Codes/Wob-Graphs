import requests, json, datetime
import matplotlib.pyplot as plt
"""
FORST CREATE SET WITH ALL XTICK, DONT PLOT ANYTHING
WHEN PLOTTING EACH LINE, CHECK FOR INDEX OF THAT DATE IN THE LIST 
PLOT ACCORDING TO THE LIST INDEX
FINALLY SET X LABELS AND TICKS WITH XTICKS() (hopefully doesn't cause probelm)
if problem, use set_xticklabels() and ignore warning forever
"""

def graph(user, type1, light, multi=False):
  if light:
    c = None #use default
  else:
    c = "yellow"
  fig = plt.figure()
  if multi:
    global lines
    all_time = set()
    for item in lines[type1]:
      datelist = [datetime.datetime.strptime(datetime.datetime.utcfromtimestamp(i).strftime("%d-%m-%y"), "%d-%m-%y") for i in item[0]]
      all_time = all_time.union(datelist)
      plt.plot(datelist, item[1], "o--", linewidth=3)
    name = "Wasteof"
    plt.title(f"wasteof.money's aggregate {type1} graph")
    all_time = list(all_time)
    all_time.sort()
    #print(all_time)
  else:
    try:
      with open(f"stats/{user}.json", "r") as file:
        data = json.load(file)
    except FileNotFoundError:
      return "no file"
    y = data[type1]
    x = []
    for item in data["timestamp"]:
      date = datetime.datetime.utcfromtimestamp(item).strftime("%d-%m-%y")
      x.append(date)
    plt.plot(range(len(data["timestamp"])), y, "o--", c = c, linewidth=3) #for even spaces
    plt.xticks(range(len(data["timestamp"])), x)
    name = data['name']
    plt.title(f"{name}'s {type1} graph")
  

  plt.grid(True, ls= "--", c="#7a7a7a")
  plt.xlabel('Timestamp')
  plt.ylabel(type1.title())
  fig.canvas.draw() #to update x labels, stuff
  axes = plt.gca()
  label_x = axes.get_xticklabels()
  if multi:
    print(len(label_x), len(all_time))
    plt.xticks(range(len(all_time)), [item.strftime("%d-%m-%y") for item in all_time])
    #print(x, len(x))
    #label_x = [item.get_text() for item in label_x]
  if len(label_x) > 25:
    #label_x[1::2] = len(label_x[1::2]) * [""] #alternate position blank. leaves the first item
    for label in label_x[::2]: #remove slice and add if enumerate label % 3 = 0 for every 3rd label remove
      label.set_visible(False)
  #axes.set_xticklabels(label_x, rotation=45)
  plt.xticks(rotation=45)
  plt.tight_layout()
  print(f"Created for {name}", "dark" if light==0 else "light")
  folder = "images"
  if light:
    folder = "lightimages"
  plt.savefig(f"{folder}/{user}-{type1}.png", dpi=100)
  plt.close()
  if not multi:
    return (data["timestamp"], y)


def graph_all(first=1):
  global lines
  try:
    tracklist = requests.get("https://Wasteof-api-test.quantumcodes.repl.co/track", headers={ "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).json()
  except Exception:
    with open("tracklist.json", "r") as file:
      tracklist = json.loads(file.read())

  tracklist = tuple(set(tracklist))
  for item in tracklist:
    print(item, "dark" if first==0 else "light")
    ab, bc, ac = graph(item, "followers", first), graph(item, "following", first), graph(item, "posts", first) #yes I know good var names. also graph light mode first 
    if ab == "no file":
      continue
    if first: #collect data only first time
      lines["followers"].append(ab)
      lines["following"].append(bc)
      lines["posts"].append(ac)

#plt.style.use("dark_background")
#"""
#graph("60db0c5a956cdbbd0489eff6", "posts", light=1)
with open("stats/wasteof.json", "r") as file:
  lines = json.load(file)
graph("Wasteof", "posts", 1, True)
#"""

lines = {"following": [], "followers": [], "posts": []}
def start_graph():
  global lines
  for i in range(1,-1,-1): #value = 1, 0 -> 1=lightmode 0=darkmode also
    plt.style.use("default") #reset style. else stylesheets merge
    if i == 1:
      plt.style.use("bmh") #light style
    else:
      plt.style.use('dark_background')
  
    graph_all(i)
    if i == 1:
      with open("stats/wasteof.json", "w") as file:
        json.dump(lines, file, indent=2)
    graph("Wasteof", "posts", i, True) #graph light mode first
    graph("Wasteof", "followers", i, True)
    graph("Wasteof", "following", i, True)

#start_graph()

