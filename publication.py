from datetime import datetime
from flask import Flask, make_response, render_template, Response, request, send_from_directory
import hashlib

# Default configuration
DEBUG = False

# Data for each edition: image filename, description.
EDITIONS = [
    ['adder.png', 'Adder'],
    ['aegopithecus.png', 'Aegopithecus'],
    ['african_bugil.png', 'African Bugil'],
    ['allocamelus.png', 'Allocamelus'],
    ['alpine_mouse.png', 'Alpine Mouse'],
    ['another_monster.png', 'Another Monster'],
    ['antalope.png', 'Antalope'],
    ['ape.png', 'Ape'],
    ['ape_calitrich.png', 'Ape Calitrich'],
    ['arabian_crocodile.png', 'Arabian or Egyptian Land Crocodile'],
    ['arabian_sheep_broad.png', 'Arabian Sheep with a broad tail'],
    ['arabian_sheep_long.png', 'Arabian Sheep with a long tail'],
    ['aspes.png', 'Aspes'],
    ['asse.png', 'Asse'],
    ['badger.png', 'Badger'],
    ['bear.png', 'Bear'],
    ['bear_ape.png', 'Bear Ape Arctopithecus'],
    ['beaver.png', 'Beaver'],
    ['boa.png', 'Boa'],
    ['camelopardals.png', 'Camelopardals'],
    ['cat.png', 'Cat'],
    ['cepus_monkey.png', 'Cepus or Martime monkey'],
    ['hydra.png', 'Hydra'],
    ['lamia.png', 'Lamia'],
    ['lion.png', 'Lion'],
    ['man_ape.png', 'Man Ape'],
    ['mantichora.png', 'Mantichora'],
    ['mole.png', 'The mole or want'],
    ['porcupine.png', 'Porcuspine or Porcupine'],
    ['prasyan_ape.png', 'Prasyan Ape'],
    ['sagoin.png', 'Sagoin, called Galeopithecus'],
    ['satyre.png', 'Satyre'],
    ['scythian_wolf.png', 'Scythian Wolf'],
    ['sphinx.png', 'Spinga or Sphinx'],
    ['squirrel.png', 'Squirrel'],
    ['su.png', 'A wilde beaste in the New Found World called SU'],
    ['unicorn.png', 'Unicorn'],
    ['winged_dragon.png', 'Winged Dragon'],
]

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
# If there's a MINISERIES_SETTINGS environment variable, which should be a
# config filename, use those settings:
app.config.from_envvar('MINISERIES_SETTINGS', silent=True)


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
    delivery_count = 0
    response = make_response(render_template(
                        'edition.html',
                        delivery_count=delivery_count,
                        image_name=app.config['EDITIONS'][delivery_count][0],
                        description=app.config['EDITIONS'][delivery_count][1]
                    ))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['ETag'] = '"%s"' % (
        hashlib.md5('sample'+datetime.today().strftime('%d%m%Y')).hexdigest() )
    return response


# Called by BERG Cloud to generate publication output to print.
@app.route('/edition/')
def edition():
    delivery_count = int(request.args.get('delivery_count', 0))

    if 'local_delivery_time' in request.args:
        # local_delivery_time is like '2013-10-16T23:20:30-08:00'.
        # We strip off the timezone, as we only need to know what day this
        # date is on.
        date = datetime.strptime(request.args['local_delivery_time'][:-6],
                                                        '%Y-%m-%dT%H:%M:%S')
    else:
        # Default to now.
        date = datetime.today()

    if (delivery_count + 1) > len(app.config['EDITIONS']):
        # The publication has finished, so unsubscribe this subscriber.
        return Response(response=None, status=410)

    elif date.isoweekday() != 3:
        # No content is delivered this day (Monday=1, Tuesday=2, etc).
        return Response(response=None, status=204)

    else:
        # It's all good, so display the publication.
        response = make_response(render_template(
                        'edition.html',
                        delivery_count=delivery_count,
                        image_name=app.config['EDITIONS'][delivery_count][0],
                        description=app.config['EDITIONS'][delivery_count][1]
                    ))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['ETag'] = '"%s"' % (
                hashlib.md5(
                    str(delivery_count) + datetime.today().strftime('%d%m%Y')
                ).hexdigest()
            )
        return response


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()

