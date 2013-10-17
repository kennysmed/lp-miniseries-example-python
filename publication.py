from datetime import datetime
from flask import Flask, make_response, render_template, Response, request, send_from_directory
import hashlib
import json


# Default configuration
DEBUG = False

# EDITIONS will be an array of arrays.
# Each sub-array be like ["ape.png", "Ape"]
with open('editions.json') as editions_data:
    EDITIONS = json.load(editions_data)


app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
# If there's a MINISERIES_SETTINGS environment variable, which should be a
# config filename, use those settings:
app.config.from_envvar('MINISERIES_SETTINGS', silent=True)


@app.route('/')
def root():
    return make_response('A Little Printer publication.')

@app.route('/meta.json')
@app.route('/icon.png')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/img/<image_name>')
def image(image_name):
    return send_from_directory(app.static_folder+'/img', image_name)


# Called to generate the sample shown on BERG Cloud Remote.
@app.route('/sample/')
def sample():
    # We can choose which edition we want as the sample:
    edition_number = 0
    response = make_response(render_template(
                        'edition.html',
                        edition_number=edition_number,
                        image_name=app.config['EDITIONS'][edition_number][0],
                        description=app.config['EDITIONS'][edition_number][1]
                    ))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['ETag'] = '"%s"' % (
        hashlib.md5('sample'+datetime.utcnow().strftime('%d%m%Y')).hexdigest() )
    return response


# Called by BERG Cloud to generate publication output to print.
@app.route('/edition/')
def edition():
    edition_number = int(request.args.get('delivery_count', 0))

    if 'local_delivery_time' in request.args:
        # local_delivery_time is like '2013-10-16T23:20:30-08:00'.
        # We strip off the timezone, as we only need to know the day.
        date = datetime.strptime(request.args['local_delivery_time'][:-6],
                                                        '%Y-%m-%dT%H:%M:%S')
    else:
        # Default to now.
        date = datetime.utcnow()

    if (edition_number + 1) > len(app.config['EDITIONS']):
        # The publication has finished, so unsubscribe this subscriber.
        return Response(response=None, status=410)

    elif date.isoweekday() in (6, 7):
        # No content is delivered this day.
        return Response(response=None, status=204)

    else:
        # It's all good, so display the publication.
        response = make_response(render_template(
                        'edition.html',
                        edition_number=edition_number,
                        image_name=app.config['EDITIONS'][edition_number][0],
                        description=app.config['EDITIONS'][edition_number][1]
                    ))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['ETag'] = '"%s"' % (
                hashlib.md5(
                    str(edition_number) + datetime.utcnow().strftime('%d%m%Y')
                ).hexdigest()
            )
        return response


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()

