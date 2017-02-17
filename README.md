# Pyphon
[![Build Status](https://travis-ci.org/pyphonic/Pyphon.svg?branch=development)](https://travis-ci.org/pyphonic/Pyphon)
[![Coverage Status](https://coveralls.io/repos/github/pyphonic/Pyphon/badge.svg?branch=development)](https://coveralls.io/github/pyphonic/Pyphon?branch=development)



The Pyphon [pronounced py-phone] is a smartphone built on a Raspberry Pi and the Django Framework.


# Website
[Pyphon](http://ec2-52-39-22-59.us-west-2.compute.amazonaws.com)

# Major Components
- Login
- Touch screen
- Voice
- Text messaging
- Address Book


# Tools used
Django, Django Rest framework, Postgres, JQuery, Twilio, Ngrok, AWS, Unittest, Travis CI, Coveralls

# Planned features
1) Email

2) Camera

3) Spotify

4) GPS navigation

# Current URL routes:
- /
- /login
- /logout
- /admin
- /api/texts/
- /api/calls/
- /api/contacts/list/
- /api/contact/retrieve/[number]
- /calls/dial/
- /calls/token/
- /calls/call/
- /calls/recent/
- /contacts/
- /contacts/[pk]
- /contacts/new/
- /contacts/[pk]/edit/
- /texts/
- /texts/new/
- /texts/hook/
- /texts/contact/[pk]/


# License
Apache2 License


# Build Your Own PyPhon!

## First, gather your materials. 

- Raspberry Pi3 (and case, if desired). Make sure it has Raspbian Jessie installed.

- PiTFT Touch Screen (Make sure it is plugged in to your pi.)

- Mini USB Microphone


## Next, get the app set up on your local device.

- Clone it on your local machine.

```
git clone https://github.com/pyphonic/Pyphon.git
```

- Set up a virtual environment on your local device, and create a local database.

- Download all dependencies.

```
pip install -r requirements.pip
```

- Set up ngrok so you can run the OS on your browser.

[Download ngrok](https://ngrok.com/download)

In a separate terminal, unzip ngrok:

```
unzip /path/to/ngrok.zip
```

Then run it on that terminal.

```
ngrok http 8000
```

Grab the second ngrok forwarding address, and save it. Twilio needs a public url in order to make successful phone calls and texts, and this is the address that you will use. Be careful here; if you exit out of the ngrok server, or close the terminal, your ngrok forwarding address will change, and you will need to change more configurations.

- Set up your account on Twilio. Get a paid phone number.

- Set up your Twilio configuration to use that ngrok instance you captured. 

On the phone numbers page in your console, make sure you're configured with Webhooks/TwiML.

Set the 'A Call Comes In' setting to use Webhooks, and forward to your base ngrok forwarding address. Use POST requests.

Set the 'Primary Handler Fails' setting to use Webhooks, and forward to your ngrok forwarding address with the following url route at the end: 

```
/calls/call
```
Make sure this setting uses GET requests.

- Set up your TwiML application on the Twilio TwiML app page. Name your TwIML app, and go into the detail view. Configure the Voice request url to your base ngrok forwarding address + /calls/call, using the POST request setting. Open the optional settings, and configure the "Fallback URL" to the same url, using the GET request setting.

- Set up the following environment variables, using the variables from your Twilio account and/or your local environment.

```
  * SECRET_KEY
  * EMAIL_PASSWORD
  * DB_USERNAME
  * DB_PASSWORD
  * DB_NAME
  * ALLOWED_HOSTS
  * DEBUG
  * TWIML_APPLICATION_SID
  * ACCOUNT_SID
  * AUTH_TOKEN
  * TWILIO_NUMBER
  * TEST_ACCOUNT_SID
  * TEST_AUTH_TOKEN
```

- In a new terminal (*not* the one running ngrok), run your localhost on port 8000. Check that the OS works as desired. You must keep both localhost and ngrok running in order to use the phone's functionality, unless you wish to deploy.

## Now, get the OS loaded on to the PyPhon

- On the Raspberry Pi, go to settings, and allow ssh. Make sure you know your pi's password. Change it if desired.


- Find out what your pi's ip address is.


- On a separate computer, in the command line, type:

```
ssh pi@<ip address>
```

You will then be prompted for your password.


- Next, run this prompt on your pi.

```
sudo nano ~/.config/autostart/openChromium.desktop
```


- That will open up a nano window. Within that window, type:
```
[Desktop Entry]
Type=Application
Exec=/usr/bin/chromium-browser --noerrdialogs --disable-session-crashed-bubble --disable-infobars --kiosk http://www.yourNGROKsite.com
Hidden=false
X-GNOME-Autostart-enabled=true
Name[en_US]=AutoChromium
Name=AutoChromium
Comment=Start Chromium when GNOME starts
```

Make sure that you replace "http://www.yourNGROKsite.com" with your actual ngrok forwarding address.

Save this file. This sets up your pi to run our start up script on boot, which enables kiosk mode.


- Now for the screen. To set up your screen's driver, type the following in to your pi terminal:

```
cd

curl -O https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/pitft-fbcp.sh

sudo bash pitft-fbcp.sh
```

This will take you to a screen, from which you can select from a few options. 

Select "configure options manually". 

Next, choose your screen size. We used 3.5 inch, but make sure that your screen size corresponds to the size of the screen you chose.

Select 90 degree rotation for your desktop, to enable screen orientation in portrait and landscape mode.

Then, select 90 degrees rotation counter-clockwise for your touchscreen orientation.


- Reboot your pi:

```
sudo reboot
```

This will restart your phone, and load the OS on boot.

## Start using your phone!



# Team
[Ford Fowler](https://github.com/fordf)

[Avery Pratt](https://github.com/averypratt)

[Maelle Vance](https://github.com/ellezv)

[Julien Wilson](https://github.com/julienawilson)

[Rachael Wisecarver](https://github.com/rwisecar)

# Special Thanks
[Nicholas Hunt-Walker](https://github.com/nhuntwalker)

[David Smith](https://github.com/bl41r)

[Ben Garnaat](https://github.com/bgarnaat)

[Selena Flannery](https://github.com/seleniumK)

[Will Weatherford](https://github.com/WillWeatherford)

[Duncan Marsh](https://github.com/slugbyte)

[Judy Vue](https://github.com/JudyVue)

[Go Django tutorial on Ngrok](https://godjango.com/55-webhooks-django-and-ngrok/)

[Raspberry Pi kiosk mode tutorial by Dan Purdy](https://www.danpurdy.co.uk/web-development/raspberry-pi-kiosk-screen-tutorial/)

[Twilio tutorials](https://www.twilio.com/docs/tutorials?filter-language=node.js&filter-platform=server)

[On screen keyboard by Sam Deering](https://github.com/sdeering/onscreenkeyboard)

**Daily Ice Cream team meetings!**
