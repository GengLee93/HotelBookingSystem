from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import db, Booking, User, Service
from sqlalchemy import or_
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET', 'POST'])
def dashboard():
    """Admin dashboard for searching and viewing bookings."""
    query = Booking.query.join(User).options(db.joinedload(Booking.service))
    search_criteria = {}

    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        customer_name = request.form.get('customer_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        search_criteria = {
            'booking_id': booking_id,
            'customer_name': customer_name,
            'start_date': start_date,
            'end_date': end_date
        }

        if booking_id:
            try:
                query = query.filter(Booking.id == int(booking_id))
            except ValueError:
                flash('Invalid Booking ID format.', 'danger')
        
        if customer_name:
            query = query.filter(or_(User.name.ilike(f"%%{customer_name}%%"), User.email.ilike(f"%%{customer_name}%%")))

        if start_date and end_date:
            query = query.filter(Booking.check_in_date >= start_date, Booking.check_out_date <= end_date)

    bookings = query.order_by(Booking.check_in_date.desc()).all()
    
    return render_template('admin.html', bookings=bookings, search_criteria=search_criteria)

@admin.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    """Edit a booking's details."""
    booking = Booking.query.get_or_404(booking_id)
    
    if request.method == 'POST':
        # Get form data
        service_id = request.form.get('service_id')
        check_in_str = request.form.get('check_in_date')
        check_out_str = request.form.get('check_out_date')

        # Validate dates
        try:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            if check_out_date <= check_in_date:
                flash('Check-out date must be after check-in date.', 'danger')
                return redirect(url_for('admin.edit_booking', booking_id=booking.id))
        except (ValueError, TypeError):
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('admin.edit_booking', booking_id=booking.id))

        # Update booking object
        booking.service_id = service_id
        booking.check_in_date = check_in_date
        booking.check_out_date = check_out_date
        
        db.session.commit()
        flash(f'Booking #{booking.id} has been updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    # For GET request, show the form
    services = Service.query.all()
    return render_template('admin_edit_booking.html', booking=booking, services=services)

@admin.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    """Cancel (delete) a booking."""
    booking = Booking.query.get_or_404(booking_id)
    try:
        db.session.delete(booking)
        db.session.commit()
        flash(f'Booking #{booking.id} has been successfully canceled.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error canceling booking: {e}', 'danger')
        
    return redirect(url_for('admin.dashboard'))
