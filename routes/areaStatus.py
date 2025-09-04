from flask import request, render_template, redirect, url_for, flash
from models import db, Area, AreaStatus, Specialist


def register_fermer_areaStatus(app):

    def get_status_by_id(id):
        return AreaStatus.query.get_or_404(id)

    @app.route('/status', methods=['GET'], endpoint='list_status')
    def list_status():
        page = request.args.get('page', 1, type=int)
        areaStatuses = AreaStatus.query.paginate(page=page, per_page=10)
        return render_template('areaStatus/list.html', areaStatuses=areaStatuses)

    @app.route('/status/<int:status_id>', methods=['GET'], endpoint='single_status')
    def single_status(status_id):
        areaStatus = get_status_by_id(status_id)
        return render_template('areaStatus/single.html', areaStatus=areaStatus)

    @app.route('/status/add', methods=['GET', 'POST'], endpoint='add_status')
    def add_status():
        if request.method == 'POST':
            area_id = request.form['area_id']
            specialist_id = request.form['specialist_id']
            inspection_date = request.form['inspection_date']
            notes = request.form['notes']
            status_value = request.form['status']

            new_status = AreaStatus(
                area_id=area_id,
                specialist_id=specialist_id,
                inspection_date=inspection_date,
                notes=notes,
                status=status_value
            )
            db.session.add(new_status)
            db.session.commit()
            flash('Status uğurla əlavə olundu!', 'success')
            return redirect(url_for('list_status'))

        areas = Area.query.all()
        specialists = Specialist.query.all()
        return render_template('areaStatus/add.html', areas=areas, specialists=specialists)

    @app.route('/status/<int:status_id>/delete', methods=['GET'], endpoint='delete_status')
    def delete_status(status_id):
        areaStatus = get_status_by_id(status_id)
        db.session.delete(areaStatus)
        db.session.commit()
        flash('Status uğurla silindi!', 'success')
        return redirect(url_for('list_status'))

    @app.route('/status/<int:status_id>/update', methods=['POST'], endpoint='update_status')
    def update_status(status_id):
        areaStatus = get_status_by_id(status_id)
        areaStatus.area_id = request.form['area_id']
        areaStatus.specialist_id = request.form['specialist_id']
        areaStatus.inspection_date = request.form['inspection_date']
        areaStatus.notes = request.form['notes']
        areaStatus.status = request.form['status']
        db.session.commit()
        flash('Status uğurla yeniləndi!', 'success')
        return redirect(url_for('single_status', status_id=areaStatus.id))
