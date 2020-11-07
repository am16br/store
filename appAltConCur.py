
from flask import *
import flask_login
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length
from werkzeug.datastructures import CombinedMultiDict, ImmutableOrderedMultiDict
import sqlite3          #libraries
from datetime import date,datetime
from werkzeug.utils import secure_filename
import os
import shutil
import glob

import base64

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'wxyzthisisAsecretqbf'
app.config['ENV'] = True
app.config['UPLOAD_FOLDER'] = "static/images/"


products = []   #dictionary so each has an ID
srvs = []       #dict
ords = []       #dict?
subs = []
messages = []

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'test@gmail.com': {'password': 'pw123'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

#forms
class SubscriberForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])

class ContactForm(FlaskForm):
    fname = StringField('c_f_name', validators=[InputRequired()])
    lname = StringField('c_l_name', validators=[InputRequired()])
    email = StringField('c_email', validators=[InputRequired()])
    subject = StringField('c_subject', validators=[InputRequired()])
    message = TextAreaField('c_message', validators=[InputRequired()])

class CouponCodeForm(FlaskForm):
    code = StringField('code', validators=[InputRequired()])

class CheckoutForm(FlaskForm):
    fname = StringField('f_name', validators=[InputRequired()])
    lname = StringField('l_name', validators=[InputRequired()])
    cname = StringField('c_name', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])
    apt = StringField('apt', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    zip = StringField('zip', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    notes = StringField('notes', validators=[InputRequired()])


#bck end forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username Required')])
    password = PasswordField('Password', validators=[InputRequired()])

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    price = DecimalField('Price', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    small = IntegerField('Number of Small', validators=[InputRequired()])
    medium = IntegerField('Number of Medium', validators=[InputRequired()])
    large = IntegerField('Number of Large', validators=[InputRequired()])
    xl = IntegerField('Number of XL', validators=[InputRequired()])
    type = StringField('Type', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired()])

class ServicesForm(FlaskForm):
    sname = StringField('Name', validators=[InputRequired()])
    sprice = DecimalField('Price', validators=[InputRequired()])
    stime = StringField('Time', validators=[InputRequired()])
    sdescription = TextAreaField('Description', validators=[InputRequired()])
    stype = StringField('Type', validators=[InputRequired()])
    sphoto = FileField('Photo', validators=[FileRequired()])

class ArtistForm(FlaskForm):
    artistname = StringField('Artist Name', validators=[InputRequired()])
    artistemail = StringField('Artist Email', validators=[InputRequired()])
    artistbio = TextAreaField('Artist Biography', validators=[InputRequired()])
    artistimage = FileField('Primary Image', validators=[FileRequired()])
    artistimage2 = FileField('Secondary Image or Video', validators=[FileRequired()])

class PlaylistForm(FlaskForm):
    playlistname = StringField('Playlist Name', validators=[InputRequired()])
    playlistlink = StringField('Playlist Link', validators=[InputRequired()])
    playlistimage = FileField('Image', validators=[FileRequired()])

class WatchForm(FlaskForm):
    addname = StringField('Name', validators=[InputRequired()])
    addtype = StringField('Type (Music Video, Podcast, Skit, Ad)', validators=[InputRequired()])
    addlink = StringField('Link', validators=[InputRequired()])
    addfile = FileField('File', validators=[FileRequired()])

class RemoveForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])

class EditForm(FlaskForm):
    ename = StringField('Name', validators=[InputRequired()])
    eemail = StringField('CompanyEmail', validators=[InputRequired()])
    eaddress = StringField('CompanyAddress', validators=[InputRequired()])
    ephone = StringField('CompanyPhone', validators=[InputRequired()])
    eabout = TextAreaField('CompanyAbout', validators=[InputRequired()])

class EditHome(FlaskForm):
    card1Title = StringField('Card 1 Title', validators=[InputRequired()])
    card1Tagline = StringField('Card 1 Tagline', validators=[InputRequired()])
    card1Price = StringField('Card 1 Price', validators=[InputRequired()])
    card1Link = StringField('Card 1 Link', validators=[InputRequired()])
    card1Photo = FileField('Card 1 Photo', validators=[FileRequired()])
    card2Hashtag = StringField('Card 2 Hashtag', validators=[InputRequired()])
    card2Title = StringField('Card 2 Title', validators=[InputRequired()])
    card2Link = StringField('Card 2 Link', validators=[InputRequired()])
    card2Photo = FileField('Card 2 Photo', validators=[FileRequired()])
    card3Hashtag = StringField('Card 3 Hashtag', validators=[InputRequired()])
    card3Title = StringField('Card 3 Title', validators=[InputRequired()])
    card3Link = StringField('Card 3 Link', validators=[InputRequired()])
    card3Photo = FileField('Card 3 Photo', validators=[FileRequired()])


class EditAbout(FlaskForm):
    aboutPar = StringField('About Paragraph', validators=[InputRequired()])
    title = StringField('Title ex How We Started', validators=[InputRequired()])
    cardPar = StringField('Card Paragraph', validators=[InputRequired()])
    cardPhoto = FileField('Card Photo', validators=[FileRequired()])
    team1Name = StringField('Team Member 1 Name', validators=[InputRequired()])
    team1Position = StringField('Team Member 1 Position', validators=[InputRequired()])
    team1About = StringField('Team Member 1 About', validators=[InputRequired()])
    team1Photo = FileField('Team 1 Photo', validators=[FileRequired()])
    team2Name = StringField('Team Member 2 Name', validators=[InputRequired()])
    team2Position = StringField('Team Member 2 Position', validators=[InputRequired()])
    team2About = StringField('Team Member 2 About', validators=[InputRequired()])
    team2Photo = FileField('Team 2 Photo', validators=[FileRequired()])
    team3Name = StringField('Team Member 3 Name', validators=[InputRequired()])
    team3Position = StringField('Team Member 3 Position', validators=[InputRequired()])
    team3About = StringField('Team Member 3 About', validators=[InputRequired()])
    team3Photo = FileField('Team 3 Photo', validators=[FileRequired()])
    team4Name = StringField('Team Member 4 Name', validators=[InputRequired()])
    team4Position = StringField('Team Member 4 Position', validators=[InputRequired()])
    team4About = StringField('Team Member 4 About', validators=[InputRequired()])
    team4Photo = FileField('Team 4 Photo', validators=[FileRequired()])


#classes

class Message():
    def __init__(self,fname,lname,cemail,csubject,cmessage):
        self.f = fname
        self.l = lname
        self.e = cemail
        self.s = csubject
        self.m = cmessage

class Cart():
    def __init__(self,id):  #id for session or user
        self.id = id
        self.cart = []
        self.items = 0
        self.total = 0
    def addToCart(self, obj):
        self.cart.append(obj)
        self.items = self.items + 1
        self.total = self.total + obj.p


class Artist():
    def __init__(self,name,location,biography,links,posts):
        self.n = name
        self.l = location
        self.b = biography
    def add_post(self, post):
        self.posts.append(post)

def visits():
    con = sqlite3.connect('products.db')                   #connecting to/creating/opening database
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    #dropTable(cur,"Visitors")
    createTable(cur,"Visitors","Date TEXT,Sessions INTEGER")
    cur.execute("SELECT count(*) FROM Visitors")
    count=cur.fetchone()[0]
    if count == 0:
        cur.execute("""INSERT INTO Visitors (Date,Sessions) VALUES (?,?)""",(str(date.today()),session.get('visits')))
        con.commit()
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
        cur.execute("SELECT * FROM Visitors")
        for row in cur:
            if row[0] > str(date.today()):
                session['visits'] = 1
                cur.execute("""INSERT INTO Visitors (Date,Sessions) VALUES (?,?)""",(str(date.today()),session.get('visits')))
            else:
                cur.execute("""UPDATE Visitors SET Sessions=? WHERE Date=?""",(session.get('visits'),str(date.today())))
            con.commit()
    else:
        session['visits'] = 1 # setting session data
    return session.get('visits')

def cartSum():
    rows = selectAll("Cart")
    if len(rows) == 0:
        return 0
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    cur.execute("SELECT SUM(Quantity) FROM Cart")
    return cur.fetchone()[0]

def editinfo():
    rows = selectAll("SiteInfo")
    if len(rows) == 0:
        return "Name", "Email", "Address", "Phone Number", "About"
    else:
        con = sqlite3.connect('products.db')
        cur = con.cursor()
        name = selectOne(cur,"Name","SiteInfo")
        email = selectOne(cur,"Email","SiteInfo")
        address = selectOne(cur,"Address","SiteInfo")
        phonenumber = selectOne(cur,"PhoneNumber","SiteInfo")
        about = selectOne(cur,"About","SiteInfo")
    return name,email,address,phonenumber,about

def homeinfo():
    rows = selectAll("EditHome")
    if len(rows) == 0:  #add images
        return "card1Title", "card1Tagline", "card1Link","card1Image", "card2Hashtag","card2Title", "card2Link","card2image","card3Hashtag","card3Title","card3Link","card3image"
    else:
        con = sqlite3.connect('products.db')
        cur = con.cursor()
        c1ti = selectOne(cur,"Card1Title","EditHome")
        c1ta = selectOne(cur,"Card1Tagline","EditHome")
        c1p = selectOne(cur,"Card1Price","EditHome")
        c1l = selectOne(cur,"Card1Link","EditHome")
        dst1 = selectOne(cur,"Card1Photo","EditHome")
        c2h = selectOne(cur,"Card2Hashtag","EditHome")
        c2t = selectOne(cur,"Card2Title","EditHome")
        c2l = selectOne(cur,"Card2Link","EditHome")
        dst2 = selectOne(cur,"Card2Photo","EditHome")
        c3h = selectOne(cur,"Card3Hashtag","EditHome")
        c3t = selectOne(cur,"Card3Title","EditHome")
        c3l = selectOne(cur,"Card3Link","EditHome")
        dst3 = selectOne(cur,"Card3Photo","EditHome")
    return c1ti,c1ta,c1p,c1l,dst1,c2h,c2t,c2l,dst2,c3h,c3t,c3l,dst3

def aboutinfo():
    rows = selectAll("EditAbout")
    if len(rows) == 0:  #add images
        return "About Paragraph", "Title, ex. How We Started", "Card Paragraph", "Team1Name","Team1Position", "Team1About","Team2Name","Team2Position", "Team2About","Team3Name","Team3Position", "Team3About","Team4Name","Team4Position", "Team4About"
    else:
        con = sqlite3.connect('products.db')
        cur = con.cursor()
        aP = selectOne(cur,"aboutPar","EditAbout")
        t = selectOne(cur,"Title","EditAbout")
        c1p = selectOne(cur,"cardPar","EditAbout")
        dst = selectOne(cur,"cardPhoto","EditAbout")
        t1n = selectOne(cur,"Team1Name","EditAbout")
        t1p = selectOne(cur,"Team1Position","EditAbout")
        t1a = selectOne(cur,"Team1About","EditAbout")
        dst1 = selectOne(cur,"Team1Photo","EditAbout")
        t2n = selectOne(cur,"Team2Name","EditAbout")
        t2p = selectOne(cur,"Team2Position","EditAbout")
        t2a = selectOne(cur,"Team2About","EditAbout")
        dst2 = selectOne(cur,"Team2Photo","EditAbout")
        t3n = selectOne(cur,"Team3Name","EditAbout")
        t3p = selectOne(cur,"Team3Position","EditAbout")
        t3a = selectOne(cur,"Team3About","EditAbout")
        dst3 = selectOne(cur,"Team3Photo","EditAbout")
        t4n = selectOne(cur,"Team4Name","EditAbout")
        t4p = selectOne(cur,"Team4Position","EditAbout")
        t4a = selectOne(cur,"Team4About","EditAbout")
        dst4 = selectOne(cur,"Team4Photo","EditAbout")
    return aP,t,c1p,dst,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4

def createTable(cur,table,fields):
    temp = "CREATE TABLE IF NOT EXISTS "+table+" ("+fields+");"
    cur.execute(temp)
    return

def dropTable(cur,table):
    temp = "DROP TABLE IF EXISTS "+table
    cur.execute(temp)
    return

def selectOne(cur,field,table):
    temp = "SELECT "+field+" FROM "+table
    cur.execute(temp)
    return cur.fetchone()[0]

def selectOneWhere(cur,field,table,field2,option):
    temp = "SELECT "+field+" FROM "+table+" WHERE "+field2+" = ?"
    cur.execute(temp,(option,))
    return cur.fetchone()[0]

def selectAll(table):
    con = sqlite3.connect('products.db')                   #connecting to/creating/opening database
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    temp = "SELECT * FROM "+table
    cur.execute(temp)
    return cur.fetchall()

def selectAllWhere(cur,table,field,option):
    temp = "SELECT * FROM "+table+" WHERE "+field+" = ?"
    cur.execute(temp,(option,))
    return cur.fetchall()

def insert(cur,table,values,tuple):
    spots = ""
    for x in range(len(tuple)-1):
        spots = spots + "?,"
    spots = spots + "?"
    temp = "INSERT INTO "+table+" ("+values+") VALUES ("+spots+");"
    cur.execute(temp, tuple)
    return

def removeitem(cur,table,field,option):
    temp = 'SELECT EXISTS(SELECT 1 FROM '+table+' WHERE '+field+'=?);'
    cur.execute(temp,(option,))
    if (cur.fetchone()[0]==1):
        temp = 'DELETE FROM '+table+' WHERE '+field+' = ?;'
        cur.execute(temp,(option,))
        return True

@app.route('/', methods = ['POST', 'GET'])
def home():
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    c1ti,c1ta,c1p,c1l,dst1,c2h,c2t,c2l,dst2,c3h,c3t,c3l,dst3=homeinfo()
    rows = selectAll("Products")
    rows2 = selectAll("Services")
    if request.method == 'POST':
        prod = request.form['product']
        return redirect(url_for('shopsingle', prod=prod))
    return render_template("index.html",cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about, rows=rows, rows2=rows2, subsciber_form=subsciber_form,c1ti=c1ti,c1ta=c1ta,c1p=c1p,c1l=c1l,dst1=dst1,c2h=c2h,c2t=c2t,c2l=c2l,dst2=dst2,c3h=c3h,c3t=c3t,c3l=c3l,dst3=dst3)

@app.route('/index.html', methods = ['POST', 'GET'])
def index():
    return redirect(url_for('home'))

@app.route('/listen.html', methods = ['POST', 'GET'])
def listen():
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    con = sqlite3.connect('products.db')                   #connecting to/creating/opening database
    cur = con.cursor()
    artistname = selectOne(cur,"Name","Artists")
    artistimage = selectOne(cur,"Image","Artists")
    rows = selectAll("Playlists")
    rows2 = selectAll("Artists")
    if request.method == 'POST':
        art = request.form['artist']
        return redirect(url_for('artist',art=art))
    return render_template('listen.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about, rows=rows, rows2=rows2, subsciber_form=subsciber_form,artistname=artistname,artistimage=artistimage)

@app.route('/<art>', methods = ['POST', 'GET'])
def artist(art=None):
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    con = sqlite3.connect('products.db')                   #connecting to/creating/opening database
    cur = con.cursor()                              #setting cursor
    artistname = art
    artistbio = selectOneWhere(cur,"Biography","Artists","Name",art)
    artistimage = selectOneWhere(cur,"Image","Artists","Name",art)
    artistimage2 = selectOneWhere(cur,"Image2","Artists","Name",art)
    return render_template('artist.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about, subsciber_form=subsciber_form, artistname=artistname,artistbio=artistbio,artistimage=artistimage,artistimage2=artistimage2)

@app.route('/watch.html', methods = ['POST', 'GET'])
def watch():
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    con = sqlite3.connect('products.db')                   #connecting to/creating/opening database
    con.row_factory = sqlite3.Row
    cur = con.cursor()                              #setting cursor
    rows = selectAllWhere(cur,"Watch","Type","Music Video")
    rows2 = selectAllWhere(cur,"Watch","Type","Skit")
    rows3 = selectAllWhere(cur,"Watch","Type","Ad")
    rows4 = selectAllWhere(cur,"Watch","Type","Podcast")
    return render_template('watch.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about, subsciber_form=subsciber_form, rows=rows,rows2=rows2,rows3=rows3,rows4=rows4)

@app.route('/about.html',methods = ['POST', 'GET'])
def about():
   subsciber_form = SubscriberForm()
   cart = cartSum()
   name,email,address,phonenumber,about=editinfo()
   aP,t,c1p,dst,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4=aboutinfo()
   if subsciber_form.validate_on_submit():
       subs.append(subsciber_form.email.data)
   return render_template('about.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,aP=aP,t=t,c1p=c1p,dst=dst,t1n=t1n,t1p=t1p,t1a=t1a,dst1=dst1,t2n=t2n,t2p=t2p,t2a=t2a,dst2=dst2,t3n=t3n,t3p=t3p,t3a=t3a,dst3=dst3,t4n=t4n,t4p=t4p,t4a=t4a,dst4=dst4,subsciber_form=subsciber_form)

@app.route('/subscribed.html',methods = ['POST', 'GET'])
def subscribed():
   subsciber_form = SubscriberForm()
   cart = cartSum()
   name,email,address,phonenumber,about=editinfo()
   if subsciber_form.validate_on_submit():
       subs.append(subsciber_form.email.data)
   return render_template('subscribed.html',cart=cart,name=name, email=email,address=address,phonenumber=phonenumber,about=about,)

@app.route('/contact.html',methods = ['POST', 'GET'])
def contact():
    contact_form = ContactForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    if contact_form.validate_on_submit():
        msg = Message(contact_form.fname.data,contact_form.lname.data,contact_form.email.data,contact_form.subject.data,contact_form.message.data)
        messages.append(msg)
        return redirect(url_for('home'))   #returning to homepage after adding data
    return render_template("contact.html", cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,contact_form=contact_form)


@app.route('/shop.html',methods = ['POST', 'GET'])
def shop():
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    rows = selectAll("Products")
    if request.method == 'POST':
        prod = request.form['product']
        return redirect(url_for('shopsingle', prod=prod))
    return render_template('shop.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,rows=rows, subsciber_form=subsciber_form)

@app.route('/shopservices.html',methods = ['POST', 'GET'])
def shopservices():
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    rows = selectAll("Services")
    if request.method == 'POST':
        prod = request.form['product']
        return redirect(url_for('shopsingle', prod=prod))
    return render_template('shopservices.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,rows=rows, subsciber_form=subsciber_form)

@app.route('/<prod>.html',methods = ['POST', 'GET'])
def shopsingle(prod=None):    #get name, price, pricture, descritption, or row number and get from directory
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    options = []
    cur.execute("SELECT EXISTS(SELECT 1 FROM Products WHERE Name=?)",(prod,))
    flag= (cur.fetchone()[0])
    if flag == 1:
        price = selectOneWhere(cur,"Price","Products","Name",prod)
        description = selectOneWhere(cur,"Description","Products","Name",prod)
        dst = selectOneWhere(cur,"Image","Products","Name",prod)
        op = selectOneWhere(cur,"Small","Products","Name",prod)
        if op > 0:
            options.append('Small')
        op = selectOneWhere(cur,"Medium","Products","Name",prod)
        if op > 0:
            options.append('Medium')
        op = selectOneWhere(cur,"Large","Products","Name",prod)
        if op > 0:
            options.append('Large')
        op = selectOneWhere(cur,"XL","Products","Name",prod)
        if op > 0:
            options.append('XL')
    else:
        price = selectOneWhere(cur,"Price","Services","Name",prod)
        description = selectOneWhere(cur,"Description","Services","Name",prod)
        dst = selectOneWhere(cur,"Image","Services","Name",prod)
    if request.method == 'POST':
        option = request.form['option']
        quantity = int(request.form['qty'])
        total=price*quantity
        price = format(price, '.2f')
        cur.execute("SELECT * FROM Cart")
        rows = cur.fetchall()
        if cartSum() == 0:
            item = 1
        else:
            item = cartSum() + 1
        try:
            with sqlite3.connect("products.db") as con:
              cur = con.cursor()
              insert(cur,"Cart","ItemNum,Name,Price,Size,Quantity,Total,Image",(item,prod,price,option,quantity,total,dst))
              con.commit()
        except:
           con.rollback()
        finally:
            con.close()
            return redirect(url_for('cart'))
    price = format(price, '.2f')
    return render_template('shop-single.html',prod=prod,cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,subsciber_form=subsciber_form, price=price, description=description, image=dst, options=options)


@app.route('/cart.html',methods = ['POST', 'GET'])
def cart():
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    rows = selectAll("Cart")
    if len(rows) == 0:
        sub = 0
    else:
        cur.execute("SELECT SUM(Total) FROM Cart")
        sub = float(cur.fetchone()[0])
    if request.method == 'POST':
        item = request.form['remove']
        cur.execute('DELETE FROM Cart WHERE ItemNum = ?;',(item,))
        con.commit()
        cart = cartSum()
        rows = selectAll("Cart")
        if len(rows) == 0:
            sub = 0
        else:
            cur.execute("SELECT SUM(Total) FROM Cart")
            sub = float(cur.fetchone()[0])
        ship = 5
        total = round(sub * 1.07,2)
        sub = format(sub, '.2f')
        total = format(total, '.2f')
        return render_template('cart.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,subsciber_form=subsciber_form, rows=rows, subtotal=sub, total=total)
    ship = 5
    total = round(sub * 1.07,2)
    sub = format(sub, '.2f')
    total = format(total, '.2f')
    return render_template('cart.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,subsciber_form=subsciber_form,rows=rows, subtotal=sub, total=total)

@app.route('/checkout.html',methods = ['POST', 'GET'])
def checkout():
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    subsciber_form = SubscriberForm()
    coupon_form = CouponCodeForm()
    cart = cartSum()
    name,email,address,phonenumber,about=editinfo()
    rows = selectAll("Cart")
    cur.execute("SELECT SUM(Total) FROM Cart")
    sub = (cur.fetchone()[0])
    ship = 5
    total = round(sub * 1.07,2)
    sub = format(sub, '.2f')
    total = format(total, '.2f')
    if request.method == 'POST':
        country = request.form['c_country']
        fname = request.form['c_fname']
        lname = request.form['c_lname']
        company = request.form['c_companyname']
        address = request.form['c_address']
        state = request.form['c_state']
        zip = request.form['c_postal_zip']
        email = request.form['c_email_address']
        phone = request.form['c_phone']

        acttPW = request.form['c_account_password']

        shipfname = request.form['c_diff_fname']
        shiplname = request.form['c_diff_lname']
        shipcompany = request.form['c_diff_companyname']
        shipaddress = request.form['c_diff_address']
        shipstate = request.form['c_diff_state']
        shipzip = request.form['c_diff_postal_zip']
        shipemail = request.form['c_diff_email_address']
        shipphone = request.form['c_diff_phone']

        notes = request.form['c_order_notes']

        return redirect(url_for('thankyou'))
    return render_template('checkout.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,subsciber_form=subsciber_form,rows=rows, subtotal=sub, total=total)

@app.route('/thankyou.html',methods = ['POST', 'GET'])
def thankyou():
   subsciber_form = SubscriberForm()
   name,email,address,phonenumber,about=editinfo()
   con = sqlite3.connect('products.db')
   cur = con.cursor()
   dropTable(cur,"Cart")
   createTable(cur,"Cart","ItemNum INTEGER,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")
   cart = cartSum()
   return render_template('thankyou.html',cart=cart, name=name, email=email,address=address,phonenumber=phonenumber,about=about,subsciber_form=subsciber_form)


#back-end   (ADMIN)
@app.route('/login',methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == users[form.username.data]['password']:
            user = User()
            user.id = form.username.data
            flask_login.login_user(user)
            return(redirect(url_for('adminhome')))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/adminhome',methods = ['POST', 'GET'])
@flask_login.login_required
def adminhome():
    labels=[]
    values=[]
    max = 0
    sessions = visits() #add to eveyr page?
    rows = selectAll("Visitors")
    for row in rows:
        labels.append(row[0])
        values.append(row[1])
        if row[1] > max:
            max = row[1]
    max = max * 1.125
    return render_template('adminhome.html',sessions=sessions,labels=labels, values=values, max=max)

@app.route('/edit', methods = ['POST', 'GET'])
@flask_login.login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        ename = form.ename.data
        eemail = form.eemail.data
        eaddress = form.eaddress.data
        ephone = form.ephone.data
        eabout = form.eabout.data

        with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              dropTable(cur,"SiteInfo")
              createTable(cur,"SiteInfo","Name TEXT,Email TEXT,Address TEXT,PhoneNumber TEXT,About TEXT")
              insert(cur,"SiteInfo","Name, Email, Address, PhoneNumber, About",(ename,eemail, eaddress, ephone, eabout))
              con.commit()    #committing executions to connected database
        con.close()
        return redirect(url_for('home'))

    return render_template("edit.html", form=form)

@app.route('/edithome', methods = ['POST', 'GET'])
@flask_login.login_required
def edithome():
    form = EditHome()
    if form.validate_on_submit():
        c1ti = form.card1Title.data
        c1ta = form.card1Tagline.data
        c1p = form.card1Price.data
        c1l = form.card1Link.data
        filename = secure_filename(form.card1Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.card1Photo.data.save(file_path)
        dst1 = "static/images/"+filename
        c2h = form.card2Hashtag.data
        c2t = form.card2Title.data
        c2l = form.card2Link.data
        filename = secure_filename(form.card2Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.card2Photo.data.save(file_path)
        dst2 = "static/images/"+filename
        c3h = form.card3Hashtag.data
        c3t = form.card3Title.data
        c3l = form.card3Link.data
        filename = secure_filename(form.card3Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.card3Photo.data.save(file_path)
        dst3 = "static/images/"+filename

        with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              dropTable(cur,"EditHome")
              createTable(cur,"EditHome","Card1Title TEXT,Card1Tagline TEXT,Card1Price TEXT,Card1Link TEXT,Card1Photo BLOB,Card2Hashtag TEXT,Card2Title TEXT,Card2Link TEXT,Card2Photo BLOB,Card3Hashtag TEXT,Card3Title TEXT,Card3Link TEXT,Card3Photo BLOB")
              insert(cur,"EditHome","Card1Title, Card1Tagline, Card1Price, Card1Link, Card1Photo, Card2Hashtag,Card2Title,Card2Link,Card2Photo,Card3Hashtag,Card3Title,Card3Link,Card3Photo",(c1ti,c1ta,c1p,c1l,dst1, c2h,c2t,c2l,dst2, c3h,c3t,c3l,dst3))
              con.commit()
        con.close()
        return redirect(url_for('home'))
    return render_template("edithome.html", form=form)

@app.route('/editabout', methods = ['POST', 'GET'])
@flask_login.login_required
def editabout():
    form = EditAbout()
    if form.validate_on_submit():
        about = form.aboutPar.data
        title = form.title.data
        c1p = form.cardPar.data
        filename = secure_filename(form.cardPhoto.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.cardPhoto.data.save(file_path)
        dst = "static/images/"+filename
        t1n = form.team1Name.data
        t1p = form.team1Position.data
        t1a = form.team1About.data
        filename = secure_filename(form.team1Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.team1Photo.data.save(file_path)
        dst1 = "static/images/"+filename
        t2n = form.team2Name.data
        t2p = form.team2Position.data
        t2a = form.team2About.data
        filename = secure_filename(form.team2Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.team2Photo.data.save(file_path)
        dst2 = "static/images/"+filename
        t3n = form.team1Name.data
        t3p = form.team3Position.data
        t3a = form.team3About.data
        filename = secure_filename(form.team3Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.team3Photo.data.save(file_path)
        dst3 = "static/images/"+filename
        t4n = form.team1Name.data
        t4p = form.team4Position.data
        t4a = form.team4About.data
        filename = secure_filename(form.team4Photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.team4Photo.data.save(file_path)
        dst4 = "static/images/"+filename


        with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              dropTable(cur,"EditAbout")
              createTable(cur,"EditAbout","aboutPar TEXT,Title TEXT,cardPar TEXT,cardPhoto BLOB,Team1Name TEXT,Team1Position TEXT,Team1About TEXT,Team1Photo BLOB,Team2Name TEXT,Team2Position TEXT,Team2About TEXT,Team2Photo BLOB,Team3Name TEXT,Team3Position TEXT,Team3About TEXT,Team3Photo BLOB,Team4Name TEXT,Team4Position TEXT,Team4About TEXT,Team4Photo BLOB")
              insert(cur,"EditAbout","aboutPar, Title, cardPar,cardPhoto,Team1Name,Team1Position, Team1About,Team1Photo, Team2Name,Team2Position,Team2About,Team2Photo,Team3Name,Team3Position,Team3About,Team3Photo,Team4Name,Team4Position,Team4About,Team4Photo",(about,title,c1p,dst,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4))
              con.commit()
        con.close()
        return redirect(url_for('about'))

    return render_template("editabout.html", form=form)

@app.route('/addartist', methods = ['POST', 'GET'])
@flask_login.login_required
def addartist():
    form = ArtistForm()
    form2=RemoveForm()
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    createTable(cur,"Artists","Name TEXT,Email TEXT,Biography TEXT,Image BLOB,Image2 BLOB")
    rows = selectAll("Artists")
    con.close()
    if form.validate_on_submit():
        an = form.artistname.data
        ae = form.artistemail.data
        ab = form.artistbio.data
        filename = secure_filename(form.artistimage.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.artistimage.data.save(file_path)
        ai = "static/images/"+filename
        filename = secure_filename(form.artistimage2.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.artistimage2.data.save(file_path)
        ai2 = "static/images/"+filename
        with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              insert(cur,"Artists","Name, Email, Biography, Image, Image2",(an,ae, ab, ai, ai2))
              con.commit()    #committing executions to connected database
        rows = selectAll("Artists")
        con.close()
        return render_template("addartist.html", form=form,form2=form2,rows=rows)
    return render_template("addartist.html", form=form,form2=form2,rows=rows)

@app.route('/addplaylist', methods = ['POST', 'GET'])
@flask_login.login_required
def addplaylist():
    form = PlaylistForm()
    form2=RemoveForm()
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    createTable(cur,"Playlists","Name TEXT,Link TEXT,Image BLOB")
    rows = selectAll("Playlists")
    con.close()
    if form.validate_on_submit():
        pn = form.playlistname.data
        pl = form.playlistlink.data
        filename = secure_filename(form.playlistimage.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.playlistimage.data.save(file_path)
        pi = "static/images/"+filename

        with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              insert(cur,"Playlists","Name, Link, Image",(pn,pl, pi))
              con.commit()
        rows = selectAll("Playlists")
        con.close()
        return render_template("addplaylist.html", form=form,form2=form2,rows=rows)
    return render_template("addplaylist.html", form=form,form2=form2,rows=rows)

@app.route('/addwatch', methods = ['POST', 'GET'])
@flask_login.login_required
def addwatch():
    form = WatchForm()
    form2=RemoveForm()
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    createTable(cur,"Watch","Name TEXT,Type TEXT,Link TEXT,Image BLOB")
    rows = selectAll("Watch")
    con.close()
    if form.validate_on_submit():
        n = form.addname.data
        t = form.addtype.data
        l = form.addlink.data
        filename = secure_filename(form.addfile.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.addfile.data.save(file_path)
        f = "static/images/"+filename

        with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              insert(cur,"Watch","Name, Type, Link, Image",(n,t,l,f))
              con.commit()
        rows = selectAll("Watch")
        con.close()
        return render_template("addwatch.html", form=form,form2=form2,rows=rows)
    return render_template("addwatch.html", form=form,form2=form2,rows=rows)

@app.route('/add', methods = ['POST', 'GET'])
@flask_login.login_required
def add():
    form = ProductForm()
    form2 = RemoveForm()
    rows = selectAll("Products")
    if form.validate_on_submit():
        name = form.name.data
        price = float(form.price.data)
        description = form.description.data
        small = int(form.small.data)
        medium = int(form.medium.data)
        large = int(form.large.data)
        xl = int(form.xl.data)
        type = form.type.data
        filename = secure_filename(form.photo.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.photo.data.save(file_path)
        dst = "static/images/"+filename
        try:
           with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              insert(cur,"Products","Name, Price, Description, Small, Medium, Large, XL, Type, Image",(name,price, description, small, medium, large, xl, type, dst))
              con.commit()
        except:
           con.rollback()     #rollback for errors
        finally:
            rows = selectAll("Playlists")
            con.close()
            return render_template("add.html", form=form, form2=form2, rows=rows)   #returning to homepage after adding data
    return render_template("add.html", form=form, form2=form2, rows=rows)

@app.route('/remove', methods = ['POST', 'GET'])
@flask_login.login_required
def remove():
    form = ProductForm()
    form2 = RemoveForm()
    if form2.validate_on_submit():
        name = form2.name.data
        con = sqlite3.connect('products.db')
        cur = con.cursor()
        if removeitem(cur,"Products","Name",name):
            con.commit()
            con.close()
            return redirect(url_for('add'))
        if removeitem(cur,"Services","Name",name):
            con.commit()
            con.close()
            return redirect(url_for('services'))
        if removeitem(cur,"Artists","Name",name):
            con.commit()
            con.close()
            return redirect(url_for('addartist'))
        if removeitem(cur,"Watch","Name",name):
            con.commit()
            con.close()
            return redirect(url_for('addwatch'))
        if removeitem(cur,"Playlist","Name",name):
            con.commit()
            con.close()
            return redirect(url_for('addplaylist'))
        return redirect(url_for('add'))
    return redirect(url_for('add'))


@app.route('/services', methods = ['POST', 'GET'])
@flask_login.login_required
def services():
    form = ServicesForm()
    form2 = RemoveForm()
    rows = selectAll("Services")
    if form.validate_on_submit():
        name = form.sname.data
        price = float(form.sprice.data)
        time = form.stime.data
        description = form.sdescription.data
        type = form.stype.data
        filename = secure_filename(form.sphoto.data.filename)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.sphoto.data.save(file_path)
        dst = "static/images/"+filename
        try:
           with sqlite3.connect("products.db") as con:  #connecting database
              cur = con.cursor()
              insert(cur,"Services","Name, Price, Time, Description, Type, Image",(name,price,time,description,type,dst))
              con.commit()
        except:
           con.rollback()     #rollback for errors
        finally:
            rows = selectAll("Services")
            con.close()
            return render_template("services.html", form=form,form2=form2,rows=rows)
    return render_template("services.html", form=form,form2=form2,rows=rows)

@app.route('/orders', methods = ['POST', 'GET'])
@flask_login.login_required
def orders():
    return render_template("orders.html", ords=ords)

@app.route('/subscribers', methods = ['POST', 'GET'])
@flask_login.login_required
def subscribers():
    return render_template("subscribers.html", subs=subs)

@app.route('/contactList', methods = ['POST', 'GET'])
@flask_login.login_required
def contactList():
    return render_template("contactList.html", messages=messages)

@app.route('/logout', methods = ['POST', 'GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':  #function for if this were main

   app.run(debug = True)    #run application
