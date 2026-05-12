from app import create_app, db
from models.product_model import Product

def update_images():
    app = create_app()
    with app.app_context():
        image_map = {
            'Fresh Tomatoes': '/Frontend/images/tomato.jpg',
            'Basmati Rice': '/Frontend/images/rice.jpg',
            'Alphonso Mangoes': '/Frontend/images/mango.jpg',
            'Spinach Bunch': '/Frontend/images/coriander.jpg',
            'Turmeric Powder': '/Frontend/images/turmaric powder.jpg',
            'Moong Dal': '/Frontend/images/moong dal.jpg',
            'Desi Butter': '/Frontend/images/milk.jpg',
            'Red Onions': '/Frontend/images/tomato.jpg',
            'Green Cardamom': '/Frontend/images/turmaric powder.jpg',
            'Sweet Corn': '/Frontend/images/tomato.jpg',
            'Fresh Milk': '/Frontend/images/milk.jpg',
            'Wheat Flour (Atta)': '/Frontend/images/wheat.jpg',
            'Amchur Powder': '/Frontend/images/amchur powder.webp',
            'Fresh Apples': '/Frontend/images/apple.jpg',
            'Arhar Dal': '/Frontend/images/arhar dal.jpg',
            'Ripe Bananas': '/Frontend/images/banana.jpg',
            'Bottle Guard': '/Frontend/images/bottleguard.jpg',
            'Brinjal': '/Frontend/images/bringal.jpg',
            'Chana Dal': '/Frontend/images/chana dal.jpg',
            'Fresh Coriander': '/Frontend/images/coriander.jpg',
            'Lady Finger': '/Frontend/images/lady finger.jpg',
            'Organic Oats': '/Frontend/images/oats.jpg',
            'Juicy Oranges': '/Frontend/images/orange.jpg',
            'Fresh Paneer': '/Frontend/images/paneer.jpg',
            'Sweet Pineapple': '/Frontend/images/pineapple.jpg',
            'Fresh Potatoes': '/Frontend/images/potato.jpg',
            'Red Chilli Powder': '/Frontend/images/red chilli powder.jpeg',
            'Soya Beans': '/Frontend/images/soyabean.jpg',
            'Toor Dal': '/Frontend/images/toor dal.jpg',
            'Watermelon': '/Frontend/images/watermelon.jpg',
        }

        products = Product.query.all()
        updated_count = 0
        for p in products:
            if p.name in image_map:
                p.image_url = image_map[p.name]
                updated_count += 1
        
        db.session.commit()
        print(f"Successfully updated {updated_count} products with images.")

if __name__ == '__main__':
    update_images()
