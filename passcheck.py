
import requests
import hashlib
import sys

def api_data(password):
  url = 'https://api.pwnedpasswords.com/range/' + password
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
  return res

def get_leaks_count(hashes, hash_to_check):
  hashes = [line.split(':') for line in hashes.text.splitlines()]
  for h in hashes:
    if h[0] == hash_to_check:
      return h[1]
  return 0

def pwned_api_check(password):
  encod_e=password.encode('utf-8')
  sha1password = hashlib.sha1(encod_e).hexdigest().upper()
  first5_char, tail = sha1password[:5], sha1password[5:]
  response = api_data(first5_char)
  return get_leaks_count(response, tail)

def main(args):
  for password in args:
    count = pwned_api_check(password)
    if count:
      print(f'{password} was compromised {count} times. you should probably change your password!')
    else:
      print(f'{password} was NOT compromised. your password is good!')
  return 'done!'

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))