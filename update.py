import requests, time, json, os
from copy import deepcopy
import mysql.connector

db = mysql.connector.connect(
  host = os.environ["db_host"],
  user = os.environ["db_user"],
  password = os.environ["db_pass"],
  database = "testdb"
)
sql = db.cursor()

headers = {"User-Agent":"@wasteof_bot by @Ankit_Anmol | Contact on wasteof-@ankit_anmol on github-@Quantum-Codes on discord(you have)"}
history_struct = {"followers":[], "following":[], "posts":[], "timestamp":[]}

def get_list():
  try:
    x = requests.get("https://Wasteof-api-test.quantumcodes.repl.co/track", headers={ "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    return x.json()
  except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
    print("Bruhhhhhhhh connection/SSL error")
    print(e)
  except Exception as e:
    print(e)
  
tracklist = 0
for i in range(5):
  try:
    tracklist = get_list()
  except Exception as e:
    print(i, e)
    time.sleep(60) #wait for repl to wake up
    
    
if type(tracklist) is list:
  print("Live data!!")
  with open("tracklist.json", "w") as file:
    file.write(json.dumps(tracklist, indent=2))
else:
  with open("tracklist.json", "r") as file:
    tracklist = json.load(file)
    print("old data :(")
  
def stats(id):
  post = None
  user = requests.get(f"https://api.wasteof.money/username-from-id/{id}",  headers=headers).json()
  if not user.get("username", None):
    print("!!ERROR ID: ", id)
    print(user)
  else:
    user = user["username"]
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
    if not x:
      continue
    y = prev_stats(item)
    print(x,"being updated")
    y["followers"].append(x["followers"])
    y["following"].append(x["following"])
    y["posts"].append(x["posts"])
    y["timestamp"].append(int(time.time()))
    y["name"] = x["user"]
    with open(f"stats/{item}.json", "w") as file:
      file.write(json.dumps(y, indent=2))

track()
