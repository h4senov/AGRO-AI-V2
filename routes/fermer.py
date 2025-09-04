from flask import request, render_template, redirect, url_for, flash
from models import db, Fermer, Area

def register_fermer_routes(app):
    

    @app.route('/fermers',methods =['GET'], endpoint='list_fermer')
    def list_fermer():
        page = request.args.get('page', 1, type=int)
        fermers = Fermer.query.paginate(page=page, per_page=10)

        return render_template('fermer/list.html', fermers=fermers)
    
    @app.route('/fermer/<int:fermer_id>', methods=['GET'], endpoint='single_fermer')
    def single_fermer(fermer_id):
        fermer = get_id(fermer_id)
        if not fermer:
            flash('Fermer not found.', 'error')
            return redirect(url_for('list_fermer'))
        areas = Area.query.all()
        return render_template('fermer/single.html', fermer=fermer, areas=areas)

    @app.route('/fermer/add', methods=['GET', 'POST'], endpoint='add_fermer')
    def add_fermer():
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            contact_info = request.form['contact_info']
            area_id = request.form.get('area_id')  # sahə seçimi (optional)

            new_fermer = Fermer(
                first_name=first_name,
                last_name=last_name,
                contact_info=contact_info,
                area_id=area_id
            )
            db.session.add(new_fermer)
            db.session.commit()
            flash('Fermer uğurla əlavə olundu!', 'success')
            return redirect(url_for('list_fermer'))

        areas = Area.query.all()  # sahə seçmək üçün
        return render_template('fermer/add.html', areas=areas)

    def get_id(id):
        fermer = Fermer.query.get_or_404(id)
        return fermer



    @app.route('/fermer/<int:fermer_id>/delete', methods=['GET'], endpoint='delete_fermer')
    def delete_fermer(fermer_id):
        fermer = get_id(fermer_id)
        db.session.delete(fermer)
        db.session.commit()
        flash('Fermer uğurla silindi!', 'success')
        return redirect(url_for('list_fermer'))

    @app.route('/fermer/<int:fermer_id>/update', methods=['POST'], endpoint='update_fermer')
    def update_fermer(fermer_id):
        fermer = get_id(fermer_id)
        fermer.first_name = request.form['first_name']
        fermer.last_name = request.form['last_name']
        fermer.contact_info = request.form['contact_info']
        fermer.area_id = request.form.get('area_id')

        db.session.commit()
        flash('Fermer məlumatları uğurla yeniləndi!', 'success')
        return redirect(url_for('single_fermer', fermer_id=fermer.id))