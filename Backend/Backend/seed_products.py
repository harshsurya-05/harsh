import os
import sys
import random

# Setup path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models.user_model import User
from models.product_model import Product

app = create_app()

sample_data = {
    'Vegetables': [
        ('Fresh Tomato', 40.0, 'kg', 'Farm fresh red tomatoes', 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&q=80'),
        ('Potato', 30.0, 'kg', 'Quality potatoes', 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&q=80'),
        ('Red Onion', 50.0, 'kg', 'Fresh red onions', 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=400&q=80'),
        ('Cabbage', 25.0, 'piece', 'Large green cabbage', 'https://images.unsplash.com/photo-1596482163484-9d5543c1626f?w=400&q=80'),
        ('Carrot', 45.0, 'kg', 'Sweet orange carrots', 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=400&q=80'),
        ('Spinach (Palak)', 20.0, 'bunch', 'Fresh leafy spinach', 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&q=80'),
        ('Cauliflower', 35.0, 'piece', 'Fresh cauliflower', 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=400&q=80'),
        ('Capsicum (Green)', 60.0, 'kg', 'Crisp green bell peppers', 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa8a?w=400&q=80'),
        ('Brinjal', 40.0, 'kg', 'Purple eggplant', 'https://plus.unsplash.com/premium_photo-1664300900349-afb5fbc9a85c?w=400&q=80'),
        ('Green Peas', 80.0, 'kg', 'Sweet green peas', 'https://images.unsplash.com/photo-1596482164326-805c8a329d66?w=400&q=80')
    ],
    'Fruits': [
        ('Apple (Fuji)', 150.0, 'kg', 'Sweet and crisp apples', 'https://images.unsplash.com/photo-1560806887-1e4cd0b6faa6?w=400&q=80'),
        ('Banana', 60.0, 'dozen', 'Fresh yellow bananas', 'https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400&q=80'),
        ('Alphonso Mango', 300.0, 'dozen', 'Premium Alphonso Mangoes', 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&q=80'),
        ('Orange', 80.0, 'kg', 'Juicy oranges', 'https://images.unsplash.com/photo-1549888834-3ec93abae044?w=400&q=80'),
        ('Grapes', 120.0, 'kg', 'Seedless green grapes', 'https://images.unsplash.com/photo-1596363505729-4190a9506133?w=400&q=80'),
        ('Papaya', 40.0, 'piece', 'Ripe sweet papaya', 'https://images.unsplash.com/photo-1617112848923-cc2234394a8a?w=400&q=80'),
        ('Watermelon', 25.0, 'kg', 'Fresh red watermelon', 'https://images.unsplash.com/photo-1587049352847-81a56d773c1c?w=400&q=80'),
        ('Pineapple', 70.0, 'piece', 'Sweet pineapple', 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400&q=80'),
        ('Pomegranate', 140.0, 'kg', 'Fresh pomegranate', 'https://images.unsplash.com/photo-1615486171448-4afdcb9b110a?w=400&q=80'),
        ('Guava', 60.0, 'kg', 'Fresh guava', 'https://images.unsplash.com/photo-1533038590840-1cbf6d21f8a8?w=400&q=80')
    ],
    'Grains': [
        ('Premium Wheat', 35.0, 'kg', 'High quality wheat grains', 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&q=80'),
        ('Basmati Rice', 120.0, 'kg', 'Long grain basmati rice', 'https://images.unsplash.com/photo-1586201375761-83865001e8ac?w=400&q=80'),
        ('Bajra (Pearl Millet)', 40.0, 'kg', 'Nutritious bajra grains', 'https://images.unsplash.com/photo-1533727710313-2287c8a49c3f?w=400&q=80'),
        ('Jowar (Sorghum)', 45.0, 'kg', 'Healthy jowar', 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&q=80'),
        ('Maize / Corn', 30.0, 'kg', 'Dried yellow maize', 'https://images.unsplash.com/photo-1601264426569-ce5642a42dc8?w=400&q=80'),
        ('Ragi (Finger Millet)', 60.0, 'kg', 'High calcium ragi', 'https://images.unsplash.com/photo-1586201375761-83865001e8ac?w=400&q=80'),
        ('Oats', 150.0, 'kg', 'Rolled oats', 'https://images.unsplash.com/photo-1516711311099-0120ee802874?w=400&q=80'),
        ('Barley', 80.0, 'kg', 'Whole grain barley', 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&q=80'),
        ('Quinoa', 250.0, 'kg', 'Premium white quinoa', 'https://images.unsplash.com/photo-1586201375761-83865001e8ac?w=400&q=80'),
        ('Brown Rice', 100.0, 'kg', 'Healthy unpolished brown rice', 'https://images.unsplash.com/photo-1586201375761-83865001e8ac?w=400&q=80')
    ],
    'Pulses': [
        ('Toor Dal', 160.0, 'kg', 'Unpolished Toor Dal', 'https://images.unsplash.com/photo-1600188769045-8c7da197828f?w=400&q=80'),
        ('Moong Dal', 120.0, 'kg', 'Yellow Moong Dal', 'https://images.unsplash.com/photo-1589196726207-6c2e36d4df6c?w=400&q=80'),
        ('Chana Dal', 90.0, 'kg', 'Quality Chana Dal', 'https://images.unsplash.com/photo-1600188769045-8c7da197828f?w=400&q=80'),
        ('Urad Dal', 140.0, 'kg', 'White Urad Dal', 'https://images.unsplash.com/photo-1589196726207-6c2e36d4df6c?w=400&q=80'),
        ('Masoor Dal', 110.0, 'kg', 'Red Lentils / Masoor Dal', 'https://images.unsplash.com/photo-1600188769045-8c7da197828f?w=400&q=80'),
        ('Rajma (Kidney Beans)', 150.0, 'kg', 'Red Rajma', 'https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=400&q=80'),
        ('Kabuli Chana', 130.0, 'kg', 'Large White Chickpeas', 'https://images.unsplash.com/photo-1589196726207-6c2e36d4df6c?w=400&q=80'),
        ('Green Moong', 100.0, 'kg', 'Whole Green Moong', 'https://images.unsplash.com/photo-1600188769045-8c7da197828f?w=400&q=80'),
        ('Black Eyed Peas', 110.0, 'kg', 'Lobia / Black Eyed Peas', 'https://images.unsplash.com/photo-1589196726207-6c2e36d4df6c?w=400&q=80'),
        ('Soybeans', 90.0, 'kg', 'Protein rich Soybeans', 'https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=400&q=80')
    ],
    'Spices': [
        ('Turmeric Powder', 250.0, 'kg', 'Pure Turmeric Powder', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Coriander Powder', 200.0, 'kg', 'Fresh Coriander Powder', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Cumin Seeds (Jeera)', 450.0, 'kg', 'Premium Cumin Seeds', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Red Chilli Powder', 300.0, 'kg', 'Spicy Red Chilli Powder', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Black Pepper', 800.0, 'kg', 'Whole Black Pepper', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Cardamom (Elaichi)', 3000.0, 'kg', 'Green Cardamom', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Cinnamon', 600.0, 'kg', 'Cinnamon Sticks', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Cloves', 1200.0, 'kg', 'Premium Cloves', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Mustard Seeds', 150.0, 'kg', 'Black Mustard Seeds', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80'),
        ('Fenugreek Seeds', 180.0, 'kg', 'Methi Seeds', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&q=80')
    ],
    'Dairy': [
        ('Fresh Cow Milk', 60.0, 'liter', 'Farm fresh cow milk', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80'),
        ('Pure Desi Ghee', 800.0, 'kg', 'A2 Cow Ghee', 'https://images.unsplash.com/photo-1606330058814-1e03c27e0a4f?w=400&q=80'),
        ('Fresh Paneer', 350.0, 'kg', 'Soft and fresh paneer', 'https://images.unsplash.com/photo-1631452180519-c014fe946bc0?w=400&q=80'),
        ('White Butter', 450.0, 'kg', 'Homemade unsalted butter', 'https://images.unsplash.com/photo-1589301760014-d929f39ce9b0?w=400&q=80'),
        ('Curd (Dahi)', 80.0, 'kg', 'Thick fresh curd', 'https://images.unsplash.com/photo-1598926940898-316279fcc253?w=400&q=80'),
        ('Cheese Block', 500.0, 'kg', 'Processed Cheese', 'https://images.unsplash.com/photo-1618164435735-414d33966dc2?w=400&q=80'),
        ('Buttermilk (Chaas)', 30.0, 'liter', 'Spiced Buttermilk', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80'),
        ('Fresh Cream (Malai)', 400.0, 'kg', 'Thick milk cream', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80'),
        ('Khoya / Mawa', 380.0, 'kg', 'Fresh Khoya for sweets', 'https://images.unsplash.com/photo-1631452180519-c014fe946bc0?w=400&q=80'),
        ('Flavored Milk', 80.0, 'liter', 'Badam / Rose flavored milk', 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80')
    ]
}

def seed_database():
    with app.app_context():
        # Get or create a farmer
        farmer = User.query.filter_by(role='farmer').first()
        if not farmer:
            farmer = User(
                name='AgroHub Demo Farmer',
                email='farmer@demo.com',
                role='farmer',
                phone='9876543210'
            )
            farmer.set_password('password123')
            db.session.add(farmer)
            db.session.commit()
            print("Created Demo Farmer")

        # Clear existing products to prevent duplicates (optional, doing it for clean slate)
        # db.session.query(Product).delete()
        # db.session.commit()

        count = 0
        for category, items in sample_data.items():
            for item in items:
                name, price, unit, desc, img = item
                
                # Check if product exists
                exists = Product.query.filter_by(name=name, farmer_id=farmer.id).first()
                if not exists:
                    p = Product(
                        farmer_id=farmer.id,
                        name=name,
                        category=category,
                        price=price,
                        unit=unit,
                        description=desc,
                        image_url=img,
                        stock=random.randint(50, 500)
                    )
                    db.session.add(p)
                    count += 1
        
        db.session.commit()
        print(f"Successfully added {count} new sample products across 6 categories!")

if __name__ == '__main__':
    seed_database()
