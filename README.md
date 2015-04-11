CitiBike
======

The following Flask application serves as the underlying infrastructure for MusicBike, a recommendation system for suggesting music to bikers to encourage them to ride their bikes more actively. An API has been built off the historical data stored within a MongoDB database.

```
python runserver.py
```

Notes:

- geocode.py: Utilizes the Google Directions API to grab routing data for a sample size of one hundred trips within a given month-year collection.
- fitbit.py: Automates the scraping of the bpm JSON data from the raw source code of a user's dashboard. 

