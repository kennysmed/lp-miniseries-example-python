from flask import Flask, render_template, request, send_from_directory

# Default configuration
DEBUG = False

EDITIONS = [
    ['satyre.png', 'Satyre'],
    ['porcupine.png', 'Porcuspine or Porcupine'],
    ['lamia.png', 'Lamia'],
    ['man_ape.png', 'Man Ape'],
    ['crocodile.png', 'Arabian or Egyptian Land Crocodile'],
    ['camelopardals.png', 'Camelopardals'],
    ['boa.png', 'Boa'],
    ['unicorn.png', 'Unicorn'],
    ['aegopithecus.png', 'Aegopithecus'],
    ['badger.png', 'Badger'],
    ['hydra.png', 'Hydra'],
    ['ape.png', 'Ape'],
    ['mantichora.png', 'Mantichora'],
    ['squirrel.png', 'Squirrel'],
    ['scythian_wolf.png', 'Scythian Wolf'],
    ['beaver.png', 'Beaver'],
    ['cepus_monkey.png', 'Cepus or Martime monkey'],
    ['mole.png', 'The mole or want'],
    ['sphinx.png', 'Spinga or Sphinx'],
    ['bear_ape.png', 'Bear Ape Arctopithecus'],
    ['cat.png', 'Cat'],
    ['dragon.png', 'Winged Dragon'],
    ['prasyan_ape.png', 'Prasyan Ape'],
    ['su.png', 'A wilde beaste in the New Found World called SU'],
    ['bear.png', 'Bear'],
    ['sagoin.png', 'Sagoin, called Galeopithecus'],
    ['lion.png', 'Lion'],
    ['another_monster.png', 'Another Monster'],
    ['adder.png', 'Adder'],
    ['african_bugil.png', 'African Bugil'],
    ['allocamelus.png', 'Allocamelus'],
    ['alpine_mouse.png', 'Alpine Mouse'],
]

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
app.config.from_envvar('MINISERIES_SETTINGS', silent=True)


@app.route('/meta.json')
@app.route('/icon.png')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/img/<image_name>')
def image(image_name):
    return send_from_directory(app.static_folder+'/img', image_name)


@app.route('/sample/')
def sample():
    delivery_count = 0
    return render_template('edition.html',
                        delivery_count=delivery_count,
                        image=app.config['EDITIONS'][delivery_count][0],
                        description=app.config['EDITIONS'][delivery_count][1]
                    )


@app.route('/edition/')
def edition():

    delivery_count = int(request.args.get('delivery_count', 0))

    return render_template('edition.html',
                        delivery_count=delivery_count,
                        image=app.config['EDITIONS'][delivery_count][0],
                        description=app.config['EDITIONS'][delivery_count][1]
                    )


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()

