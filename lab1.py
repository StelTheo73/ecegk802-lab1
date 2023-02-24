import requests
import json
import re
from datetime import datetime

def more(text):
    count = 0
    for line in text.split('\n'):
        print(line)
        count += 1
        if count % 30 == 0:
            reply = input('Show more (y/n)? ')
            if reply == 'n':
                break

def get_server_info(response):
  try:
    server = response.headers["Server"]
  except KeyError:
    server = "Unknown server"
  print("Server: " + server, end = "\n\n")

def get_cookies_info(response):
  cookies = response.cookies
  
  if len(cookies) == 0:
    print("No cookies found.")
    return
  
  print("Cookies:")
  for cookie in cookies:
    name = cookie.name
    try:
      expiration = str(datetime.fromtimestamp(cookie.expires))
    except TypeError:
      expiration = "Unknown"
    print_cookie_info(name, expiration)

def print_cookie_info(name, expiration):
  cookie_dict = {
    "Name": name,
    "Expiration" : expiration
  }
  print (json.dumps(cookie_dict, indent=2))

def make_request(url):
  try:
    with requests.get(url) as resp:
      response = resp
  except Exception:
    print("Could not establish connection!")
    response = None
  return response

def validate_user_input(url):
  if url == "0":
    print("Goodbye!")
    exit(0)
    
  url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
  if re.match(url_pattern, url):
    return True
  return False

def get_user_input():
  return input("Give a url (0 to exit): ")
  
def main():
  while True:
    url = get_user_input()
    if not(validate_user_input(url)):
      print("Not a valid url!")
    else:
      break

  response = make_request(url)
  if(response):
    #more(response.text)
    print(json.dumps(dict(response.headers), indent=2), end = "\n\n")
    get_server_info(response)
    get_cookies_info(response)
  
  print("\n-----------------------------------\n")
  return
  
if __name__ == "__main__":
  while(True):
    main()
