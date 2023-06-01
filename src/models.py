from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'  #__tablename__ Especifica el nombre de la tabla en la base de datos para cada clase.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    favorites_planets = db.relationship('FavoritesPlanets', backref='user', lazy=True) #Se definen relaciones entre las tablas utilizando la función relationship de SQLAlchemy.
    favorites_characters = db.relationship('FavoritesCharacters', backref='user', lazy=True) #Se definen relaciones entre las tablas utilizando la función relationship de SQLAlchemy.

    def __repr__(self):
        return self.email   #__repr__() se utiliza para proporcionar una representación de cadena legible de un objeto.

    def serialize(self):  #En este caso, el método serialize() devuelve un diccionario que contiene tres claves: "id", "name" y "email".
                          # El valor de "id" se obtiene del atributo self.id, el valor de "name" se obtiene del atributo self.name,
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    # Aquí definimos columnas para la dirección de la tabla.
    # Tenga en cuenta que cada columna también es un atributo de instancia de Python normal.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
            #backref='characters' crea un atributo en la tabla characters que permite acceder a los registros relacionados en la tabla FavoritesCharacters, y 
        # lazy=True configura la carga diferida de los registros relacionados, cargandolos solo cuando se accede a ellos explicitamente.
    favorites_character = db.relationship('FavoritesCharacters', backref='characters', lazy=True) #backref en SQLAlchemy es utilizada para establecer una relacion
                                                                                            #bidireccional entre las tablas. En este caso, cuando se establece 
                                                                                            # backref='characters' en la relación de la tabla FavoritesCharacters, se crea 
                                                                                            # automáticamente un atributo adicional en la tabla Characters que permite 
                                                                                            # acceder a los registros relacionados en la tabla FavoritesCharacters
    def __repr__(self):
        return '<Characters %r>' %  self.name #

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planets(db.Model):
    __tablename__ = 'planets'
    # Aquí definimos columnas para la dirección de la tabla.
    # Tenga en cuenta que cada columna también es un atributo de instancia de Python normal.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False) 
    terrain = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    favorites_planets = db.relationship('FavoritesPlanets', backref='planets', lazy=True) #lazy=True se utiliza para configurar la carga diferida (lazy loading) de los 
                                                                                        #registros relacionados. Con lazy=True, los registros relacionados se cargarán 
                                                                                        # solo cuando se acceda a ellos explícitamente. Esto puede ser util para mejorar el
                                                                                        #  rendimiento, ya que evita la carga de todos los registros relacionados de forma 
                                                                                        # automatica.
    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population":self.population
        }


class FavoritesCharacters(db.Model):
    __tablename__ = "favoritescharacters"
    id = db.Column (db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)

    def __repr__(self):
        return str(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id,
        }    

class FavoritesPlanets(db.Model):
    __tablename__ = "favoritesplanets"
    id = db.Column (db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return str(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.user_id
        }    

