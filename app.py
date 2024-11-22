from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

from models import Customer, Manufacturer, Solution, Component

@app.route('/')
def home():
    customers_count = Customer.query.count()
    manufacturers_count = Manufacturer.query.count()
    solutions_count = Solution.query.count()
    components_count = Component.query.count()
    return render_template('dashboard.html', customers_count=customers_count, manufacturers_count=manufacturers_count, solutions_count=solutions_count, components_count=components_count)

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        # Process the form data and add the customer to the database
        if 'name' in request.form:
            customer = Customer(name=request.form['name'])
            db.session.add(customer)
            db.session.commit()
        return redirect(url_for('customers'))
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/manufacturers', methods=['GET', 'POST'])
def manufacturers():
    if request.method == 'POST':
        # Process the form data and add the manufacturer to the database
        if 'name' and 'customer_id' in request.form:
            manufacturer = Manufacturer(name=request.form['name'], customer_id=request.form['customer_id'])
            db.session.add(manufacturer)
            db.session.commit()
        return redirect(url_for('manufacturers'))
    manufacturers = Manufacturer.query.all()
    return render_template('manufacturers.html', manufacturers=manufacturers, customers=Customer.query.all())

@app.route('/solutions', methods=['GET', 'POST'])
def solutions():
    if request.method == 'POST':
        # Process the form data and add the solution to the database
        if 'name' in request.form:
            solution = Solution(name=request.form['name'], manufacturer_id=request.form['manufacturer_id'])
            db.session.add(solution)
            db.session.commit()
        return redirect(url_for('solutions'))
    solutions = Solution.query.all()
    return render_template('solutions.html', solutions=solutions, manufacturers=Manufacturer.query.all())

@app.route('/components', methods=['GET', 'POST'])
def components():
    if request.method == 'POST':
        # Process the form data and add the component to the database
        if 'name' in request.form:
            component = Component(name=request.form['name'], solution_id=request.form['solution_id'])
            db.session.add(component)
            db.session.commit()
        return redirect(url_for('components'))
    components = Component.query.all()
    return render_template('components.html', components=components, solutions=Solution.query.all())

@app.route('/templates', methods=['GET'])
def index():
    return render_template('templates.html')