from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import os
from flask_cors import CORS
import jwt

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

db = SQLAlchemy(app)

# Initializing Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'index'

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Dummy users
users = []

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Login successful', 'token': token, 'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }}), 200

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/about', methods=['GET'])
def about_api():
    data = {
        "title": "Redefining Sports Excellence",
        "description": "At Sportify, we're revolutionizing the sports industry through innovation, passion, and cutting-edge technology.",
        "team": [
            {
                "name": "Ishardeep Singh",
                "role": "Team Leader",
                "bio": "I’m a first-year B.Tech student at Chitkara University, specializing in Computer Science with a focus on AI.",
                "image": "http://localhost:5000/static/images/ishar.jpeg",
                "linkedin": "https://www.linkedin.com/in/ishardeep-singh-743789311/",
                "github": "https://github.com/ishar06"
            },
            {
                "name": "Aryan Verma",
                "role": "Team Member",
                "bio": "I’m Aryan Verma, a first-year B.Tech student at Chitkara University.",
                "image": "http://localhost:5000/static/images/aryan.jpeg",

                "linkedin": "https://www.linkedin.com/in/aryan-verma-638594320/",
                "github": "https://github.com/Aryan-verma-ai"
            },
            {
                "name": "Damanjeet Singh",
                "role": "Team Member",
                "bio": "I’m Damanjeet Singh, a first-year B.Tech student at Chitkara University.",
                "image": "http://localhost:5000/static/images/daman.jpeg",
                "linkedin": "https://www.linkedin.com/in/damanjeet-singh-834596316/",
                "github": "https://github.com/daman-max"
            },
            {
                "name": "Madhav Garg",
                "role": "Team Member",
                "bio": "I’m Madhav Garg, a first-year B.Tech student at Chitkara University.",
                "image": "http://localhost:5000/static/images/madhav.jpeg",
                "linkedin": "https://www.linkedin.com/in/madhav-garg-059b4b339/",
                "github": "https://github.com/madhav205"
            }
        ]
    }
    return jsonify(data)


#--------------- MODELS --------------------------


# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)  

# Address Model
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    house_street = db.Column(db.String(200), nullable=False)
    landmark = db.Column(db.String(100))
    pincode = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(100), nullable=False)

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    image_url = db.Column(db.String(500))


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    payment_method = db.Column(db.String(50), nullable=False)
    shipping_address = db.Column(db.String(500), nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)



# Creating the database table
with app.app_context():
    db.drop_all()  #
    db.create_all()



# ------ APP ROUTES -----------

@app.route('/')
def index():
    address = None
    if current_user.is_authenticated:
        address = Address.query.filter_by(user_id=current_user.id).first()
    
    return render_template('index.html', address=address)

@app.route('/subscribe')
def subscribe():
    if current_user.is_authenticated:
        flash('Subscription successful! Check your email for future updates.', 'success')
        return redirect(url_for('index'))
    else:
        flash('Login to Subscribe with us!', 'danger')
        return redirect(url_for('index'))

@app.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    return render_template('orders.html', orders=orders)

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the data whether it's JSON or form data
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        if not email or not password:
            return jsonify({
                'status': 'fail',
                'message': 'Email and password are required'
            }), 400

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            
            # Generate JWT token
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            }), 200
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Invalid email or password'
            }), 401

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get the data from either JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        # Extract data with validation
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        password = data.get('password')

        # Validate required fields
        if not all([name, email, phone_number, password]):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        # Check for existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': 'Email already registered'
            }), 409

        # Create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # Auto login after registration
        login_user(new_user)

        return jsonify({
            'status': 'success',
            'message': 'Registration successful',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/update_user', methods=['POST'])
@login_required
def update_user():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        current_user.phone_number = request.form.get('phoneNumber')
        db.session.commit()
        flash('Your information has been updated!', 'success')
    return redirect(url_for('index'))

@app.route('/update_address', methods=['POST'])
@login_required
def update_address():
    if request.method == 'POST':
        address = Address.query.filter_by(user_id=current_user.id).first()
        if address:
            address.house_street = request.form.get('house_street')
            address.landmark = request.form.get('landmark')
            address.pincode = request.form.get('pincode')
            address.state = request.form.get('state')
            db.session.commit()
            flash('Your address has been updated!', 'success')
        else:
            flash('No address found to update.', 'danger')
    return redirect(url_for('index'))

@app.route('/save_address', methods=['POST'])
@login_required
def save_address():
    if request.method == 'POST':
        house_street = request.form.get('house_street')
        landmark = request.form.get('landmark')
        pincode = request.form.get('pincode')
        state = request.form.get('state')

        # Check if the user already has an address
        address = Address.query.filter_by(user_id=current_user.id).first()
        if address:
            address.house_street = house_street
            address.landmark = landmark
            address.pincode = pincode
            address.state = state
        else:
            # Create a new address
            new_address = Address(
                user_id=current_user.id,
                house_street=house_street,
                landmark=landmark,
                pincode=pincode,
                state=state
            )
            db.session.add(new_address)
        db.session.commit()
        flash('Address saved successfully!', 'success')
    return redirect(url_for('index'))

@app.context_processor
def inject_user_address():
    address = None
    if current_user.is_authenticated:
        address = Address.query.filter_by(user_id=current_user.id).first()
    return dict(address=address)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tc')
def tc():
    return render_template('tc.html')

@app.route('/privacyPolicy')
def privacyPolicy():
    return render_template('privacyPolicy.html')

@app.route('/exchangePolicy')
def exchangePolicy():
    return render_template('exchangePolicy.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/csr')
def csr():
    return render_template('csr.html')

@app.route('/basketball')
def basketball():
    return render_template('basketball.html', products=basketball_products)

@app.route('/football')
def football():
    return render_template('football.html', products=football_products)

@app.route('/cricket')
def cricket():
    return render_template('cricket.html', products=cricket_products)

@app.route('/volleyball')
def volleyball():
    return render_template('volleyball.html', products=volleyball_products)

@app.route('/badminton')
def badminton():
    return render_template('badminton.html', products=badminton_products)

@app.route('/tabletennis')
def tabletennis():
    return render_template('tabletennis.html', products=tabletennis_products)

@app.route('/hockey')
def hockey():
    return render_template('hockey.html', products=hockey_products)

@app.route('/trekking')
def trekking():
    return render_template('trekking.html', products=trekking_products)

# ------ ADMIN AUTHENTICATION & AUTHORIZATION -------

# Create a decorator function to restrict access to admin-only routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash('Admin access required', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the credentials match the admin credentials
        if email == 'admin@sportify.com' and password == 'admin123':
            session['admin_logged_in'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out successfully', 'info')
    return redirect(url_for('admin_login'))

# ------ ADMIN DASHBOARD & PRODUCT MANAGEMENT -------

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Getting all products from all categories
    products = {
        'basketball': basketball_products,
        'football': football_products,
        'cricket': cricket_products,
        'volleyball': volleyball_products,
        'badminton': badminton_products,
        'tabletennis': tabletennis_products,
        'hockey': hockey_products,
        'trekking': trekking_products
    }
    
    return render_template('admin_dashboard.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        category = request.form.get('category')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = int(request.form.get('stock'))
        image = request.form.get('image')
        
        # Geting the appropriate product list based on category
        product_list = get_product_list_by_category(category)
        
        if product_list is not None:
            # Find the highest ID across all products
            max_id = 0
            for product in all_products.values():
                if product['id'] > max_id:
                    max_id = product['id']
            
            # Creating new product with the next available ID
            new_product = {
                "id": max_id + 1,
                "image": image,
                "title": title,
                "description": description,
                "price": price + "/-",
                "stock": stock
            }
            
            # Adding the product to the appropriate category list
            product_list.append(new_product)
            # Also add to all_products dictionary
            all_products[new_product['id']] = new_product
            
            flash(f'Product "{title}" added to {category} category successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid category selected', 'danger')
    
    # GET request - render the add product form
    categories = [
        'basketball', 'football', 'cricket', 'volleyball',
        'badminton', 'tabletennis', 'hockey', 'trekking'
    ]
    return render_template('add_product.html', categories=categories)

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    # Finding the product in all_products
    product = all_products.get(product_id)
    
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    # Finding which category the product belongs to
    category = find_product_category(product_id)
    
    if request.method == 'POST':
        # Updating the product details
        product['title'] = request.form.get('title')
        product['description'] = request.form.get('description')
        product['price'] = request.form.get('price') + "/-"
        product['stock'] = int(request.form.get('stock'))
        product['image'] = request.form.get('image')
        
        flash(f'Product "{product["title"]}" updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # GET request - render the edit product form
    categories = [
        'basketball', 'football', 'cricket', 'volleyball',
        'badminton', 'tabletennis', 'hockey', 'trekking'
    ]
    
    # Removing the trailing "/- from price for the form
    form_price = product['price'].replace('/-', '')
    
    return render_template('edit_product.html', 
                          product=product, 
                          form_price=form_price,
                          category=category,
                          categories=categories)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    # Find which category the product belongs to
    category = find_product_category(product_id)
    
    if not category:
        flash('Product not found', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    # Get the product from all_products before deleting
    product = all_products.get(product_id)
    product_title = product['title'] if product else "Unknown product"
    
    # Get the appropriate product list based on category
    product_list = get_product_list_by_category(category)
    
    # Remove the product from the category list
    product_list[:] = [p for p in product_list if p['id'] != product_id]
    
    # Also remove from all_products dictionary
    if product_id in all_products:
        del all_products[product_id]
    
    flash(f'Product "{product_title}" removed successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Helper function to get the product list by category name
def get_product_list_by_category(category):
    category_map = {
        'basketball': basketball_products,
        'football': football_products,
        'cricket': cricket_products,
        'volleyball': volleyball_products,
        'badminton': badminton_products,
        'tabletennis': tabletennis_products,
        'hockey': hockey_products,
        'trekking': trekking_products
    }
    return category_map.get(category)

# Helper function to find which category a product belongs to
def find_product_category(product_id):
    category_map = {
        'basketball': basketball_products,
        'football': football_products,
        'cricket': cricket_products,
        'volleyball': volleyball_products,
        'badminton': badminton_products,
        'tabletennis': tabletennis_products,
        'hockey': hockey_products,
        'trekking': trekking_products
    }
    
    for category, products in category_map.items():
        if any(p['id'] == product_id for p in products):
            return category
    
    return None

#----PRODUCTS-------
basketball_products = [
    {"id": 1, "image": "static/images/basketball1.webp", "title": "Varsity Outdoor Basketball", "description": 'Official size and Weight: Size 7, 29.5"', "price": "1500/-", "stock": 15},
    {"id": 2, "image": "static/images/basketball2.webp", "title": "Tucana", "description": "Excellent stability and precision in every shot.", "price": "1200/-", "stock": 10},
    {"id": 3, "image": "static/images/basketball3.webp", "title": "Basketball Shoes", "description": "Size: 8-US, High-quality basketball shoes with excellent grip.", "price": "1600/-", "stock": 5},
    {"id": 4, "image": "static/images/basketball4.webp", "title": "Panther Basketball Jersey Set", "description": "Basketball Jersey Set, Size: XL", "price": "1000/-", "stock": 20}
]

football_products = [
    {"id": 5, "image": "static/images/football1.webp", "title": "Storm Football", "description": "Rubberized molded ball, designed for durability & performance.", "price": "749/-", "stock": 3},
    {"id": 6, "image": "static/images/football2.webp", "title": "Carbonite 7.0", "description": "High-quality football shoes with excellent grip. Size: 8-US", "price": "899/-", "stock": 5},
    {"id": 7, "image": "static/images/football3.webp", "title": "Astra-32", "description": "High-quality football with killer performance & grip.", "price": "1049/-", "stock": 15},
    {"id": 8, "image": "static/images/football4.webp", "title": "Safari Football Studs", "description": "Designed for superior speed, & control on the pitch, Size: 7-US", "price": "1399/-", "stock": 15}
]

cricket_products = [
    {"id": 9, "image": "static/images/cricket1.jpg", "title": "SS Willow Cricket Bat", "description": "High-quality cricket bat.", "price": "1500/-", "stock": 15},
    {"id": 10, "image": "static/images/cricket2.jpg", "title": "SS Sky Stunner Kashmir", "description": "Professional cricket bat.", "price": "800/-", "stock": 15},
    {"id": 11, "image": "static/images/cricket3.jpg", "title": "Cricket Pads", "description": "Protective cricket pads.", "price": "1200/-", "stock": 15},
    {"id": 12, "image": "static/images/cricket4.jpg", "title": "Cricket Helmet", "description": "Safety cricket helmet.", "price": "2000/-", "stock": 15}
]

volleyball_products = [
    {"id": 13, "image": "static/images/volleyball1.jpg", "title": "Volleyball", "description": "Professional volleyball.", "price": "900/-", "stock": 15},
    {"id": 14, "image": "static/images/volleyball2.jpg", "title": "Knee Pads", "description": "Volleyball knee pads.", "price": "500/-", "stock": 15},
    {"id": 15, "image": "static/images/volleyball3.jpg", "title": "Net Set", "description": "Volleyball net set.", "price": "1500/-", "stock": 15},
    {"id": 16, "image": "static/images/volleyball4.jpg", "title": "Sports Shoes", "description": "Volleyball shoes.", "price": "2000/-", "stock": 15}
]

badminton_products = [
    {"id": 17, "image": "static/images/badminton1.webp", "title": "Badminton Racket", "description": "Professional racket.", "price": "1200/-", "stock": 15},
    {"id": 18, "image": "static/images/badminton2.webp", "title": "Shuttlecocks", "description": "Pack of 6 shuttlecocks.", "price": "400/-", "stock": 15},
    {"id": 19, "image": "static/images/badminton3.jpg", "title": "Net Set", "description": "Badminton net set.", "price": "800/-", "stock": 15},
    {"id": 20, "image": "static/images/badminton4.avif", "title": "Sports Shoes", "description": "Badminton shoes.", "price": "1800/-", "stock": 15}
]

tabletennis_products = [
    {"id": 21, "image": "static/images/tt1.jpg", "title": "TT Bat", "description": "Professional table tennis racket.", "price": "1000/-", "stock": 15},
    {"id": 22, "image": "static/images/tt2.jpg", "title": "TT Balls", "description": "Pack of 6 balls.", "price": "300/-", "stock": 15},
    {"id": 23, "image": "static/images/tt3.jpg", "title": "Table Net", "description": "Table tennis net.", "price": "500/-", "stock": 15},
    {"id": 24, "image": "static/images/tt4.avif", "title": "TT Table", "description": "Professional table.", "price": "15000/-", "stock": 5}
]

hockey_products = [
    {"id": 25, "image": "static/images/hockey1.webp", "title": "Hockey Stick", "description": "Professional hockey stick.", "price": "1500/-", "stock": 15},
    {"id": 26, "image": "static/images/hockey2.jpg", "title": "Hockey Ball", "description": "Standard hockey ball.", "price": "400/-", "stock": 15},
    {"id": 27, "image": "static/images/hockey3.jpg", "title": "Shin Guard", "description": "Protective shin guards.", "price": "800/-", "stock": 15},
    {"id": 28, "image": "static/images/hockey4.webp", "title": "Goalkeeper Kit", "description": "Complete goalkeeper kit.", "price": "3000/-", "stock": 5}
]

trekking_products = [
    {"id": 29, "image": "static/images/trekking1.jpg", "title": "Trekking Bag", "description": "40L trekking backpack.", "price": "2500/-", "stock": 10},
    {"id": 30, "image": "static/images/trekking2.jpg", "title": "Trekking Shoes", "description": "Waterproof trekking shoes.", "price": "3000/-", "stock": 15},
    {"id": 31, "image": "static/images/trekking3.webp", "title": "Trekking Pole", "description": "Adjustable trekking pole.", "price": "1000/-", "stock": 20},
    {"id": 32, "image": "static/images/trekking4.jpg", "title": "Camping Tent", "description": "2-person camping tent.", "price": "4000/-", "stock": 8}
]

# Combine all products into one dictionary for easy lookup
all_products = {}
for product in (basketball_products + football_products + cricket_products + 
                volleyball_products + badminton_products + tabletennis_products + 
                hockey_products + trekking_products):
    all_products[product['id']] = product

#------ CART ------------

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = all_products.get(product_id)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(request.referrer or url_for('index'))
    
    # Check if product already in cart
    cart_item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=current_user.id,
            product_id=product_id,
            product_name=product['title'],
            product_price=float(product['price'].replace('/-', '')),
            quantity=1,
            image_url=product['image']
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', 'info')
        return redirect(url_for('index'))
    total = sum(item.product_price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = Cart.query.get_or_404(item_id)
    action = request.form.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            db.session.delete(cart_item)
    elif action == 'remove':
        db.session.delete(cart_item)
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('cart'))
    
    address = Address.query.filter_by(user_id=current_user.id).first()
    if not address:
        flash('Please add a shipping address before checkout!', 'warning')
    
    total = sum(item.product_price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    if not request.form:
        flash('Invalid form submission', 'error')
        return redirect(url_for('checkout'))

    # Verify cart is not empty
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('cart'))

    # Verify shipping address exists
    address = Address.query.filter_by(user_id=current_user.id).first()
    if not address:
        flash('Please add a shipping address before placing order!', 'error')
        return redirect(url_for('checkout'))

    payment_method = request.form.get('paymentMethod')
    
    if not payment_method:
        flash('Please select a payment method!', 'error')
        return redirect(url_for('checkout'))
    
    try:
        success_message = None

        total_amount = sum(item.product_price * item.quantity for item in cart_items)
        
        shipping_address = f"{address.house_street}, {address.landmark}, {address.pincode}, {address.state}"
        
        new_order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            payment_method=payment_method,
            shipping_address=shipping_address
        )
        db.session.add(new_order)
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order=new_order,
                product_name=cart_item.product_name,
                product_price=cart_item.product_price,
                quantity=cart_item.quantity,
                image_url=cart_item.image_url
            )
            db.session.add(order_item)
        
        if payment_method == 'card':
            required_fields = ['cardNumber', 'expiryDate', 'cvv', 'cardName']
            if not all(request.form.get(field) for field in required_fields):
                flash('Please fill in all card details!', 'error')
                return redirect(url_for('checkout'))
            success_message = 'Payment processed successfully!'
        
        elif payment_method == 'cod':
            success_message = 'Order placed successfully with Cash on Delivery!'
        
        elif payment_method == 'gift_card':
            if not request.form.get('giftCardNumber'):
                flash('Please enter gift card number!', 'error')
                return redirect(url_for('checkout'))
            success_message = 'Gift card payment processed successfully!'
        
        elif payment_method == 'coupon':
            if not request.form.get('couponCode'):
                flash('Please enter coupon code!', 'error')
                return redirect(url_for('checkout'))
            success_message = 'Coupon applied and payment processed successfully!'
        
        # Clear the cart after successful payment
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        

    

        if success_message:
            flash('Order placed successfully!', 'success')
            return redirect(url_for('order_history'))
        
        # Explicitly return a redirect response
        return redirect(url_for('index'))
    
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while processing your payment. Please try again.', 'error')
        return redirect(url_for('checkout'))
    

    

@app.route('/order_confirmation')
@login_required
def order_confirmation():
    return render_template('order_confirmation.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    search_results = []

    # Search through all products
    for product in all_products.values():
        if query in product['title'].lower() or query in product['description'].lower():
            search_results.append(product)

    return render_template('search_results.html', query=query, products=search_results)

@app.context_processor
def inject_cart_count():
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = Cart.query.filter_by(user_id=current_user.id).count()
    return dict(cart_count=cart_count)

@app.route('/animation')
def animation():
    return render_template('animation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)