from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user


local_server= True
app = Flask(__name__)
app.secret_key='hetroadmin'


login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/Hetro_pd'
db=SQLAlchemy(app)




class pests_d(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)



class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50)) 
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))
    uid = db.Column(db.Integer)
    phone = db.Column(db.String(20))  
    hiredate = db.Column(db.Date)  



class Register(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    active = db.Column(db.String(100)) 
    uid = db.Column(db.Integer)
    phonenumber = db.Column(db.String(20)) 
    address = db.Column(db.String(100)) 
    dateofjoind = db.Column(db.DateTime) 
    lastname = db.Column(db.String(50))  
    password = db.Column(db.String(1000)) 

class Horticulturepests(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CommonName = db.Column(db.String(255))
    ScientificName = db.Column(db.String(255))
    PresenceInNZ = db.Column(db.Boolean)
    PrimaryImageURL = db.Column(db.String(255))
    KeyCharacteristics = db.Column(db.Text)
    BiologyDescription = db.Column(db.Text)
    Impacts = db.Column(db.Text)


    

@app.route('/')
def index():
    uids = [user.uid for user in User.query.all()]  
    return render_template('index.html', current_user=current_user, uids=uids)

@app.route('/index_hetro')
def index_hetro():
    # Get the email from the session
    email = session.get('email')

    
    if email:
        registers = Register.query.filter_by(email=email).all()
        uids = [register.uid for register in registers]
        return render_template('index.html', registers=registers, uids=uids)
    else:
       
        flash('Please login first.', 'error')
        return redirect(url_for('loginh'))

@app.route('/all_pests')
def display_all_pests():
 
    all_pests = Horticulturepests.query.all()

    return render_template('all_pests.html', pests=all_pests)

@app.route('/loginh')
def loginh():
 
    return render_template('loginh.html')



@app.route('/view_pests')
def display_pest_details():
    pest_id = request.args.get('pest_id')  

    
    try:
        pest_id = int(pest_id)
    except (TypeError, ValueError):
        
        return "Invalid pest ID"

  
    pest = Horticulturepests.query.get_or_404(pest_id)

    return render_template('view_pests.html', pest=pest)


@app.route('/addpests', methods=['GET', 'POST'])
def add_pest():
    if request.method == 'POST':
        common_name = request.form['common_name']
        scientific_name = request.form['scientific_name']
        presence_in_nz = True if request.form.get('presence_in_nz') == 'on' else False
        primary_image_url = request.form['primary_image_url']
        key_characteristics = request.form['key_characteristics']
        biology_description = request.form['biology_description']
        impacts = request.form['impacts']

        new_pest = Horticulturepests(
            CommonName=common_name,
            ScientificName=scientific_name,
            PresenceInNZ=presence_in_nz,
            PrimaryImageURL=primary_image_url,
            KeyCharacteristics=key_characteristics,
            BiologyDescription=biology_description,
            Impacts=impacts,
        )

        db.session.add(new_pest)
        db.session.commit()

        flash('New pest added successfully!', 'success')
        return redirect(url_for('show_pests'))

    return render_template('addpests.html')


@app.route('/edit_pest/<int:pest_id>', methods=['GET', 'POST'])
def edit_pest(pest_id):
    pest = Horticulturepests.query.get_or_404(pest_id)

    if request.method == 'POST':
        pest.CommonName = request.form['common_name']
        pest.ScientificName = request.form['scientific_name']
        pest.PresenceInNZ = True if request.form.get('presence_in_nz') == 'on' else False
        pest.PrimaryImageURL = request.form['primary_image_url']
        pest.KeyCharacteristics = request.form['key_characteristics']
        pest.BiologyDescription = request.form['biology_description']
        pest.Impacts = request.form['impacts']

        db.session.commit()
        flash('Pest updated successfully!', 'success')
        return redirect(url_for('show_pests'))

    return render_template('edit_pests.html', pest=pest)

@app.route('/delete_pest/<int:pest_id>',methods=['POST','GET'])
def delete_pest(pest_id):
    pest = Horticulturepests.query.get_or_404(pest_id)
    db.session.delete(pest)
    db.session.commit()
    flash('Pest deleted successfully!', 'success')
    return redirect(url_for('show_pests'))


@app.route('/pests')
def show_pests():
    pests = Horticulturepests.query.all()
    return render_template('pests.html', pests=pests)

@app.route('/staffdetails')
@login_required
def staff_details():
    users = User.query.all()  
    return render_template('staff.html', user_entry=users)


@app.route('/hetroistdetail')
@login_required
def hetroistdetail():
    query=Register.query.all()
    uids = [user.uid for user in User.query.all()]  
    return render_template('hetroistdetail.html',query=query ,  id=id)

@app.route('/agroproducts')
def agroproducts():
    query=pests_d.query.all()
    return render_template('agroproducts.html',query=query)

@app.route('/addagroproduct',methods=['POST','GET'])
@login_required
def addagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        products=pests_d(username=username,email=email,productname=productname,productdesc=productdesc,price=price)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addagroproducts.html')

@app.route('/triggers')
@login_required
def triggers():
    
    query=Trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/addfarming',methods=['POST','GET'])
@login_required
def addfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farming')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist","warning")
            return redirect('/addfarming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Addes","success")
    return render_template('farming.html')




@app.route("/delete/<string:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
    post=Register.query.filter_by(rid=rid).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/hetroistdetail')

from flask import request, render_template, redirect, flash
from main import app, db, User
from flask_login import current_user


@app.route('/edit_profile/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_profile(id):
    if request.method == "POST":
        firstname = request.form.get('firstname')
        email = request.form.get('email')
        password = request.form.get('password')
        uid = request.form.get('uid')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        hiredate = request.form.get('hiredate')

        user_entry = User.query.get(id) 
        if user_entry:
            user_entry.firstname = firstname
            user_entry.email = email
            user_entry.password = password
            user_entry.uid = uid
            user_entry.lastname = lastname
            user_entry.phone = phone
            user_entry.hiredate = hiredate

            db.session.commit()
            flash("Profile Updated", "success")
            return redirect('/') 
        else:
            flash("User profile not found", "error")

 
    user_entry = User.query.get(id)

    return render_template('/edit_profile.html', user_entry=user_entry)


@app.route('/edit/<int:rid>', methods=['POST', 'GET'])
def edit(rid):
    if request.method == "POST":
    
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        active = request.form.get('active')
        phonenumber = request.form.get('phonenumber')
        address = request.form.get('address')
        datejoined = request.form.get('datejoined')

        active = True if active == '1' else False

       
        posts = Register.query.get(rid)
        posts.firstname = firstname
        posts.lastname = lastname
        posts.email = email
        posts.active = active
        posts.phonenumber = phonenumber
        posts.address = address
        posts.datejoined = datejoined

        db.session.commit()
        flash(" details updated successfully", "success")
        return redirect('/hetroistdetail')

   
    posts = Register.query.get(rid)
    return render_template('/edit.html', posts=posts)

   
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
      
        newuser=User(username=username,email=email,password=password)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","warning")
            return render_template('login.html')    

    return render_template('login.html')


from flask import redirect, url_for, flash

from flask import session

@app.route('/login_hetro', methods=['POST'])
def login_hetro():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Register.query.filter_by(email=email).first()

        if user and user.password == password:
            flash('Login successful!', 'success')
            session['email'] = email 
            return redirect(url_for('index_hetro'))  
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('loginh'))



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    if request.method == "POST":
        # Fetching form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        active = request.form.get('active')
        phonenumber = request.form.get('phonenumber')
        address = request.form.get('address')
        datejoined = request.form.get('datejoined')
        password = request.form.get('password')  # Corrected variable name

        # Converting 'active' to boolean
        active = True if active == '1' else False

        # Creating a new Register object
        new_hetroist = Register(
            firstname=firstname,
            lastname=lastname,
            email=email,
            active=active,
            phonenumber=phonenumber,
            address=address,
            dateofjoind=datejoined,  # Corrected variable name
            password=password
        )

        # Adding and committing to the database
        db.session.add(new_hetroist)
        db.session.commit()

        flash("Your record has been saved successfully", "success")
        return redirect('/hetroistdetail')

    # If method is not POST, render the registration form
    return render_template('hetroist.html')

@app.route('/register_hetro', methods=['POST', 'GET'])
def register_hetro():
    if request.method == "POST":
        # Fetching form data
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        active = request.form.get('active')
        phonenumber = request.form.get('phonenumber')
        address = request.form.get('address')
        datejoined = request.form.get('datejoined')
        password = request.form.get('password')  # Corrected variable name

        # Converting 'active' to boolean
        active = True if active == '1' else False

        # Creating a new Register object
        new_hetroist = Register(
            firstname=firstname,
            lastname=lastname,
            email=email,
            active=active,
            phonenumber=phonenumber,
            address=address,
            dateofjoind=datejoined,  # Corrected variable name
            password=password
        )

        # Adding and committing to the database
        db.session.add(new_hetroist)
        db.session.commit()

        flash("Your record has been saved successfully", "success")
        return redirect('/loginh')

    # If method is not POST, render the registration form
    return render_template('signup.html')

@app.route('/save_profile/<int:id>', methods=['POST'])
@login_required
def save_profile(id):
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        uid = request.form.get('uid')


        user_entry = User.query.get(id)

        if user_entry:
        
            user_entry.username = username
            user_entry.email = email
            user_entry.password = password
            user_entry.uid = uid

            db.session.commit()

            flash("Profile Updated", "success")
        else:
           
            flash("User profile not found", "error")

  
    return redirect('/hetroistdetail')

@app.route('/addstaff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
     
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        uid = 2
        phone = request.form.get('phone')
        hiredate = request.form.get('hiredate')

  
        new_user = User(firstname=firstname, lastname=lastname, email=email, password=password,
                        uid=uid, phone=phone, hiredate=hiredate)

        db.session.add(new_user)
        db.session.commit()

 
        flash('Staff added successfully!', 'success')

     
        return redirect('/staffdetails')


    return render_template('addstaff.html')

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    
