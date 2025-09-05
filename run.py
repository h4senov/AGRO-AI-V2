from flask import Flask, render_template
from models import init_db, db
from datetime import datetime
import os
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "agro_layihe.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

    # Init DB
    init_db(app)

    migrate = Migrate(app, db)

    # Add datetime for all templates
    @app.context_processor
    def inject_now():
        return {'datetime': datetime}

    @app.route('/')
    def home():
        return render_template('base.html')

    @app.route('/init-sample-data')
    def init_sample_data_route():
        """Initialize sample data"""
        try:
            from sample_data import create_sample_data  # əlavə fayl ola bilər
            create_sample_data()
            return '<h1>Sample data created successfully!</h1><a href="/">Go Home</a>'
        except Exception as e:
            return f'<h1>Error: {str(e)}</h1><a href="/">Go Home</a>'

    # Import and register routes
    from routes.plantbase import register_plant_routes
    from routes.fermer import register_fermer_routes
    from routes.area import register_area_routes
    from routes.areaStatus import register_fermer_areaStatus
    

    register_plant_routes(app)
    register_fermer_routes(app)
    register_area_routes(app)
    register_fermer_areaStatus(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
