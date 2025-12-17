from flask import Flask
from config import Config
from .models import db
import os
from datetime import datetime

def create_app(config_class=Config):
    """
    Application factory function.
    """
    # The template_folder is now inside the 'app' directory
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Import and register blueprints
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Context processor to inject variables into all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Check if we need to seed the database with initial data
        from .models import Service
        if Service.query.first() is None:
            seed_database()

    return app

def seed_database():
    """Inserts initial data into the database."""
    from .models import Service, User, Booking
    from datetime import date

    # Create services
    service1 = Service(name='Standard Room', description='A cozy room with a double bed.', price=100.0)
    service2 = Service(name='Deluxe Room', description='A spacious room with a king-size bed and a city view.', price=180.0)
    service3 = Service(name='Meeting Room', description='A professional space for up to 10 people.', price=50.0)
    
    db.session.add_all([service1, service2, service3])
    db.session.commit()

    # Create users
    user1 = User(name='John Doe', email='john@example.com', contact_info='111-222-3333')
    user2 = User(name='Jane Smith', email='jane@example.com', contact_info='444-555-6666')

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create bookings
    booking1 = Booking(user_id=user1.id, service_id=service1.id, check_in_date=date(2025, 12, 18), check_out_date=date(2025, 12, 20))
    booking2 = Booking(user_id=user2.id, service_id=service2.id, check_in_date=date(2025, 11, 20), check_out_date=date(2025, 11, 25))

    db.session.add_all([booking1, booking2])
    db.session.commit()
    print("Database seeded with initial data.")
