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

headers = {"User-Agent":"@wasteof_bot by @Quantum-Codes | Contact on wasteof- @quantum-codes, on github- @Quantum-Codes, on discord(you have)"}
history_struct = {"followers":[], "following":[], "posts":[], "timestamp":[]}
  
def get_list():
  sql.execute("SELECT userid FROM wasteof WHERE track = 1;")
  tracklist = []
  for item in sql:
    tracklist.append(item[0])
  return tracklist

try:
  tracklist = get_list()
  with open("tracklist.json", "w") as file:
    file.write(json.dumps(tracklist, indent=2))
except:
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
