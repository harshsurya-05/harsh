from app import create_app, db
from models.product_model import Product
from models.user_model import User

def seed_all():
    app = create_app()
    with app.app_context():
        # Get demo farmer
        farmer = User.query.filter_by(email='farmer@agrohub.com').first()
        if not farmer:
            print("Error: Demo farmer not found. Please run the app once to create the demo farmer.")
            return

        products_to_seed = [
            {'name': 'Fresh Tomatoes',    'category': 'Vegetables', 'price': 45.00,  'stock': 200, 'unit': 'kg',    'image_url': '/Frontend/images/tomato.jpg',      'desc': 'Organically grown red tomatoes, freshly harvested.'},
            {'name': 'Basmati Rice',      'category': 'Grains',     'price': 120.00, 'stock': 500, 'unit': 'kg',    'image_url': '/Frontend/images/rice.jpg',        'desc': 'Premium long-grain Basmati rice from Punjab farms.'},
            {'name': 'Alphonso Mangoes',  'category': 'Fruits',     'price': 350.00, 'stock': 80,  'unit': 'dozen', 'image_url': '/Frontend/images/mango.jpg',       'desc': 'Sweet Alphonso mangoes from Ratnagiri.'},
            {'name': 'Spinach Bunch',     'category': 'Vegetables', 'price': 25.00,  'stock': 150, 'unit': 'bunch', 'image_url': '/Frontend/images/spinach.jpg',     'desc': 'Fresh green spinach, pesticide-free.'},
            {'name': 'Turmeric Powder',   'category': 'Spices',     'price': 90.00,  'stock': 100, 'unit': 'kg',    'image_url': '/Frontend/images/turmaric powder.jpg', 'desc': 'Pure organic turmeric from Kerala.'},
            {'name': 'Moong Dal',         'category': 'Pulses',     'price': 110.00, 'stock': 300, 'unit': 'kg',    'image_url': '/Frontend/images/moong dal.jpg',     'desc': 'Yellow moong dal, sun-dried and stone-cleaned.'},
            {'name': 'Desi Butter',       'category': 'Dairy',      'price': 60.00,  'stock': 100, 'unit': 'pack',  'image_url': '/Frontend/images/butter.jpg',      'desc': 'Pure desi cow butter, chilled fresh daily.'},
            {'name': 'Red Onions',        'category': 'Vegetables', 'price': 35.00,  'stock': 300, 'unit': 'kg',    'image_url': '/Frontend/images/onion.jpg',       'desc': 'Fresh red onions, farm direct.'},
            {'name': 'Green Cardamom',    'category': 'Spices',     'price': 180.00, 'stock': 50,  'unit': '100g',  'image_url': '/Frontend/images/cardamom.jpg',    'desc': 'Premium Kerala green cardamom pods.'},
            {'name': 'Sweet Corn',        'category': 'Vegetables', 'price': 40.00,  'stock': 120, 'unit': 'dozen', 'image_url': '/Frontend/images/corn.jpg',        'desc': 'Golden sweet corn, farm fresh.'},
            {'name': 'Fresh Milk',        'category': 'Dairy',      'price': 55.00,  'stock': 200, 'unit': 'liter', 'image_url': '/Frontend/images/milk.jpg',          'desc': 'Pure cow milk, delivered fresh every morning.'},
            {'name': 'Wheat', 'category': 'Grains',     'price': 45.00,  'stock': 400, 'unit': 'kg',    'image_url': '/Frontend/images/wheat.jpg',         'desc': 'Stone-ground whole wheat flour.'},
            {'name': 'Amchur Powder',     'category': 'Spices',     'price': 150.00, 'stock': 50,  'unit': 'kg',    'image_url': '/Frontend/images/amchur powder.webp', 'desc': 'Tangy dried mango powder.'},
            {'name': 'Fresh Apples',      'category': 'Fruits',     'price': 180.00, 'stock': 100, 'unit': 'kg',    'image_url': '/Frontend/images/apple.jpg',         'desc': 'Crunchy red apples from Himachal.'},
            {'name': 'Arhar Dal',         'category': 'Pulses',     'price': 140.00, 'stock': 200, 'unit': 'kg',    'image_url': '/Frontend/images/arhar dal.jpg',     'desc': 'Protein-rich arhar dal (Toor dal).'},
            {'name': 'Ripe Bananas',      'category': 'Fruits',     'price': 60.00,  'stock': 150, 'unit': 'dozen', 'image_url': '/Frontend/images/banana.jpg',        'desc': 'Fresh yellow bananas from Jalgaon.'},
            {'name': 'Bottle Guard',      'category': 'Vegetables', 'price': 30.00,  'stock': 100, 'unit': 'kg',    'image_url': '/Frontend/images/bottleguard.jpg',   'desc': 'Fresh and tender Lauki (Bottle Guard).'},
            {'name': 'Brinjal',           'category': 'Vegetables', 'price': 40.00,  'stock': 120, 'unit': 'kg',    'image_url': '/Frontend/images/bringal.jpg',       'desc': 'Purple shiny brinjals, farm fresh.'},
            {'name': 'Chana Dal',         'category': 'Pulses',     'price': 95.00,  'stock': 250, 'unit': 'kg',    'image_url': '/Frontend/images/chana dal.jpg',     'desc': 'Yellow split chickpeas.'},
            {'name': 'Fresh Coriander',   'category': 'Vegetables', 'price': 20.00,  'stock': 100, 'unit': 'bunch', 'image_url': '/Frontend/images/coriander.jpg',     'desc': 'Fragrant green coriander leaves.'},
            {'name': 'Lady Finger',       'category': 'Vegetables', 'price': 50.00,  'stock': 100, 'unit': 'kg',    'image_url': '/Frontend/images/lady finger.jpg',   'desc': 'Fresh Bhindi (Lady Finger).'},
            {'name': 'Organic Oats',      'category': 'Grains',     'price': 120.00, 'stock': 80,  'unit': 'kg',    'image_url': '/Frontend/images/oats.jpg',          'desc': 'Healthy whole grain oats.'},
            {'name': 'Juicy Oranges',     'category': 'Fruits',     'price': 100.00, 'stock': 120, 'unit': 'kg',    'image_url': '/Frontend/images/orange.jpg',        'desc': 'Sweet and tangy Nagpur oranges.'},
            {'name': 'Fresh Paneer',      'category': 'Dairy',      'price': 320.00, 'stock': 40,  'unit': 'kg',    'image_url': '/Frontend/images/paneer.jpg',        'desc': 'Soft and fresh malai paneer.'},
            {'name': 'Sweet Pineapple',   'category': 'Fruits',     'price': 80.00,  'stock': 60,  'unit': 'piece', 'image_url': '/Frontend/images/pineapple.jpg',     'desc': 'Tropical sweet pineapples.'},
            {'name': 'Fresh Potatoes',    'category': 'Vegetables', 'price': 30.00,  'stock': 500, 'unit': 'kg',    'image_url': '/Frontend/images/potato.jpg',        'desc': 'Farm fresh potatoes, ideal for all dishes.'},
            {'name': 'Red Chilli Powder', 'category': 'Spices',     'price': 220.00, 'stock': 70,  'unit': 'kg',    'image_url': '/Frontend/images/red chilli powder.jpeg', 'desc': 'Spicy ground red chillies.'},
            {'name': 'Soya Beans',        'category': 'Pulses',     'price': 85.00,  'stock': 300, 'unit': 'kg',    'image_url': '/Frontend/images/soyabean.jpg',      'desc': 'High-protein soya beans.'},
            {'name': 'Toor Dal',          'category': 'Pulses',     'price': 145.00, 'stock': 180, 'unit': 'kg',    'image_url': '/Frontend/images/toor dal.jpg',      'desc': 'Premium quality split pigeon peas.'},
            {'name': 'Watermelon',        'category': 'Fruits',     'price': 40.00,  'stock': 50,  'unit': 'piece', 'image_url': '/Frontend/images/watermelon.jpg',    'desc': 'Sweet and hydrating watermelons.'},
        ]

        added_count = 0
        updated_count = 0
        for p_data in products_to_seed:
            existing = Product.query.filter_by(name=p_data['name']).first()
            if existing:
                existing.image_url = p_data['image_url']
                existing.category = p_data['category']
                existing.price = p_data['price']
                existing.stock = p_data['stock']
                existing.unit = p_data['unit']
                existing.description = p_data['desc']
                updated_count += 1
            else:
                new_p = Product(
                    farmer_id=farmer.id,
                    name=p_data['name'],
                    category=p_data['category'],
                    price=p_data['price'],
                    stock=p_data['stock'],
                    unit=p_data['unit'],
                    image_url=p_data['image_url'],
                    description=p_data['desc']
                )
                db.session.add(new_p)
                added_count += 1
        
        db.session.commit()
        print(f"Successfully seeded/updated products: {added_count} added, {updated_count} updated.")

if __name__ == '__main__':
    seed_all()
