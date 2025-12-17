from app import create_app, db
from app.models import Booking, User, Service
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    # 使用 SQLAlchemy 的 drop_all() 方法刪除所有定義在 models 中的資料表
    # 這會自動處理外鍵依賴關係
    db.drop_all()
    
    print("Creating all tables...")
    # 根據新的 models 重新建立資料表
    db.create_all()
    
    print("Seeding database...")
    # 重新填入初始資料
    # 這裡我們直接呼叫 app/__init__.py 中的 seed_database 邏輯
    # 但因為 seed_database 沒有被 export，我們直接在這裡重寫一次簡單的 seed 邏輯
    
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
    
    print("Database reset and seeded successfully!")
