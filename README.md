# Stories of Solidarity

A social media tool that helps workers in low wage, precarious jobs to build new forms of solidarity and mutual aid.

## Database

Provides structured data via a REST API, used by [stories-of-solidarity-api](https://github.com/spacedogXYZ/stories-of-solidarity-api) to display them visually. Also connects with a phone number to add new stories by SMS.


### Technologies

* [Django](https://www.djangoproject.com) and [REST Framework](https://www.djangoproject.com)
* [Twilio](http://django-twilio.readthedocs.io) via [django-twilio](http://django-twilio.readthedocs.io)
* [WP-Admin](https://github.com/barszczmm/django-wpadmin)

### Geolocation

Uses [Mapzen Search](https://mapzen.com/documentation/search/) to geolocate zipcodes to lat/lon, or reverse geocode browser locations to zipcode. Requires a free API key.

### Development

Run it locally in a [virtualenvironment](https://virtualenv.pypa.io/en/stable/) with 

```bash
$ source env/bin/activate
$ pip install -r requirements.txt
$ python manager.py runserver
```

to connect with a live phone number from Twilio, you need a web-routable domain. You can get this for free with [ngrok](https://ngrok.com)

`$ ngrok http 5000`

and place the Forwarding url https://SOMETHING.ngrok.io/sms/post/ as the Request POST URL of your Twilio phone number.

When running locally you may want to turn off the SSLify middleware, unless you have a 

### Deployment

Send to Heroku with 

```bash
$ git push heroku master
```

Requires a Postgres database and memcache add-on. Also uses Sendgrid for sending user registration emails.