from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt, mail
from werkzeug.security import generate_password_hash

# --- Import Models to register with SQLAlchemy metadata ---
from models.user_model import User
from models.product_model import Product
from models.order_model import Order
from models.review_model import Review
from models.delivery_model import Delivery
from models.notification_model import Notification


def _seed_sample_products():
    """Insert demo data if DB is empty."""
    if User.query.first() is None:
        demo_farmer = User(
            name='Ramesh Kumar (Demo Farmer)',
            email='farmer@agrohub.com',
            password_hash=generate_password_hash('password123'),
            role='farmer',
            phone='9876543210',
            address='Village Rampur, Haryana, India',
            referral_code='AHFARMER1',
            farm_location='Rampur, Haryana',
            farming_type='Organic',
            crops_category='Vegetables,Grains,Fruits',
            quantity_available='500 kg assorted',
            upi_id='ramesh@upi',
            preferred_language='hindi',
            rating=4.5,
            rating_count=12,
        )
        db.session.add(demo_farmer)

        demo_customer = User(
            name='Priya Sharma (Demo Customer)',
            email='customer@agrohub.com',
            password_hash=generate_password_hash('password123'),
            role='customer',
            phone='9123456789',
            address='Flat 4B, Andheri West, Mumbai',
            referral_code='AHCUST001',
            preferred_language='english',
            payment_method='upi',
        )
        db.session.add(demo_customer)

        demo_delivery = User(
            name='Suresh Delivery (Demo Rider)',
            email='delivery@agrohub.com',
            password_hash=generate_password_hash('password123'),
            role='delivery',
            phone='9988776655',
            referral_code='AHDELIV01',
            vehicle_type='Bike',
            license_number='MH01AB1234',
            availability_status='online',
            rating=4.2,
            rating_count=8,
        )
        db.session.add(demo_delivery)
        db.session.flush()

        sample_products = [
            Product(farmer_id=demo_farmer.id, name='Fresh Tomatoes',    category='Vegetables',
                    price=45.00, stock=200, unit='kg', image_url='/Frontend/images/tomato.jpg',
                    description='Organically grown red tomatoes, freshly harvested.'),
            Product(farmer_id=demo_farmer.id, name='Basmati Rice',      category='Grains',
                    price=120.00, stock=500, unit='kg', image_url='/Frontend/images/rice.jpg',
                    description='Premium long-grain Basmati rice from Punjab farms.'),
            Product(farmer_id=demo_farmer.id, name='Alphonso Mangoes',  category='Fruits',
                    price=350.00, stock=80,  unit='dozen', image_url='/Frontend/images/mango.jpg',
                    description='Sweet Alphonso mangoes from Ratnagiri.'),
            Product(farmer_id=demo_farmer.id, name='Spinach Bunch',     category='Vegetables',
                    price=25.00, stock=150, unit='bunch', image_url='/Frontend/images/spinach.jpg',
                    description='Fresh green spinach, pesticide-free.'),
            Product(farmer_id=demo_farmer.id, name='Turmeric Powder',   category='Spices',
                    price=90.00, stock=100, unit='kg', image_url='/Frontend/images/turmaric powder.jpg',
                    description='Pure organic turmeric from Kerala.'),
            Product(farmer_id=demo_farmer.id, name='Moong Dal',         category='Pulses',
                    price=110.00, stock=300, unit='kg', image_url='/Frontend/images/moong dal.jpg',
                    description='Yellow moong dal, sun-dried and stone-cleaned.'),
            Product(farmer_id=demo_farmer.id, name='Desi Butter',       category='Dairy',
                    price=60.00, stock=100, unit='pack', image_url='/Frontend/images/butter.jpg',
                    description='Pure desi cow butter, chilled fresh daily.'),
            Product(farmer_id=demo_farmer.id, name='Red Onions',        category='Vegetables',
                    price=35.00, stock=300, unit='kg', image_url='/Frontend/images/onion.jpg',
                    description='Fresh red onions, farm direct.'),
            Product(farmer_id=demo_farmer.id, name='Green Cardamom',    category='Spices',
                    price=180.00, stock=50,  unit='100g', image_url='/Frontend/images/cardamom.jpg',
                    description='Premium Kerala green cardamom pods.'),
            Product(farmer_id=demo_farmer.id, name='Sweet Corn',        category='Vegetables',
                    price=40.00, stock=120, unit='dozen', image_url='/Frontend/images/corn.jpg',
                    description='Golden sweet corn, farm fresh.'),
            Product(farmer_id=demo_farmer.id, name='Fresh Milk',        category='Dairy',
                    price=55.00, stock=200, unit='liter', image_url='/Frontend/images/milk.jpg',
                    description='Pure cow milk, delivered fresh every morning.'),
            Product(farmer_id=demo_farmer.id, name='Wheat', category='Grains',
                    price=45.00, stock=400, unit='kg', image_url='/Frontend/images/wheat.jpg',
                    description='Stone-ground whole wheat flour.'),
            Product(farmer_id=demo_farmer.id, name='Amchur Powder',     category='Spices',
                    price=150.00, stock=50,  unit='kg', image_url='/Frontend/images/amchur powder.webp',
                    description='Tangy dried mango powder.'),
            Product(farmer_id=demo_farmer.id, name='Fresh Apples',      category='Fruits',
                    price=180.00, stock=100, unit='kg', image_url='/Frontend/images/apple.jpg',
                    description='Crunchy red apples from Himachal.'),
            Product(farmer_id=demo_farmer.id, name='Arhar Dal',         category='Pulses',
                    price=140.00, stock=200, unit='kg', image_url='/Frontend/images/arhar dal.jpg',
                    description='Protein-rich arhar dal (Toor dal).'),
            Product(farmer_id=demo_farmer.id, name='Ripe Bananas',      category='Fruits',
                    price=60.00,  stock=150, unit='dozen', image_url='/Frontend/images/banana.jpg',
                    description='Fresh yellow bananas from Jalgaon.'),
            Product(farmer_id=demo_farmer.id, name='Bottle Guard',      category='Vegetables',
                    price=30.00,  stock=100, unit='kg', image_url='/Frontend/images/bottleguard.jpg',
                    description='Fresh and tender Lauki (Bottle Guard).'),
            Product(farmer_id=demo_farmer.id, name='Brinjal',           category='Vegetables',
                    price=40.00,  stock=120, unit='kg', image_url='/Frontend/images/bringal.jpg',
                    description='Purple shiny brinjals, farm fresh.'),
            Product(farmer_id=demo_farmer.id, name='Chana Dal',         category='Pulses',
                    price=95.00,  stock=250, unit='kg', image_url='/Frontend/images/chana dal.jpg',
                    description='Yellow split chickpeas.'),
            Product(farmer_id=demo_farmer.id, name='Fresh Coriander',   category='Vegetables',
                    price=20.00,  stock=100, unit='bunch', image_url='/Frontend/images/coriander.jpg',
                    description='Fragrant green coriander leaves.'),
            Product(farmer_id=demo_farmer.id, name='Lady Finger',       category='Vegetables',
                    price=50.00,  stock=100, unit='kg', image_url='/Frontend/images/lady finger.jpg',
                    description='Fresh Bhindi (Lady Finger).'),
            Product(farmer_id=demo_farmer.id, name='Organic Oats',      category='Grains',
                    price=120.00, stock=80,  unit='kg', image_url='/Frontend/images/oats.jpg',
                    description='Healthy whole grain oats.'),
            Product(farmer_id=demo_farmer.id, name='Juicy Oranges',     category='Fruits',
                    price=100.00, stock=120, unit='kg', image_url='/Frontend/images/orange.jpg',
                    description='Sweet and tangy Nagpur oranges.'),
            Product(farmer_id=demo_farmer.id, name='Fresh Paneer',      category='Dairy',
                    price=320.00, stock=40,  unit='kg', image_url='/Frontend/images/paneer.jpg',
                    description='Soft and fresh malai paneer.'),
            Product(farmer_id=demo_farmer.id, name='Sweet Pineapple',   category='Fruits',
                    price=80.00,  stock=60,  unit='piece', image_url='/Frontend/images/pineapple.jpg',
                    description='Tropical sweet pineapples.'),
            Product(farmer_id=demo_farmer.id, name='Fresh Potatoes',    category='Vegetables',
                    price=30.00,  stock=500, unit='kg', image_url='/Frontend/images/potato.jpg',
                    description='Farm fresh potatoes, ideal for all dishes.'),
            Product(farmer_id=demo_farmer.id, name='Red Chilli Powder', category='Spices',
                    price=220.00, stock=70,  unit='kg', image_url='/Frontend/images/red chilli powder.jpeg',
                    description='Spicy ground red chillies.'),
            Product(farmer_id=demo_farmer.id, name='Soya Beans',        category='Pulses',
                    price=85.00,  stock=300, unit='kg', image_url='/Frontend/images/soyabean.jpg',
                    description='High-protein soya beans.'),
            Product(farmer_id=demo_farmer.id, name='Toor Dal',          category='Pulses',
                    price=145.00, stock=180, unit='kg', image_url='/Frontend/images/toor dal.jpg',
                    description='Premium quality split pigeon peas.'),
            Product(farmer_id=demo_farmer.id, name='Watermelon',        category='Fruits',
                    price=40.00,  stock=50,  unit='piece', image_url='/Frontend/images/watermelon.jpg',
                    description='Sweet and hydrating watermelons.'),
        ]
        db.session.add_all(sample_products)
        db.session.commit()


def create_app():
    app = Flask(__name__, static_folder='../Frontend', static_url_path='/Frontend')
    app.config.from_object(Config)
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # ── Register Blueprints ──────────────────────────
    from routes.auth_routes     import auth_bp
    from routes.product_routes  import product_bp
    from routes.order_routes    import order_bp
    from routes.tracking_routes import tracking_bp
    from routes.user_routes     import user_bp
    from routes.review_routes   import review_bp
    from routes.delivery_routes import delivery_bp
    from routes.weather_routes  import weather_bp
    from routes.admin_routes    import admin_bp
    from routes.notification_routes import notification_bp
    from routes.support_routes      import support_bp

    app.register_blueprint(auth_bp,     url_prefix='/api/auth')
    app.register_blueprint(product_bp,  url_prefix='/api/products')
    app.register_blueprint(order_bp,    url_prefix='/api/orders')
    app.register_blueprint(tracking_bp, url_prefix='/api/track')
    app.register_blueprint(user_bp,     url_prefix='/api/user')
    app.register_blueprint(review_bp,   url_prefix='/api/reviews')
    app.register_blueprint(delivery_bp, url_prefix='/api/delivery')
    app.register_blueprint(weather_bp,  url_prefix='/api/weather')
    app.register_blueprint(admin_bp,    url_prefix='/api/admin')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(support_bp,      url_prefix='/api/support')

    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect('/Frontend/html/index.html')

    # Create all tables & seed demo data
    with app.app_context():
        print("Creating all tables...")
        db.create_all()
        print("Seeding demo data...")
        _seed_sample_products()
        print("Seeding complete.")

    return app

# Expose app for 'flask run'
app = create_app()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
