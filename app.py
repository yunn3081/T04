from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
from export_db import get_data

app = Flask(__name__)
getdata = get_data()

#ENV = 'prod'
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/cellline'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bgbfkkhaaxvsqz:4651cb865eab9a07557a214fe78c5828f68f1bc240dfdc3d79972722a927f2f5@ec2-3-231-69-204.compute-1.amazonaws.com:5432/dfhrugeougj002'
    #app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class acc_information(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    pwd = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __init__(self, customer, email, pwd, location):
        self.customer = customer
        self.email = email
        self.pwd = pwd
        self.location = location

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/index')
def index():
    return render_template('index.html') 

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/about_whoWeAre')
def about_whoWeAre():
    return render_template('about_whoWeAre.html')

@app.route('/about_whatWeDo')
def about_whatWeDo():
    return render_template('about_whatWeDo.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product_submit', methods=['POST'])
def product_submit():
    if request.method == 'POST':
        Product_Category = request.form['Product Category']
        Age = request.form['Age']
        Gender = request.form['Gender']
        Ethnicity = request.form['Ethnicity']
        Cancer_type = request.form['Cancer type']
        Growth_Properties = request.form['Growth Properties']
        filter_list = [Product_Category, Age, Gender, Ethnicity, Cancer_type, Growth_Properties]
        #print(type(Product_Category), Age, Gender, Ethnicity, Cancer_type, Growth_Properties)
        return render_template('showup_cellline.html', showupcellline = getdata, myfilter = filter_list)

@app.route('/showup_cellline')
def showup_cellline():
    return render_template('showup_cellline.html')

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/others')
def others():
    return render_template('others.html') 

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        pwd = request.form['pwd']
        location = request.form['location']
        #print(customer, email, pwd, location)
        #return render_template('success.html')
        
        if customer == '' or email == '' or pwd == '' or location == '':
           return render_template('index.html', message = 'Please enter required fields')
        
        if db.session.query(acc_information).filter(acc_information.customer == customer).count() == 0:
            data = acc_information(customer, email, pwd, location)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, email, location)
            return render_template('success.html')

        return render_template('index.html', message = 'This email address have already registered.')

if __name__ == '__main__':
    app.run()