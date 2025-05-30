from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, User, Parking_Lot, Parking_Spot, Reserved
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = 'rakshanaa_mad'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EasyPark.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = request.form.get['address']
        pincode = request.form.get['pincode']
        phoneno = request.form['phoneno']
        role = request.form.get('role','user')
        
        if(confirm_password != password):
            flash('Passwords do not match')

        new_user = User(fullname = fullname,
                    email = email,
                    password = generate_password_hash(password),
                    address = address,
                    pincode = pincode,
                    phoneno = phoneno,
                    role = role)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login','success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful!','success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

def initialize_admin():
    with app.app_context():
        if not User.query.filter_by(role='admin').first():
            admin = User(fullname = 'Sathivika',
                         email = 'sathivika_admin@gmail.com',
                         password = generate_password_hash('admin'),
                         address = '1st Cross Street Nugambakkam',
                         pincode = '600026',
                         phoneno = '9884705410',
                         role = 'admin')
            db.session.add(admin)
            db.session.commit()

@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    initialize_admin()
    app.run(debug=True)