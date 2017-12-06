# Stories of Solidarity

A social media tool that helps workers in low wage, precarious jobs to build new forms of solidarity and mutual aid.

## Database

Provides structured data via a REST API, used by the [Stories of Solidarity website](https://github.com/storiesofsolidarity/website-frontend) to display visually. Also connects with a phone number to add new stories by SMS.

## Data Structure

The building blocks of this project are Stories. Stories have an author, a location, textual content, an optional image, and metadata about when it was posted.

Each story has an Author, which is one-to-one mapped to the Django User model via an abstract base class. Authors can be grouped by Employer or Occupation. Authors can also be marked as Anonymous for privacy, which redacts their name in the API although not in the database. Users who wish to maintain full anonymity may use a pseudonym and should ensure that their content does not include identifying information.

Text messages are parsed via the `sms` application, and users may send longer stories through multiple messages. They can end by sending their zipcode, which is matched to an existing Location object, or creating a new one.

### Geolocation

[Mapzen Search](https://mapzen.com/documentation/search/) is used to geolocate zipcodes to lat/lon, or to reverse geocode browser locations to zipcode. This requires a free API key, and is rate-limited.

Stories are available at the state, county, and zipcode level, based on the geographic views defined in the frontend. These return previews of a few recent stories in that location, to avoid multiple roundtrips.

### Technologies

* [Django](https://www.djangoproject.com) and [REST Framework](https://www.djangoproject.com)
* [Twilio](http://django-twilio.readthedocs.io) via [django-twilio](http://django-twilio.readthedocs.io)
* [WP-Admin](https://github.com/barszczmm/django-wpadmin)

### Development

Run it locally in a [virtualenvironment](https://virtualenv.pypa.io/en/stable/) with 

```bash
$ source env/bin/activate
$ pip install -r requirements.txt
$ export DJANGO_SETTINGS_MODULE=sos.settings_local
$ python manager.py runserver
```

To connect with a live phone number from Twilio, you need a web-routable domain connected to your localhost. You can get this for free with [ngrok](https://ngrok.com).

`$ ngrok http 8000`

and place the Forwarding url https://SOMETHING.ngrok.io/sms/post/ as the Request POST URL of your Twilio phone number.

When running locally you may want to turn off the SSLify middleware with `SSLIFY_DISABLE = True` in settings_local.py

### Deployment

Send to Heroku with 

```bash
$ heroku config:set DJANGO_SETTINGS_MODULE=sos.settings_production
$ git push heroku master
```

Requires a Postgres database and memcache add-on. Also uses Sendgrid for sending user registration emails.
