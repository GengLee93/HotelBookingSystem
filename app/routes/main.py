from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from app.models import db, Booking, User, Service

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage: Display available services and a search form."""
    services = Service.query.all()
    return render_template('index.html', services=services)

@main.route('/search', methods=['POST'])
def search_booking():
    """Handle booking search by ID."""
    booking_id = request.form.get('booking_id')
    
    if not booking_id or not booking_id.isdigit():
        flash('Invalid Booking ID. Please enter a numeric ID.', 'danger')
        return redirect(url_for('main.index'))

    booking = Booking.query.get(int(booking_id))
    
    if booking:
        return render_template('index.html', booking=booking, services=Service.query.all())
    else:
        flash(f'Booking with ID "{booking_id}" not found.', 'info')
        return redirect(url_for('main.index'))

@main.route('/booking/<int:service_id>', methods=['GET'])
def booking_form(service_id):
    """Display the booking form for a specific service."""
    service = Service.query.get_or_404(service_id)
    return render_template('booking.html', service=service)

@main.route('/booking/create', methods=['POST'])
def create_booking():
    """Process the creation of a new booking."""
    service_id = request.form.get('service_id')
    customer_name = request.form.get('customer_name')
    email = request.form.get('email')
    check_in_str = request.form.get('check_in_date')
    check_out_str = request.form.get('check_out_date')

    # Validate dates
    try:
        check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        if check_out_date <= check_in_date:
            flash('Check-out date must be after check-in date.', 'danger')
            return redirect(url_for('main.booking_form', service_id=service_id))
    except (ValueError, TypeError):
        flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
        return redirect(url_for('main.booking_form', service_id=service_id))

    # Find or create user
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=customer_name, email=email)
        db.session.add(user)
        db.session.commit()

    # Create booking
    new_booking = Booking(
        user_id=user.id,
        service_id=service_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date
    )
    db.session.add(new_booking)
    db.session.commit()

    flash(f'Booking successful! Your Booking ID is {new_booking.id}.', 'success')
    return redirect(url_for('main.index'))
