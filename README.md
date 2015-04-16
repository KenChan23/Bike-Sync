Bike-Sync
======
The following Flask application serves as the underlying infrastructure for Bike-Sync, a recommendation system for suggesting music to bikers to encourage them to ride their bikes more actively. An API has been built off the historical data stored within a MongoDB database.

```
python runserver.py
```

File Structure (will have more details soon)
======
- data/geocode.py: Utilizes the Google Directions API to grab routing data for a sample size of one hundred trips within a given month-year collection.
- data/fitbit.py: Automates the scraping of the bpm JSON data from the raw source code of a user's dashboard. 
- mongoDB database access
	use citibike --> switich to db that contains the collection citibike
	db --> show the collection data, in this case, citibike
	show collections --> show all the documents that consist of the collections
	db.citibike.findOne() --> show the first record of the collections
