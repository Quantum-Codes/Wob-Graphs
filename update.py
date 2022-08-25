import requests, time, json
from copy import deepcopy

headers = {"User-Agent":"@wasteof_bot by @Ankit_Anmol | Contact on wasteof-@ankit_anmol on github-@Quantum-Codes on discord(you have)"}
history_struct = {"followers":[], "following":[], "posts":[], "timestamp":[]}
tracklist = requests.get("https://Wasteof-api-test.quantumcodes.repl.co/track").json()

def stats(id):
  user = requests.get(f"https://api.wasteof.money/username-from-id/{id}",  headers=headers).json()["username"]
  post = requests.get(f"https://api.wasteof.money/users/{user}",  headers=headers).json()["stats"]
  post["user"] = user
  return post
  
def prev_stats(user):
  try:
    with open(f"stats/{user}.json", "r") as file:
      return json.loads(file.read())
  except FileNotFoundError:
    return deepcopy(history_struct) #to not change format. deep copy also created new list in the values of dict

def track():
  for item in tracklist:
    x = stats(item)
    y = prev_stats(x["user"])
    print(history_struct)
    y["followers"].append(x["followers"])
    y["following"].append(x["following"])
    y["posts"].append(x["posts"])
    y["timestamp"].append(int(time.time()))
    with open("stats/"+x["user"]+".json", "w") as file:
      file.write(json.dumps(y, indent=2))

track()
