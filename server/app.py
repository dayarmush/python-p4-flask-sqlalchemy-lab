#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    response = f'''<ul>ID: {animal.id}</ul>'''
    response += f'''<ul>Name: {animal.name}</ul>'''
    response += f'''<ul>Species: {animal.species}</ul>'''
    response += f'''<ul>Zookeeper: {animal.zookeeper.name}</ul>'''
    response += f'''<ul>Enclosure: {animal.enclosure.environment}</ul>'''

    return make_response(response, 200)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper  = Zookeeper.query.filter(Zookeeper.id == id).first()
    animals = [animal for animal in zookeeper.animals]
    # <li>Zookeeper Birthday: {zookeeper.birthday}.</li>

    response = f'<ul>ID: {zookeeper.id}</ul>'
    response += f'<ul>Name: {zookeeper.name}</ul>'
    response += f'<ul>Birthday: {zookeeper.birthday}</ul>'

    if animals:
        for i in range(len(animals)):
            response += f'<ul>Animal: {animals[i].name}</ul>'

    return make_response(response, 200)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    animals = [animal for animal in enclosure.animals]

    response = f'<ul>ID: {enclosure.id}</ul>'
    response += f'<ul>Environment: {enclosure.environment}</ul>'
    response += f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'

    if animals:
        for i in range(len(animals)):
            response += f'<ul>Animal: {animals[i].name}</ul>'
            print(animals[i])

    return make_response(response, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)