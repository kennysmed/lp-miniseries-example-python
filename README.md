# Little Printer Miniseries Example (Python)

This is an example publication, written in Python with the [Flask framework](http://flask.pocoo.org/). The same example can also be seen in:

* [PHP](https://github.com/bergcloud/lp-miniseries-example-php)
* [Ruby](https://github.com/bergcloud/lp-miniseries-example-ruby)

The working publication (using the Ruby code) can be subscribed to [on BERG Cloud Remote](http://remote.bergcloud.com/publications/335).

The publication will deliver a new image to your Little Printer every weekday for 174 days, from [the 1658 book](http://digital.lib.uh.edu/collection/p15195coll18) 'The History of Four-Footed Beasts and Serpents'.

## Configuration

By default the application is run with `DEBUG=False`. To change this create a file at `lp-miniseries-example-python/settings.cfg` containing this:

    DEBUG = True

Then set the `MINISERIES_SETTINGS` environment variable to point to this:

    $ export MINISERIES_SETTINGS=./settings.cfg

On Windows use this instead:

    >set MINISERIES_SETTINGS=.\settings.cfg

Flask can be installed using [pip](https://pypi.python.org/pypi/pip):

	$ pip install -r requirements.txt

## Run it

Run the server with:

	$ python publication.py

You can then visit these URLs:

* `/edition/?delivery_count=0&local_delivery_time=2013-10-21T19:20:30+01:00`
* `/icon.png`
* `/meta.json`
* `/sample/`

Change the value of `delivery_count` in the call to `/edition/` to see other editions.

You can also try these URLs on the live example of the publication at http://lp-miniseries-example-ruby.herokuapp.com/ .

----

BERG Cloud Developer documentation: http://remote.bergcloud.com/developers/

