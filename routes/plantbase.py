from flask import request, render_template, redirect, url_for, flash
from models import db, PlantBase, PlantImage
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os

def register_plant_routes(app):

    @app.route('/plantbase', methods=['GET'], endpoint='list_plants')
    def list_plants():
        page = request.args.get('page', 1, type=int)
        plants = PlantBase.query.paginate(page=page, per_page=10)

        return render_template('baseplant/plantbase.html', plants=plants)

    @app.route('/plantbase/<int:plant_id>', methods=['GET'], endpoint='single_plant_detail')
    def single_plant_detail(plant_id):
        plant = PlantBase.query.get_or_404(plant_id)
        if not plant:
            flash('Plant not found.', 'error')
            return redirect(url_for('list_plants'))
        return render_template('baseplant/single.html', plant=plant)

    @app.route('/plant/add', methods=['GET', 'POST'], endpoint='add_plant_base')
    def add_plant_base():
        if request.method == 'POST':
            # Form məlumatları
            name = request.form['name']
            scientific_name = request.form.get('scientific_name')
            synonyms = request.form.get('synonyms')
            family = request.form.get('family')
            description = request.form.get('description')
            pests = request.form.get('pests')

            # Şəkil yükləmə
            image_file = request.files.get('image')
            new_image = None
            plant_image_id = None

            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                upload_folder = os.path.join('static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                image_file.save(filepath)

                # PlantImage əlavə et və commit et ki, ID yaransın
                new_image = PlantImage(image_url=filepath)
                db.session.add(new_image)
                db.session.commit()  # burada ID yaranır
                plant_image_id = new_image.id

            # Yeni bitki əlavə et
            new_plant = PlantBase(
                name=name,
                scientific_name=scientific_name,
                synonyms=synonyms,
                family=family,
                description=description,
                pests=pests,
                plant_image_id=plant_image_id  # əsas şəkil
            )
            db.session.add(new_plant)
            db.session.commit()

            # Əgər şəkil varsa, PlantImage.plant_id-ni set et
            if new_image:
                new_image.plant_id = new_plant.id
                db.session.commit()

            flash('New plant added successfully!', 'success')
            return redirect(url_for('list_plants'))

        return render_template('baseplant/add.html')

    @app.route('/plantbase/<int:plant_id>/edit', methods=['GET', 'POST'], endpoint='edit_plant_base')
    def edit_plant_base(plant_id):
        plant = PlantBase.query.get_or_404(plant_id)

        if request.method == 'POST':
            plant.name = request.form['name']
            plant.scientific_name = request.form['scientific_name']
            plant.synonyms = request.form['synonyms']
            plant.family = request.form['family']
            plant.description = request.form['description']
            plant.pests = request.form['pests']
            plant_image_id = request.form.get('plant_image_id')
            plant.plant_image_id = plant_image_id if plant_image_id != '' else None

            try:
                db.session.commit()
                flash('Plant updated successfully!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error: Plant with this name already exists.', 'danger')

            return redirect(url_for('list_plants'))

        return render_template('baseplant/edit.html', plant=plant)

    @app.route('/plantbase/<int:plant_id>/delete', methods=['GET', 'POST'], endpoint='delete_plant_base')
    def delete_plant_base(plant_id):
        plant = PlantBase.query.get_or_404(plant_id)
        db.session.delete(plant)
        db.session.commit()
        flash('Plant deleted successfully!', 'success')
        return redirect(url_for('list_plants'))
