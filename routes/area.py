from flask import request, render_template, redirect, url_for, flash
from models import db, Fermer, Area, Soil

def register_area_routes(app):

    @app.route('/areas', methods=['GET'], endpoint='list_area')
    def list_area():
        areas = Area.query.all()
        return render_template('area/list.html', areas=areas)

    @app.route('/area/<int:area_id>', methods=['GET'], endpoint='single_area')
    def single_area(area_id):
        area = Area.query.get_or_404(area_id)
        soils = Soil.query.all()  # sahəni update edəndə torpaq seçmək üçün
        return render_template('area/single.html', area=area, soils=soils)

    @app.route('/area/add', methods=['GET', 'POST'], endpoint='add_area')
    def add_area():
        if request.method == 'POST':
            name = request.form['name']
            location = request.form['location']
            gps = request.form['gps']
            region = request.form['region']
            size_hectares = request.form['size_hectares']
            soil_id = request.form.get('soil_id')
            approval_document = request.form['approval_document']

            new_area = Area(
                name=name,
                location=location,
                gps=gps,
                region=region,
                size_hectares=size_hectares,
                soil_id=soil_id,
                approval_document=approval_document
            )
            db.session.add(new_area)
            db.session.commit()
            flash('Yeni sahə uğurla əlavə olundu!', 'success')
            return redirect(url_for('list_area'))

        soils = Soil.query.all()
        return render_template('area/add.html', soils=soils)

    @app.route('/area/<int:area_id>/delete', methods=['GET'], endpoint='delete_area')
    def delete_area(area_id):
        area = Area.query.get_or_404(area_id)
        db.session.delete(area)
        db.session.commit()
        flash('Sahə uğurla silindi!', 'success')
        return redirect(url_for('list_area'))

    @app.route('/area/<int:area_id>/update', methods=['POST'], endpoint='update_area')
    def update_area(area_id):
        area = Area.query.get_or_404(area_id)

        area.name = request.form['name']
        area.location = request.form['location']
        area.gps = request.form['gps']
        area.region = request.form['region']
        area.size_hectares = request.form['size_hectares']
        area.soil_id = request.form.get('soil_id')
        area.approval_document = request.form['approval_document']

        db.session.commit()
        flash('Sahə məlumatları uğurla yeniləndi!', 'success')
        return redirect(url_for('single_area', area_id=area.id))
