import requests, time

def ping():
  try:
    requests.get("https://Wasteof-api-test.quantumcodes.repl.co", headers={ "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    print("done")
  except requests.exceptions.ConnectionError:
    print("Bruhhhhhhhh connection error")
  except Exception as e:
    print(e)

print("started")
ping()
time.sleep(10)
ping()

print("Pinged!")
