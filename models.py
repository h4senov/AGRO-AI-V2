from datetime import datetime, timedelta
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# -------------------- FERMER --------------------
class Fermer(db.Model):
    __tablename__ = "fermer"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    contact_info = db.Column(db.String(100))
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"))

    area = db.relationship("Area", back_populates="fermers")
    problems = db.relationship("Problem", back_populates="fermer")
    expenses = db.relationship("Expense", back_populates="fermer")
    income = db.relationship("Income", back_populates="fermer")
    products = db.relationship("Product", back_populates="fermer")


# -------------------- AREA --------------------
class Area(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    gps = db.Column(db.String(100))
    region = db.Column(db.String(100))
    size_hectares = db.Column(db.Float)
    soil_id = db.Column(db.Integer, db.ForeignKey("soil.id"))
    approval_document = db.Column(db.String(200))

    soil = db.relationship("Soil", back_populates="areas")
    status = db.relationship("AreaStatus", back_populates="area")
    sensors = db.relationship("Sensor", back_populates="area")
    fermers = db.relationship("Fermer", back_populates="area")
    plants = db.relationship("Plant", back_populates="area")


# -------------------- SOIL --------------------
class Soil(db.Model):
    __tablename__ = "soil"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    ph = db.Column(db.Float)
    nutrients = db.Column(db.Text)
    description = db.Column(db.Text)

    areas = db.relationship("Area", back_populates="soil")


# -------------------- AREA_STATUS --------------------
class AreaStatus(db.Model):
    __tablename__ = "area_status"

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"))
    specialist_id = db.Column(db.Integer, db.ForeignKey("specialist.id"))
    inspection_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20))  # yaxşı / orta / pis və ya ballıq

    area = db.relationship("Area", back_populates="status")
    specialist = db.relationship("Specialist", back_populates="inspections")


# -------------------- SPECIALIST --------------------
class Specialist(db.Model):
    __tablename__ = "specialist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    contact_info = db.Column(db.String(100))

    inspections = db.relationship("AreaStatus", back_populates="specialist")
    problems_solved = db.relationship("Problem", back_populates="specialist")

    @property
    def full_name(self):    
        return f"{self.name} {self.last_name}"  

# -------------------- PROBLEMS --------------------
class Problem(db.Model):
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    fermer_id = db.Column(db.Integer, db.ForeignKey("fermer.id"))
    plants_id = db.Column(db.Integer, db.ForeignKey("plants.id"), nullable=True)
    description = db.Column(db.Text)
    solved_by_id = db.Column(db.Integer, db.ForeignKey("specialist.id"))
    status = db.Column(db.String(20))  # həll edildi / gözləyir

    fermer = db.relationship("Fermer", back_populates="problems")
    specialist = db.relationship("Specialist", back_populates="problems_solved")
    plant = db.relationship("Plant", back_populates="problems")


# -------------------- EXPENSES --------------------
class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    fermer_id = db.Column(db.Integer, db.ForeignKey("fermer.id"))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))  # suvarma, gübrə, işçi və s.
    date = db.Column(db.Date)

    fermer = db.relationship("Fermer", back_populates="expenses")


# -------------------- INCOME --------------------
class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    fermer_id = db.Column(db.Integer, db.ForeignKey("fermer.id"))
    amount = db.Column(db.Float)
    source = db.Column(db.String(50))  # satış, subsidiya və s.
    date = db.Column(db.Date)

    fermer = db.relationship("Fermer", back_populates="income")


# -------------------- PRODUCTS --------------------
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    fermer_id = db.Column(db.Integer, db.ForeignKey("fermer.id"))
    plants_id = db.Column(db.Integer, db.ForeignKey("plants.id"))
    quantity = db.Column(db.Float)
    harvest_date = db.Column(db.Date)

    fermer = db.relationship("Fermer", back_populates="products")
    plant = db.relationship("Plant", back_populates="products")

# -------------------- PLANT_BASE --------------------
class PlantBase(db.Model):
    __tablename__ = "plant_base"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))
    synonyms = db.Column(db.Text)
    family = db.Column(db.String(100))
    description = db.Column(db.Text)
    pests = db.Column(db.Text)
    plant_image_id = db.Column(db.Integer, db.ForeignKey("plant_image.id"))

    # əsas şəkil
    main_image = db.relationship(
        "PlantImage",
        foreign_keys=[plant_image_id],
        uselist=False
    )

    # bütün şəkillər
    images = db.relationship(
        "PlantImage",
        back_populates="plant",
        foreign_keys="PlantImage.plant_id"
    )

    sensors = db.relationship("PlantSensorData", back_populates="plant")
    plants = db.relationship("Plant", back_populates="plant_base")

    def __repr__(self):
        return f"<PlantBase {self.id} - {self.name} ({self.scientific_name}), Family: {self.family}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "scientific_name": self.scientific_name,
            "synonyms": self.synonyms,
            "family": self.family,
            "description": self.description,
            "pests": self.pests,
            "plant_image_id": self.plant_image_id,
            "image_url": self.main_image.image_url if self.main_image else "/static/default_plant.jpg"
        }


# -------------------- PLANT_IMAGE --------------------
class PlantImage(db.Model):
    __tablename__ = "plant_image"

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant_base.id"))
    image_url = db.Column(
        db.String(200),
        default="/static/default_plant.jpg"  # default şəkil
    )
    description = db.Column(db.Text)

    plant = db.relationship(
        "PlantBase",
        back_populates="images",
        foreign_keys=[plant_id]
    )

    def __repr__(self):
        return f"<PlantImage {self.id} - {self.plant_id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "plant_id": self.plant_id,
            "image_url": self.image_url,
            "description": self.description,
        }

 

# -------------------- PLANT_SENSOR_DATA --------------------
class PlantSensorData(db.Model):
    __tablename__ = "plant_sensor_data"

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant_base.id"))
    optimal_soil_ph = db.Column(db.Float)
    optimal_soil_moisture = db.Column(db.Float)
    optimal_temperature_range = db.Column(db.String(50))
    optimal_humidity_range = db.Column(db.String(50))
    nutrient_requirements = db.Column(db.Text)
    water_need_per_day = db.Column(db.Float)
    light_need_per_day = db.Column(db.Float)
    growth_stage_descriptions = db.Column(db.Text)
    environment_notes = db.Column(db.Text)

    plant = db.relationship("PlantBase", back_populates="sensors")

    def __repr__(self):
        return f"<PlantSensorData {self.id} - {self.plant_id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "plant_id": self.plant_id,
            "optimal_soil_ph": self.optimal_soil_ph,
            "optimal_soil_moisture": self.optimal_soil_moisture,
            "optimal_temperature_range": self.optimal_temperature_range,
            "optimal_humidity_range": self.optimal_humidity_range,
            "nutrient_requirements": self.nutrient_requirements,
            "water_need_per_day": self.water_need_per_day,
            "light_need_per_day": self.light_need_per_day,
            "growth_stage_descriptions": self.growth_stage_descriptions,
            "environment_notes": self.environment_notes,
        }

 
# -------------------- PLANTS --------------------
class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant_base.id"))
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"))
    status = db.Column(db.String(50))
    planted_date = db.Column(db.Date)
    harvest_estimate = db.Column(db.Date)
    notes = db.Column(db.Text)
    sensor_data_reference = db.Column(db.Integer, db.ForeignKey("plant_sensor_data.id"))

    plant_base = db.relationship("PlantBase", back_populates="plants")
    area = db.relationship("Area", back_populates="plants")
    problems = db.relationship("Problem", back_populates="plant")
    products = db.relationship("Product", back_populates="plant")
    
    def __repr__(self):
        return f"<Plant {self.id} - {self.plant_base.name} in Area {self.area_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "plant_id": self.plant_id,
            "area_id": self.area_id,
            "status": self.status,
            "planted_date": self.planted_date,
            "harvest_estimate": self.harvest_estimate,
            "notes": self.notes,
            "sensor_data_reference": self.sensor_data_reference,
        }


# -------------------- SENSOR --------------------
class Sensor(db.Model):
    __tablename__ = "sensor"

    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"))
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id"), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    humidity = db.Column(db.Float)
    ph = db.Column(db.Float)
    soil_moisture = db.Column(db.Float)
    temperature = db.Column(db.Float)

    area = db.relationship("Area", back_populates="sensors")
    plant = db.relationship("Plant")

    def __repr__(self):
        return f"<Sensor {self.id} - Plant {self.plant_id}, Area {self.area_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "area_id": self.area_id,
            "plant_id": self.plant_id,
            "timestamp": self.timestamp,
            "humidity": self.humidity,
            "ph": self.ph,
            "soil_moisture": self.soil_moisture,
            "temperature": self.temperature,
        }


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
