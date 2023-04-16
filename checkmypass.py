import requests
import hashlib
import sys
import os

# this api uses key anonymity> you send first 5 characters and get all hashes starting the same
# uses SHA1 hashing algorithm / api will never know the full hash, so cant guess pass (in case men in mid)


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again')
    return response


def get_password_leaks_count(hashes, has_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == has_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print('\033[91m'+f'\n \"{password}\" was found {count} times... you should change it! \n'+'\033[0m')
        else:
            print('\033[93m'+f'\n \"{password}\" was NOT fount. Carry on! \n'+'\033[0m')
    # return 'done'


def logo():
    os.system('clear')
    print('''              
                                       __      __          __          
   ___ ___ ____ ____    _____  _______/ / ____/ / ___ ____/ /_____ ____
  / _ / _ `(_-<(_-| |/|/ / _ \/ __/ _  / / __/ _ / -_/ __/  '_/ -_/ __/
 / .__\_,_/___/___|__,__/\___/_/  \_,____\__/_//_\__/\__/_/\_\\__/_/   
/_/                                  /___/                                                                   
''')


if __name__ == '__main__':
    logo()
    main(sys.argv[1:])


