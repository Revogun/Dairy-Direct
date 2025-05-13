from flask import Flask, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import RegistrationForm 

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///milkmarket.db'
db = SQLAlchemy(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # New category field
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Helper function for wrapping HTML
def wrap_html(body):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Milk Market</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Fredoka+One&display=swap">
        <style>
            :root {{
                --primary: #1e88e5;
                --primary-dark: #1565c0;
                --secondary: #8bc34a;
                --accent: #ffca28;
                --light-bg: #f5f9ff;
                --card-bg: #ffffff;
                --text-dark: #333333;
                --text-light: #ffffff;
                --border-radius: 12px;
                --shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }}
            
            body {{
                font-family: 'Poppins', sans-serif;
                background-color: var(--light-bg);
                background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="%23e3f2fd" opacity="0.4"/></svg>');
                background-size: 300px;
                color: var(--text-dark);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 900px;
                margin: 20px auto;
                padding: 30px;
                background: var(--card-bg);
                box-shadow: var(--shadow);
                border-radius: var(--border-radius);
                position: relative;
                overflow: hidden;
            }}
            
            .container::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                background: linear-gradient(90deg, var(--primary), var(--secondary));
            }}
            
            h1 {{
                font-family: 'Fredoka One', cursive;
                color: var(--primary);
                font-size: 2.5rem;
                margin-bottom: 30px;
                text-shadow: 2px 2px 0px rgba(0,0,0,0.1);
                position: relative;
                display: inline-block;
            }}
            
            h1::after {{
                content: '🐄';
                font-size: 1.8rem;
                position: absolute;
                right: -40px;
                top: 0;
            }}
            
            h2 {{
                color: var(--primary-dark);
                font-weight: 600;
                margin-top: 30px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px dashed var(--secondary);
            }}
            
            h3 {{ 
                color: var(--primary-dark);
                font-weight: 500;
            }}
            
            input, select {{
                width: 100%;
                padding: 12px 15px;
                margin: 10px 0;
                border-radius: var(--border-radius);
                border: 2px solid #e0e0e0;
                font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }}
            
            input:focus, select:focus {{
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2);
            }}
            
            button {{
                background: var(--primary);
                color: var(--text-light);
                border: none;
                padding: 12px 20px;
                border-radius: var(--border-radius);
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
                margin-top: 15px;
                font-family: 'Poppins', sans-serif;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            button:hover {{
                background: var(--primary-dark);
                transform: translateY(-2px);
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
            }}
            
            a {{
                color: var(--primary);
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s ease;
            }}
            
            a:hover {{
                color: var(--primary-dark);
                text-decoration: underline;
            }}
            
            ul {{
                list-style: none;
                padding: 0;
                margin: 20px 0;
            }}
            
            li {{
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: var(--border-radius);
                border-left: 4px solid var(--secondary);
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            li:hover {{
                transform: translateX(5px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            
            .nav-links {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 20px 0;
            }}
            
            .nav-links a {{
                background-color: var(--secondary);
                color: var(--text-light);
                padding: 10px 20px;
                border-radius: 30px;
                font-weight: 600;
            }}
            
            .nav-links a:hover {{
                background-color: #7cb342;
                text-decoration: none;
                transform: scale(1.05);
            }}
            
            .product-category {{
                display: inline-block;
                background-color: var(--accent);
                color: var(--text-dark);
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-right: 10px;
            }}
            
            .action-link {{
                background-color: var(--primary);
                color: var(--text-light);
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.8rem;
                text-decoration: none;
            }}
            
            .action-link:hover {{
                background-color: var(--primary-dark);
                text-decoration: none;
            }}
            
            .delete-link {{
                background-color: #f44336;
            }}
            
            .delete-link:hover {{
                background-color: #d32f2f;
            }}
            
            .form-group {{
                margin-bottom: 15px;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                    margin: 10px;
                }}
                
                h1 {{
                    font-size: 2rem;
                }}
                
                li {{
                    flex-direction: column;
                    align-items: flex-start;
                }}
                
                .action-link {{
                    margin-top: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Diary Direct</h1>
            {body}
        </div>
    </body>
    </html>
    """

@app.route('/')
def home():
    return wrap_html("""
        <h2>Welcome to Diary Direct</h2>
        <p>Your one-stop platform for dairy products</p>
        <div class="nav-links">
            <a href='/register'>Register</a>
            <a href='/login'>Login</a>
        </div>
    """)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            role=form.user_type.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect('/login')

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect('/dashboard')

    return wrap_html("""
        <h2>Login</h2>
        <form method='POST'>
            <div class="form-group">
                <input type='text' name='username' placeholder='Username' required>
            </div>
            <div class="form-group">
                <input type='password' name='password' placeholder='Password' required>
            </div>
            <button type='submit'>Login</button>
        </form>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    role = session['role']
    user_id = session['user_id']

    if role == 'farmer':
        products = Product.query.filter_by(farmer_id=user_id).all()
        product_list = ''.join([
            f"""<li>
                <div>
                    <span class="product-category">{p.category}</span>
                    <strong>{p.name}</strong> - {p.quantity}L @ ${p.price}
                </div>
                <a href='/delete_product/{p.id}' class='action-link delete-link'>Delete</a>
            </li>""" for p in products
        ])
        
        return wrap_html(f"""
            <h2>Farmer Dashboard</h2>
            <div class="nav-links">
        <a href='/logout'>Logout</a>
    </div>
            <form method='POST' action='/add_product'>
                <div class="form-group">
                    <input type='text' name='name' placeholder='Product Name' required>
                </div>
                <div class="form-group">
                    <input type='text' name='category' placeholder='Category (Milk, Butter, Cheese)' required>
                </div>
                <div class="form-group">
                    <input type='number' name='quantity' placeholder='Quantity' required>
                </div>
                <div class="form-group">
                    <input type='number' step='0.01' name='price' placeholder='Price' required>
                </div>
                <button type='submit'>Add Product</button>
            </form>
            <h3>Your Products</h3>
            <ul>{product_list}</ul>
        """)

    else:
        products = Product.query.all()
        product_list = ''.join([
            f"""<li>
                <div>
                    <span class="product-category">{p.category}</span>
                    <strong>{p.name}</strong> - {p.quantity}L @ ${p.price}
                </div>
                <a href='/contact/{p.farmer_id}' class='action-link'>Contact Farmer</a>
            </li>""" for p in products
        ])
        
        return wrap_html(f"""
            <h2>Entrepreneur Dashboard</h2>
            <div class="nav-links">
        <a href='/logout'>Logout</a>
    </div>
            <h3>Available Products</h3>
            <ul>{product_list}</ul>
        """)

@app.route('/add_product', methods=['POST'])
def add_product():
    product = Product(
        name=request.form['name'],
        category=request.form['category'],
        quantity=request.form['quantity'],
        price=request.form['price'],
        farmer_id=session['user_id']
    )
    db.session.add(product)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/contact/<int:farmer_id>')
def contact_farmer(farmer_id):
    farmer = User.query.get_or_404(farmer_id)
    return wrap_html(f"""
        <h2>Contact {farmer.username}</h2>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: left;">
            <p><strong>Email:</strong> {farmer.email}</p>
            <p><strong>Phone:</strong> {farmer.phone}</p>
        </div>
        <div style="margin-top: 20px;">
            <a href="/dashboard" class="action-link">Back to Dashboard</a>
        </div>
    """)
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
