"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap #importamos APIExcepcion para poder hacer las validaciones
from admin import setup_admin
from models import db, User, Characters, Planets #importamos la tabla a quien queremos hacer la consulta
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints/# generar un mapa del sitio con todos sus puntos finales(endpoints)
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#COLOCAMOS NUESTROS ENDPOINTS A PARTIR DE

#USER PLURALMENTE
@app.route('/user', methods=['GET'])
def handle_userAll():

    users = User.query.all() #almacenamos todos los usuarios
    data = [user.serialize() for user in users ] # para cada usuario dentro de los usuarios me los serialice

    return jsonify(data), 200 #aqui lo convertimos en string con jsonify

#USER SINGLE
@app.route('/user/<int:id>', methods=['GET'])
def get_userSingle(id):
    user = User.query.get(id) #se obtiene el usuario de la base de datos utilizando User.query.get(id)
    
    if user is None: #Si user es None, se lanza la excepción APIException con el mensaje "This user does not exist" y el codigo de estado 400.
        raise APIException('This user does not exist', status_code=400)
    
    return jsonify(user.serialize()), 200

#CREATE NEW USER (POST)
@app.route('/user', methods = ['POST']) #ruta para aceptar solicitudes y crear nuevo usuario
def create_user(): #def create_user(): Esta función llamada create_user se ejecutará cuando se acceda a la ruta /user mediante una solicitud POST.

#se guarda el contenido en la variable "body"
    body = request.json #request.json contiene los datos enviados con la solicitud POST.

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body or not body ['name']:  #se verifica que esta agregada la propiedad name y que no se ingrese el campo vacio
        raise APIException("You need to specify the name, can't be empty" , status_code=400)
    if 'email' not in body or not body['email']:
        raise APIException("You need to specify the email, can't be empty", status_code=400)

    user = User(email=body["email"], name=body["name"]) #se crea un objeto de la clase User con los valores del correo electrónico y el estado activo obtenidos del objeto body.
    db.session.add(user) #esto indica que se debe crear un nuevo registro en la base de datos con los valores proporcionados.
    db.session.commit() #Realiza una confirmación en la sesión de la base de datos, lo que efectivamente guarda los cambios realizados en la base de datos.

    response_body = {
        "msg": "El usuario ha sido creado",
    } # Creamos un diccionario llamado response_body que contiene un mensaje indicando que el usuario ha sido creado.

    return jsonify(response_body), 200 #La función jsonify se utiliza para convertir el diccionario en una respuesta JSON valida

#DELETE USER (ID)
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_userSingle(id): #esta funcion recibe el parámetro id, que se obtiene de la URL.
        #Se verifica si user existe. Si no existe, se devuelve una respuesta con un mensaje de "User not found" y un codigo de estado 404.
        #Si el usuario existe, se elimina de la base de datos usando db.session.delete(user). Luego, se confirma la transacción con db.session.commit().
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# ALL THE CHARACTERS
@app.route('/characters', methods=['GET'])
def handle_charactersAll():

    charactersAll = Characters.query.all() #almacenamos todos los usuarios
    data = [character.serialize() for character in charactersAll] # para cada character dentro de los characters y nos lo serialice
    return jsonify(data), 200 #aqui lo convertimos en string con jsonify

#CHARACTERS SINGLE
@app.route('/characters/<int:id>', methods = ['GET'])
def get_characterSingle(id):
    characters = Characters.query.get(id)

    if characters is None: #Si characters es None(no existe el id ingresado), se lanza la excepción APIException con el mensaje "This user does not exist" y el codigo de estado 400.
        raise APIException('This Character does not exist', status_code=400)
    
    print(characters.serialize())
    return jsonify(characters.serialize()), 200

#CREATE NEW CHARACTER
@app.route('/characters', methods = ['POST']) #ruta para aceptar solicitudes y crear nuevo usuario
def create_newCharacter(): #def create_newCharacte(): Esta función se ejecutará cuando se acceda a la ruta /user mediante una solicitud POST.
 #se guarda el contenido en la variable "body"
    body = request.json

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body or not body['name']:
        raise APIException("You need to specify the name, can't be empty", status_code=400)
    if 'gender' not in body or not body['gender']:
        raise APIException("You need to specify the gender,can't be empty" , status_code=400)
    if 'eye_color' not in body or not body['eye_color']:
        raise APIException("You need to specify the eye_color, can't be empty" , status_code=400)

    print(body)
    characters = Characters(name = body["name"], gender=body["gender"], eye_color=body["eye_color"]) #se crea un objeto de la clase User con los valores del correo electrónico y el estado activo obtenidos del objeto body.
    db.session.add(characters) #esto indica que se debe crear un nuevo registro en la base de datos con los valores proporcionados.
    db.session.commit() #Realiza una confirmación en la sesión de la base de datos, lo que efectivamente guarda los cambios realizados en la base de datos.

    response_body = {
         "msg": "a new character has been added",
     } # Creamos un diccionario llamado response_body que contiene un mensaje indicando que el usuario ha sido creado.

    return jsonify(response_body), 200 #La función jsonify se utiliza para convertir el diccionario en una respuesta JSON valida

#DELETE CHARACTER(ID)
@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_charactersSingle(id): #esta funcion recibe el parámetro id, que se obtiene de la URL.

    characters = Characters.query.get(id)
    if characters:
        db.session.delete(characters)
        db.session.commit()
        return jsonify({'message': 'character deleted successfully'}), 200
    else:
        return jsonify({'message': 'Character not found'}), 404

# ALL THE PLANETS
@app.route('/planets', methods=["GET"])
def handle_planetsAll():
    planetsAll= Planets.query.all()
    data = [planet.serialize() for planet in planetsAll] # para cada planet dentro de los planetaS y nos lo serialice

    return jsonify(data), 200

#PLANET SINGLE(ID)
@app.route('/planets/<int:id>', methods=["GET"])
def get_planetSingle(id):

    planet = Planets.query.get(id)

    if planet is None: #Si el planet es None(no existe el id ingresado), se lanza la excepción APIException con el mensaje "This user does not exist" y el codigo de estado 400.
        raise APIException('This Planet does not exist', status_code=400)
    
    print(planet.serialize())
    return (jsonify.serialize()), 200

#CREATE NEW PLANET
@app.route('/planets', methods=["POST"])
def create_newPlanet():

    body = request.json

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'name' not in body or not body['name'].strip():
        raise APIException("You need to specify the name, can't be empty", status_code=400)
    if 'terrain' not in body or not body['terrain']:
        raise APIException("You need to specify the terrain can't be empty", status_code=400)
    if 'population' not in body or not body['population']:
        raise APIException("You need to specify the population, can't be empty", status_code=400)
    
    print(body)
    planets = Planets(name=body["name"], terrain=body["terrain"], population=body["population"])
    db.session.add(planets) #esto indica que se debe crear un nuevo registro en la base de datos con los valores proporcionados.
    db.session.commit()

    response_body = {
         "msg": "a new planet has been added",
     } # Creamos un diccionario llamado response_body que contiene un mensaje indicando que el nuevo planeta ha sido creado.

    return jsonify(response_body), 200

#DELETE PLANET (ID)
@app.route('/planets/<int:id>', methods = ["DELETE"])
def delete_planet(id):
    planet = Planets.query.get(id)
    if planet:
        db.session.delete(planet) #Esta línea elimina el objeto planet de la sesión de la base de datos.
        db.session.commit() # se guarda los cambios realizados en la base de datos. La eliminación del planeta se confirma al llamar a este método.
        return jsonify({'message': 'planet deleted succesfully'})
    else:
        return jsonify({'message':'Planet not found'}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)