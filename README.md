# Mojio Publishers Service Areas

This is a sample project defining publishers and the service areas associated with them. A publisher
can have multiple service area associated with them. A service area is basicaally a geoJSON polygon 
defined for the given publisher.


This is a test only assignment. So many basic things have been omitted to save time. We are currently using
sqlite as db. However settings for mySQL are configured and can be used anytime too.

Instead of using elastic search as the backend , we have a simple configuration to use haystack plain backend.
Though settings can be modified anytime too to use elastic search node too.

The application is defined to be run behind nginx where it will speak to gunicorn app server. The service will
run in background as systemctl. Extensive monitoring of service to report outage is currently not implemented
here.

The basic test cases of modules are written. Extensive test cases have been omitted currently.

To use the application:
Go to: ```mojio.assignment.io``` and start hitting the apis.

Currently very basic apis are written and no authentication exists of them. (This is to be a serious miss. This
will be implemented later.)

Extensive documentation for the apis can be found in the ```/docs```. The documentation can also be 
used to test the apis written.

## Local Setup

- Go to the project directory and create virtualenv using the command ```virtualenv --python=`which python2` mojio_env```
- Install the project requirements using the command ```pip install -r requiremnts.txt```
- Run the migrations using the command ```python manage.py migrate```
- Start the server using the command ```python manage.py runserver```

