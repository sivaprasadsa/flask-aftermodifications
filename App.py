from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
app = Flask(__name__)

app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database table name data
class Data(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    lastname =db.Column(db.String(100))
    home =db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    createdOn = db.Column(db.DateTime)
    updatedOn = db.Column(db.DateTime)
    placeid = db.Column(db.Integer)
    def __init__(self, name, lastname, home, email, phone,created,updatedOn,placeid):

        self.name = name
        self.lastname = lastname
        self.home = home
        self.email = email
        self.phone = phone
        self.createdOn=created
        self.placeid=placeid
#table name place
class Places(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    placename = db.Column(db.String(100))

def place_query():
    return Places.query       

#error pages
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
#500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
#502
@app.errorhandler(502)
def internal_error(error):
    db.session.rollback()
    return render_template('502.html'), 502
#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    try:
        all_data = Data.query.all()
        place= Places.query.all()
        data =dict()
        data['employees'] = all_data
        data['places']= place
        return render_template("index.html", data = data)
    except Exception as e:
	     return render_template("404.html")
#route to place page
@app.route('/place')
def Place():
    try:
        all_places = Places.query.all()
        data= all_places
    #return render_template("places.html",placelist=all_places)
        return render_template("places.html",data=data)
    except Exception as e:
	     return render_template("404.html")
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])

#method to insert place details to data table
def insert():
    try:
        if request.method == 'POST':
            name = request.form['name']
            lastname= request.form['lastname']
            home = request.form['home']
            email = request.form['email']
            phone = request.form['phone']
            today = date.today()
            created =today
            updated =''
        
        placename= Places.query.get(home)
        my_data = Data(name, lastname, placename.placename, email, phone, created,updated,placename.id)
        db.session.add(my_data)
        db.session.commit()
        flash("Employee Inserted Successfully")
        #return render_template('index.html')
        return redirect('/')
    except Exception as e:
	     return render_template("404.html")
#add places method
@app.route('/insertplace', methods = ['POST'])
def insertplace():
    try:
        if request.method == 'POST':
            #import pdb;pdb.set_trace()
            placename = request.form['placename']        
            my_place = Places()
            my_place.placename=placename
            db.session.add(my_place)
            db.session.commit()        
            flash("Place Inserted Successfully")
            return redirect(url_for('Place'))
    except Exception as e:
	     return render_template("404.html")

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
#update method
def update():
    try:
        if request.method == 'POST':   
            my_data = Data.query.get(request.form.get('id'))
            my_data.name = request.form['name']
            my_data.lastname = request.form['lastname']
            my_data.home = request.form['home']
            my_data.email = request.form['email']
            my_data.phone = request.form['phone']
            today = date.today()
            my_data.updatedOn= today
            db.session.commit()
            flash("Employee Updated Successfully")
            return redirect(url_for('Index'))
    except Exception as e:
	     return render_template("404.html")

#This route is for deleting  employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    try:
        my_data = Data.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Employee Deleted Successfully")
        return redirect(url_for('Index'))
    except Exception as e:
	     return render_template("404.html")
#delete place method
@app.route('/deleteplace/<id>/', methods = ['GET', 'POST'])
#function
def deleteplace(id):
    try:
        my_data = Places.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Place Deleted Successfully")
        return redirect(url_for('Index'))
    except Exception as e:
	     return render_template("404.html")
#search employee
@app.route('/search',methods=['GET','POST'])
def search():
    try:
        form=request.form
        search_key =form['key']
        my_Data="%{0}%".format(search_key)
        my_data = Data.query.filter(Data.name.like(my_Data)).all()
        place= Places.query.all()
        data =dict()
        data['employees'] = my_data
        data['places']= place
        return render_template("index.html", data = data)
    except Exception as e:
	     return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)