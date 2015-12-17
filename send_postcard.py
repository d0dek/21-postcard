#! /usr/local/bin/python3

import os, sys
import lob
from time import sleep
from flask import Flask

# Setup the Lob API (lob.com)
API_KEY = "YOUR_LOB_API_KEY"
lob.api_key = API_KEY

app = Flask(__name__)


@app.route('/')
def home():
    return open('index.html', 'r').read()


@app.route('/send/<name>/<address>/<city>/<state>/<zipcode>')
#@payment.required(POSTCARD_PRICE)
def send(name, address, city, state, zipcode):
    print("your postcard will be shipped to:\n")
    print(name)
    print(address)
    print(city, state, zipcode)
    # send_postcard(name, address, city, state, zipcode)
    return "sent!"


def send_postcard(name, address, city, state, zipcode, country='US'):
    postcard = lob.Postcard.create(
      to_address = {
        'name': name,
        'address_line1': address,
        'address_city': city,
        'address_state': state,
        'address_zip': zipcode,
        'address_country': country
      },
      from_address = {
        'name': 'Olaf Carlson-Wee',
        'address_line1': '123 Bitcoin Lane',
        'address_city': 'San Francisco',
        'address_state': 'CA',
        'address_zip': '94111',
        'address_country': 'US'
      },
      front = """
        <html style="padding: 1in; font-size: 50;">
        <img src="https://raw.githubusercontent.com/d0dek/21-postcard/master/images/postcard_front.png"/>
        Front HTML for {{name}}
        </html>
        """,
      back = """
        <html style="padding: 1in; font-size: 20;">
        <img src="https://raw.githubusercontent.com/d0dek/21-postcard/master/images/postcard_back.png"/>
        Back HTML for {{name}}
        </html>'
        """,
      data = {
        'name': name
      }
    )
    print(postcard)
    sleep(7)
    os.system('open %s' % postcard['thumbnails'][0]['large'])
    os.system('open %s' % postcard['thumbnails'][1]['large'])

def get_args():
    if len(sys.argv) > 1 and sys.argv[1]=='test':
        name = "Olaf Carlson-Wee"
        address = "123 Bitcoin Lane"
        city = "San Francisco"
        state = "CA"
        zipcode = "94111"
    else:
        name = input("please enter the recipients name: ")
        address = input("... and their street address: ")
        city = input("... and their city: ")
        state = input("... and their state: ")
        zipcode = input("... and their zip code: ")
    return (name, address, city, state, zipcode)

def print_args(name, address, city, state, zipcode):
    print("your postcard will be shipped to:\n")
    print(name)
    print(address)
    print(city, state, zipcode)

if __name__ == '__main__':
    print("starting webserver")
    # app.run(host='0.0.0.0', port=SERVER_PORT)
    
    name, address, city, state, zipcode = get_args()

    # now show all together
    print_args(name, address, city, state, zipcode)

    do_send = input("do you really want to send this? ")
    if do_send.lower().find('y') == 0:
        send_postcard(name, address, city, state, zipcode)
    else:
        print("okay, we won't send")

