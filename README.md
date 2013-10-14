
## Configuration

By default the application is run with `DEBUG=False`. To change this create a file at `lp-miniseries-example-python/settings.cfg` containing this:

    DEBUG = True

Then set the `MINISERIES_SETTINGS` environment variable to point to this:

    $ export MINISERIES_SETTINGS=./settings.cfg

On Windows use this instead:

    >set MINISERIES_SETTINGS=.\settings.cfg

Install Flask using pip:

	$ pip install -r requirements.txt

## Run it

Run the server with:

	$ python publication.py


