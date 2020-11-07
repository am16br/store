
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
#from model import *

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'wxyzthisisAsecretqbf'
app.config['ENV'] = True
app.config['UPLOAD_FOLDER'] = "static/images/"

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

class MenuForm(FlaskForm):
    label = StringField('Label', validators=[InputRequired()])
    link = StringField('Link', validators=[InputRequired()])

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
    ebackground = StringField('BackgroundColor', validators=[InputRequired()])
    etextcolor = StringField('TextColor', validators=[InputRequired()])

class EditHome(FlaskForm):
    card1Title = StringField('Card 1 Title', validators=[InputRequired()])
    card1Tagline = StringField('Card 1 Tagline', validators=[InputRequired()])
    card1Price = StringField('Card 1 Price', validators=[InputRequired()])
    card1Link = StringField('Card 1 Link', validators=[InputRequired()])
    card1Photo = FileField('Card 1 Photo', validators=[FileRequired()])
    card1background = StringField('Card 1 Background Color', validators=[InputRequired()])
    card1textcolor = StringField('Card 1 Text Color', validators=[InputRequired()])
    card2Hashtag = StringField('Card 2 Hashtag', validators=[InputRequired()])
    card2Title = StringField('Card 2 Title', validators=[InputRequired()])
    card2Link = StringField('Card 2 Link', validators=[InputRequired()])
    card2Photo = FileField('Card 2 Photo', validators=[FileRequired()])
    card2background = StringField('Card 2 Background Color', validators=[InputRequired()])
    card2textcolor = StringField('Card 2 Text Color', validators=[InputRequired()])
    card3Hashtag = StringField('Card 3 Hashtag', validators=[InputRequired()])
    card3Title = StringField('Card 3 Title', validators=[InputRequired()])
    card3Link = StringField('Card 3 Link', validators=[InputRequired()])
    card3Photo = FileField('Card 3 Photo', validators=[FileRequired()])
    card3background = StringField('Card 3 Background Color', validators=[InputRequired()])
    card3textcolor = StringField('Card 3 Text Color', validators=[InputRequired()])


class EditAbout(FlaskForm):
    aboutPar = StringField('About Paragraph', validators=[InputRequired()])
    title = StringField('Title ex How We Started', validators=[InputRequired()])
    cardPar = StringField('Card Paragraph', validators=[InputRequired()])
    cardPhoto = FileField('Card Photo', validators=[FileRequired()])
    background = StringField('Background Color', validators=[InputRequired()])
    textcolor = StringField('Text Color', validators=[InputRequired()])
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


def visits():
    #dropTable("Visitors")
    createTable("Visitors","Date TEXT,Sessions INTEGER")
    count = selectOne("count(*)","Visitors")
    if count == 0:
        insert("Visitors","Date,Sessions",(str(date.today()),session.get('visits')))
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
        if exists("Visitors","Sessions",str(date.today())) == 0:
            update("Sessions","Visitors","Date", session.get('visits'),str(date.today()))
        else:
            session['visits'] = 1
            insert("Visitors","Date,Sessions",(str(date.today()),session.get('visits')))
    else:
        session['visits'] = 1 # setting session data
    return session.get('visits')

def cartSum():
    visits()
    #dropTable("Cart")
    createTable("Cart","Session TEXT,ItemNum TEXT,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")

    if exists("Cart","Session",session['visits']) == 1:
        return selectOneWhere("SUM(Quantity)","Cart","Session",session['visits'])
    return 0

def editinfo():
    rows = selectAll("SiteInfo")
    if len(rows) == 0:
        return "Name", "Email", "Address", "Phone Number", "About","white","black"
    else:
        name = selectOne("Name","SiteInfo")
        email = selectOne("Email","SiteInfo")
        address = selectOne("Address","SiteInfo")
        phonenumber = selectOne("PhoneNumber","SiteInfo")
        about = selectOne("About","SiteInfo")
        background = selectOne("BackgroundColor","SiteInfo")
        text = selectOne("TextColor","SiteInfo")
    return name,email,address,phonenumber,about,background,text

def homeinfo():
    rows = selectAll("EditHome")
    if len(rows) == 0:  #add images
        return "card1Title", "card1Tagline", "20","card1Link","card1Image","white","black", "card2Hashtag","card2Title", "card2Link","card2image","white","black","card3Hashtag","card3Title","card3Link","card3image","white","black"
    else:
        c1ti = selectOne("Card1Title","EditHome")
        c1ta = selectOne("Card1Tagline","EditHome")
        c1p = selectOne("Card1Price","EditHome")
        c1l = selectOne("Card1Link","EditHome")
        dst1 = selectOne("Card1Photo","EditHome")
        c1bc = selectOne("Card1BackgroundColor","EditHome")
        c1tc = selectOne("Card1TextColor","EditHome")
        c2h = selectOne("Card2Hashtag","EditHome")
        c2t = selectOne("Card2Title","EditHome")
        c2l = selectOne("Card2Link","EditHome")
        dst2 = selectOne("Card2Photo","EditHome")
        c2bc = selectOne("Card2BackgroundColor","EditHome")
        c2tc = selectOne("Card2TextColor","EditHome")
        c3h = selectOne("Card3Hashtag","EditHome")
        c3t = selectOne("Card3Title","EditHome")
        c3l = selectOne("Card3Link","EditHome")
        dst3 = selectOne("Card3Photo","EditHome")
        c3bc = selectOne("Card3BackgroundColor","EditHome")
        c3tc = selectOne("Card3TextColor","EditHome")
    return c1ti,c1ta,c1p,c1l,dst1,c1bc,c1tc,c2h,c2t,c2l,dst2,c2bc,c2tc,c3h,c3t,c3l,dst3,c3bc,c3tc

def aboutinfo():
    rows = selectAll("EditAbout")
    if len(rows) == 0:  #add images
        return "About Paragraph", "Title, ex. How We Started", "Card Paragraph","cardphoto","white","black", "Team1Name","Team1Position", "Team1About","Team1Image","Team2Name","Team2Position", "Team2About","Team2Image","Team3Name","Team3Position", "Team3About","Team3Image","Team4Name","Team4Position", "Team4About","Team4Image"
    else:
        aP = selectOne("aboutPar","EditAbout")
        t = selectOne("Title","EditAbout")
        c1p = selectOne("cardPar","EditAbout")
        dst = selectOne("cardPhoto","EditAbout")
        c1bc = selectOne("BackgroundColor","EditAbout")
        c1tc = selectOne("TextColor","EditAbout")
        t1n = selectOne("Team1Name","EditAbout")
        t1p = selectOne("Team1Position","EditAbout")
        t1a = selectOne("Team1About","EditAbout")
        dst1 = selectOne("Team1Photo","EditAbout")
        t2n = selectOne("Team2Name","EditAbout")
        t2p = selectOne("Team2Position","EditAbout")
        t2a = selectOne("Team2About","EditAbout")
        dst2 = selectOne("Team2Photo","EditAbout")
        t3n = selectOne("Team3Name","EditAbout")
        t3p = selectOne("Team3Position","EditAbout")
        t3a = selectOne("Team3About","EditAbout")
        dst3 = selectOne("Team3Photo","EditAbout")
        t4n = selectOne("Team4Name","EditAbout")
        t4p = selectOne("Team4Position","EditAbout")
        t4a = selectOne("Team4About","EditAbout")
        dst4 = selectOne("Team4Photo","EditAbout")
    return aP,t,c1p,dst,c1bc,c1tc,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4

def createTable(table,fields):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "CREATE TABLE IF NOT EXISTS "+table+" ("+fields+");"
    cur.execute(temp)
    con.commit()
    con.close()
    return

def dropTable(table):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "DROP TABLE IF EXISTS "+table
    cur.execute(temp)
    con.commit()
    con.close()
    return

def selectOne(field,table):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "SELECT "+field+" FROM "+table
    cur.execute(temp)
    ret = cur.fetchone()[0]
    con.close()
    return ret

def selectOneWhere(field,table,field2,option):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = "SELECT "+field+" FROM "+table+" WHERE "+field2+" = ?"
    if field == "EXISTS(SELECT 1":
        temp = temp+")"
    cur.execute(temp,(option,))
    ret = cur.fetchone()[0]
    con.close()
    return ret

def selectDistinct(field,table):
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    temp = "SELECT DISTINCT "+field+" FROM "+table
    cur.execute(temp)
    ret = cur.fetchall()
    con.close()
    return ret

def selectAll(table):
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    temp = "SELECT * FROM "+table
    cur.execute(temp)
    ret = cur.fetchall()
    con.close()
    return ret

def selectAllWhere(table,field,option):
    con = sqlite3.connect('products.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    temp = "SELECT * FROM "+table+" WHERE "+field+" = ?"
    cur.execute(temp,(option,))
    ret = cur.fetchall()
    con.close()
    return ret

def insert(table,values,tuple):
    spots = ""
    for x in range(len(tuple)-1):
        spots = spots + "?,"
    spots = spots + "?"
    try:
       with sqlite3.connect("products.db") as con:
          cur = con.cursor()
          temp = "INSERT INTO "+table+" ("+values+") VALUES ("+spots+");"
          cur.execute(temp, tuple)
          con.commit()
    except:
       con.rollback()
    finally:
        con.close()
    return

def exists(table,field,option):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = 'SELECT EXISTS(SELECT 1 FROM '+table+' WHERE '+field+'=?);'
    cur.execute(temp,(option,))
    ret = cur.fetchone()[0]
    con.close()
    return ret

def removeitem(table,field,option):
    if (exists(table,field,option)==1):
        con = sqlite3.connect('products.db')
        cur = con.cursor()
        temp = 'DELETE FROM '+table+' WHERE '+field+' = ?;'
        cur.execute(temp,(option,))
        con.commit()
        con.close()
        return True
    return

def update(field,table,field2,option1,option2):
    con = sqlite3.connect('products.db')
    cur = con.cursor()
    temp = 'UPDATE '+table+' SET '+field+'=? WHERE '+field2+' = ?;'
    cur.execute(temp,(option1,option2))
    con.commit()
    con.close()
    return

def uploadImage(file):
    filename = secure_filename(file.data.filename)
    file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.data.save(file_path)
    return "static/images/"+filename

createTable("SiteInfo","Name TEXT,Email TEXT,Address TEXT,PhoneNumber TEXT,About TEXT,BackgroundColor TEXT,TextColor TEXT")
createTable("EditHome","Card1Title TEXT,Card1Tagline TEXT,Card1Price TEXT,Card1Link TEXT,Card1Photo BLOB,Card1BackgroundColor TEXT,Card1TextColor TEXT,Card2Hashtag TEXT,Card2Title TEXT,Card2Link TEXT,Card2Photo BLOB,Card2BackgroundColor TEXT,Card2TextColor TEXT,Card3Hashtag TEXT,Card3Title TEXT,Card3Link TEXT,Card3Photo BLOB,Card3BackgroundColor TEXT,Card3TextColor TEXT")
createTable("EditAbout","aboutPar TEXT,Title TEXT,cardPar TEXT,cardPhoto BLOB,BackgroundColor TEXT,TextColor TEXT,Team1Name TEXT,Team1Position TEXT,Team1About TEXT,Team1Photo BLOB,Team2Name TEXT,Team2Position TEXT,Team2About TEXT,Team2Photo BLOB,Team3Name TEXT,Team3Position TEXT,Team3About TEXT,Team3Photo BLOB,Team4Name TEXT,Team4Position TEXT,Team4About TEXT,Team4Photo BLOB")

createTable("Products","Name TEXT,Price REAL,Description TEXT,Small INTEGER,Medium INTEGER,Large INTEGER,XL INTEGER,Type TEXT,Image BLOB")
createTable("Services","Name TEXT,Price REAL,Time TEXT,Description TEXT,Type TEXT,Image BLOB")
createTable("Cart","Session TEXT,ItemNum TEXT,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")

createTable("Watch","Name TEXT,Type TEXT,Link TEXT,Image BLOB")
createTable("Playlists","Name TEXT,Link TEXT,Image BLOB")
createTable("Artists","Name TEXT,Email TEXT,Biography TEXT,Image BLOB,Image2 BLOB")

createTable("Subscribers","Email TEXT")
createTable("Contact","FName TEXT,LName TEXT,Email TEXT,Subject TEXT,Message TEXT")
createTable("Orders","FName TEXT,LName TEXT,Address TEXT,State TEXT,Zip TEXT,ProductsOption TEXT")

def header(backgroundcolor,textcolor,name, cart):
    str=''
    for row in selectAll("Menu"):
        url=url_for(row['link'])
        str=str+"""<li><a href='"""+url+"""' style="color:"""+textcolor+""";">"""+row['Label']+"""</a></li>"""
    return """<div class="site-navbar bg-white py-2" >
  <div class="search-wrap">
    <div class="container">
      <a href="#" class="search-close js-search-close"><span class="icon-close2"></span></a>
      <form action="#" method="post">
        <input type="text" class="form-control" placeholder="Search keyword and hit enter...">
      </form>
    </div>
  </div>
  <div class="container" style="background-color:"""+backgroundcolor+""";">
    <div class="d-flex align-items-center justify-content-between">
      <div class="logo">
        <div class="site-logo">
          <a href="index.html" class="js-logo-clone" style="color:"""+textcolor+""";">"""+name+"""</a>
        </div>
      </div>
      <div class="main-nav d-none d-lg-block">
        <nav class="site-navigation text-right text-md-center" role="navigation">
          <ul class="site-menu js-clone-nav d-none d-lg-block">
          """+str+"""
          </ul>
        </nav>
      </div>
      <div class="icons">
        <a href="#" style="color:"""+textcolor+""";" class="icons-btn d-inline-block js-search-open"><span class="icon-search"></span></a>
        <a href="cart.html" style="color:"""+textcolor+""";"class="icons-btn d-inline-block bag">
          <span class="icon-shopping-bag"></span>
          <span class="number">"""+cart+"""</span>
        </a>
        <a href="#" class="site-menu-toggle js-menu-toggle ml-3 d-inline-block d-lg-none"><span class="icon-menu"></span></a>
      </div>
    </div>
  </div>
</div>"""


def card1(backgroundcolor,textcolor,title,tagline,price,link,image):
    return """<div class="site-blocks-cover" data-aos="fade" style="background-color:"""+backgroundcolor+""";">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-5 text-center">
        <div class="featured-hero-product w-100">
          <h1 class="mb-2" style="color:"""+textcolor+""";">"""+title+"""</h1>
          <h4 style="color:"""+textcolor+""";">"""+tagline+"""</h4>
          <div class="price mt-3 mb-5" style="color:"""+textcolor+""";"><strong>$"""+price+"""</strong></div>
          <p><a href="/shop.html" class="btn btn-outline-primary rounded-0">Shop Now</a> <a href='"""+link+"""' class="btn btn-primary rounded-0">Buy Now</a></p>
        </div>
      </div>
      <div class="col-lg-7 align-self-end text-center text-lg-right">
        <img src='"""+image+"""' alt="Image" class="img-fluid img-1">
      </div>
    </div>
  </div>
</div>"""

def card2(backgroundcolor,textcolor,hashtag,title,link,image):
    return """<div class="site-blocks-cover inner-page py-5"  data-aos="fade" style="background-color:"""+backgroundcolor+""";">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-6 ml-auto order-lg-2 align-self-start">
        <div class="site-block-cover-content">
        <h2 class="sub-title" style="color:"""+textcolor+""";">#"""+hashtag+"""</h2>
        <h1 style="color:"""+textcolor+""";">"""+title+"""</h1>
        <p><a href='"""+link+"""' class="btn btn-black rounded-0">Shop Now</a></p>
        </div>
      </div>
      <div class="col-lg-6 order-1 align-self-end">
        <img src='"""+image+"""' alt="Image" class="img-fluid">
      </div>
    </div>
  </div>
</div>"""

def carousel(rows,title):
    str=''

    for row in rows:
        p = format(row['Price'], '.2f')
        url=url_for('shopsingle',prod=row['Name'])
        str=str+"""<div class="product">
        <a href='"""+url+"""' class="item">
          <img alt="Embedded Image" src='"""+row['Image']+"""' class="center"/>
          <div class="item-info">
            <h3 style="text-align:center">"""+row['Name']+"""</h3>
            <h5 class="price" style="text-align:center">$"""+p+"""</h5>
            </div>
            </a>
            </div>"""
    return """<div class="site-section">
              <div class="container">
                <div class="row">
                  <div class="title-section text-center col-12">
                    <h2 class="text-uppercase">"""+title+"""</h2>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 block-3 products-wrap">
                    <div class="nonloop-block-3 owl-carousel">
                        """+str+"""
                    </div>
                  </div>
                </div>
              </div>
            </div>"""

def carousel2(rows,title):
    str=''
    for row in rows:
        url=url_for('artist',art=row['Name'])
        str=str+"""<div class="product">
          <a href='"""+url+"""' class="item">
            <img alt="Embedded Image" src='"""+row['Image']+"""'"/>
            <div class="item-info">
              <h3>"""+row['Name']+"""</h3>
            </div>
          </a>
        </div>"""
    return """<div class="site-section">
            <div class="container">
            <div class="row">
              <div class="title-section text-center col-12">
                <h1 class="text-uppercase">"""+title+"""</h1>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12 block-3 products-wrap">
                <div class="nonloop-block-3 owl-carousel">
                  """+str+"""
                </div>
              </div>
            </div>
            </div>
            </div>"""

def footer(backgroundcolor,textcolor,about,address,phonenumber,email, subsciber_form):
    return """<footer class="site-footer custom-border-top">
  <div class="container" style="background-color:"""+backgroundcolor+""";">
    <div class="row">
      <div class="col-md-6 col-lg-3 mb-4 mb-lg-0">

        <div class="block-7">
          <h3 class="footer-heading mb-4" style="color:"""+textcolor+""";">About Us</h3>
          <p style="color:"""+textcolor+""";">"""+about+"""</p>
        </div>
        <div class="block-7">
          <form action="{{url_for('subscribed')}}" method='post'>
            {{ subsciber_form.csrf_token }}
            <label for="email_subscribe" class="footer-heading" style="color:"""+textcolor+""";">Subscribe</label>
            <div class="form-group">
            {{ subsciber_form.email(class="form-control py-4", placeholder="Email") }}
              <input type="submit" class="btn btn-sm btn-primary" value="Send">
            </div>
          </form>
        </div>
      </div>
      <div class="col-lg-5 ml-auto mb-5 mb-lg-0">
        <div class="row">
          <div class="col-md-12">
            <h3 class="footer-heading mb-4" style="color:"""+textcolor+""";">Quick Links</h3>
          </div>
          <div class="col-md-6 col-lg-6">
            <ul class="list-unstyled">
              <li><a href="/index.html" style="color:"""+textcolor+""";">Home</a></li>
              <li><a href="/shop.html" style="color:"""+textcolor+""";">Products</a></li>
              <li><a href="/shopservices.html" style="color:"""+textcolor+""";">Services</a></li>
              <li><a href="/cart.html" style="color:"""+textcolor+""";">Shopping cart</a></li>
              <li><a href="/contact.html" style="color:"""+textcolor+""";">Contact</a></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="col-md-6 col-lg-3">
        <div class="block-5 mb-5">
          <h3 class="footer-heading mb-4" style="color:"""+textcolor+""";">Contact Info</h3>
          <ul class="list-unstyled">
            <li class="address" style="color:"""+textcolor+""";">"""+address+"""</li>
            <li class="phone" style="color:"""+textcolor+""";"><a href="tel://"""+phonenumber+"""">"""+phonenumber+"""</a></li>
            <li class="email" style="color:"""+textcolor+""";">"""+email+"""</li>
          </ul>
        </div>


      </div>
    </div>
    <div class="row pt-5 mt-5 text-center">
      <div class="col-md-12">
        <p>
        <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
        Copyright &copy;<script>document.write(new Date().getFullYear());</script> All rights reserved | This template is made with <i class="icon-heart" aria-hidden="true"></i> by <a href="https://colorlib.com" target="_blank" class="text-primary">Colorlib</a>
        <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
        </p>
      </div>

    </div>
  </div>
</footer>
</div>

<script src="static/js/jquery-3.3.1.min.js"></script>
<script src="static/js/jquery-ui.js"></script>
<script src="static/js/popper.min.js"></script>
<script src="static/js/bootstrap.min.js"></script>
<script src="static/js/owl.carousel.min.js"></script>
<script src="static/js/jquery.magnific-popup.min.js"></script>
<script src="static/js/aos.js"></script>
<script src="static/js/main.js"></script>

</body>
</html>"""


@app.route('/', methods = ['POST', 'GET'])
def home():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    c1ti,c1ta,c1p,c1l,dst1,c1bc,c1tc,c2h,c2t,c2l,dst2,c2bc,c2tc,c3h,c3t,c3l,dst3,c3bc,c3tc=homeinfo()
    if request.method == 'POST':
        return redirect(url_for('shopsingle', prod=request.form['product']))
    return render_template("index.html", cart=cartSum(), subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        rows=selectAll("Products"), rows2=selectAll("Services"),menu=selectAll("Menu"),
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))),
        card1=Markup(card1(c1bc,c1tc,c1ti,c1ta,c1p,c1l,dst1)),
        collection=Markup(carousel(selectAll("Services"),"Services")),
        card2=Markup(card2(c2bc,c2tc,c2h,c2t,c2l,dst2)),
        card3=Markup(card2(c3bc,c3tc,c3h,c3t,c3l,dst3)),
        footer=Markup(footer(backgroundcolor,textcolor,about,address,phonenumber,email,SubscriberForm())))

@app.route('/index.html', methods = ['POST', 'GET'])
def index():
    return redirect(url_for('home'))

@app.route('/listen.html', methods = ['POST', 'GET'])
def listen():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    if request.method == 'POST':
        return redirect(url_for('artist',art=request.form['artist']))
    return render_template('listen.html', cart=cartSum(),subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        rows=selectAll("Playlists"), rows2=selectAll("Artists"),menu=selectAll("Menu"),
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))),
        artistname=selectOne("Name","Artists"),artistimage=selectOne("Image","Artists"),
        collection=Markup(carousel2(selectAll("Artists"),"Artist Blogs")))

@app.route('/<art>', methods = ['POST', 'GET'])
def artist(art=None):
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    return render_template('artist.html',cart=cartSum(), subsciber_form=SubscriberForm(),menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        artistname=art,artistbio=selectOneWhere("Biography","Artists","Name",art),
        artistimage=selectOneWhere("Image","Artists","Name",art),
        artistimage2=selectOneWhere("Image2","Artists","Name",art))

@app.route('/watch.html', methods = ['POST', 'GET'])
def watch():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    return render_template('watch.html',cart=cartSum(), subsciber_form=SubscriberForm(),menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        musicvideos=Markup(carousel2(selectAllWhere("Watch","Type","Music Video"),"Music Videos")),
        skits=Markup(carousel2(selectAllWhere("Watch","Type","Skit"),"Dumblit Skits")),
        ads=Markup(carousel2(selectAllWhere("Watch","Type","Ad"),"Dumblit Ads")),
        podcasts=Markup(carousel2(selectAllWhere("Watch","Type","Podcast"),"Dumblit Podcasts")),
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))

@app.route('/about.html',methods = ['POST', 'GET'])
def about():
   subsciber_form = SubscriberForm()
   cart = cartSum()
   name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
   aP,t,c1p,dst,c1bc,c1tc,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4=aboutinfo()
   if subsciber_form.validate_on_submit():
       insert("Subscribers",(subsciber_form.email.data))
   return render_template('about.html',cart=cartSum(), subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        aP=aP,t=t,c1p=c1p,dst=dst,t1n=t1n,t1p=t1p,t1a=t1a,dst1=dst1,menu=selectAll("Menu"),
        t2n=t2n,t2p=t2p,t2a=t2a,dst2=dst2,
        t3n=t3n,t3p=t3p,t3a=t3a,dst3=dst3,
        t4n=t4n,t4p=t4p,t4a=t4a,dst4=dst4,
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))

@app.route('/subscribed.html',methods = ['POST', 'GET'])
def subscribed():
   subsciber_form=SubscriberForm()
   name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
   if subsciber_form.validate_on_submit():
       val = subsciber_form.email.data
       insert("Subscribers","Email",(val))
   return render_template('subscribed.html',cart=cartSum(),subsciber_form=subsciber_form,menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))

@app.route('/contact.html',methods = ['POST', 'GET'])
def contact():
    contact_form = ContactForm()
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    if contact_form.validate_on_submit():
        insert("Contact","FName,LName,Email,Subject,Message",(contact_form.fname.data,contact_form.lname.data,contact_form.email.data,contact_form.subject.data,contact_form.message.data))
        return redirect(url_for('home'))   #returning to homepage after adding data
    return render_template("contact.html", cart=cartSum(), contact_form=contact_form,menu=selectAll("Menu"),
    name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
    header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))


@app.route('/shop.html',methods = ['POST', 'GET'])
def shop():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    categories=selectDistinct("Type","Products")
    x=[]
    for row in categories:
        x.append(selectOneWhere("Count(Type)","Products","Type",row['type']))
    y=[]
    list=['Small','Medium','Large','XL']
    for item in list:
        y.append(selectOne("SUM("+ item +")","Products"))
    if request.method == 'POST':
        return redirect(url_for('shopsingle', prod=request.form['product']))
    return render_template('shop.html',cart=cartSum(), subsciber_form=SubscriberForm(),
    name=name, email=email,address=address,phonenumber=phonenumber,about=about,
    backgroundcolor=backgroundcolor, textcolor=textcolor,
    rows=selectAll("Products"), menu=selectAll("Menu"),categories=categories, count=x, size=y,list=list,
    header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))),
    collection=Markup(carousel(selectAll("Products"),"Products")))

@app.route('/shopservices.html',methods = ['POST', 'GET'])
def shopservices():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    if request.method == 'POST':
        return redirect(url_for('shopsingle', prod=request.form['product']))
    return render_template('shop.html',cart=cartSum(), subsciber_form=SubscriberForm(),menu=selectAll("Menu"),
    name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
    rows=selectAll("Services"),collection=Markup(carousel(selectAll("Services"),"Services")),
    header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))

@app.route('/<prod>.html',methods = ['POST', 'GET'])
def shopsingle(prod=None):    #get name, price, pricture, descritption, or row number and get from directory
    subsciber_form = SubscriberForm()
    cart = cartSum()
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    options = []
    t="Services"
    if exists("Products","Name",prod) == 1:
        t="Products"
        if selectOneWhere("Small","Products","Name",prod) > 0:
            options.append('Small')
        if selectOneWhere("Medium","Products","Name",prod) > 0:
            options.append('Medium')
        if selectOneWhere("Large","Products","Name",prod) > 0:
            options.append('Large')
        if selectOneWhere("XL","Products","Name",prod) > 0:
            options.append('XL')
    price = selectOneWhere("Price",t,"Name",prod)
    description = selectOneWhere("Description",t,"Name",prod)
    dst = selectOneWhere("Image",t,"Name",prod)
    if request.method == 'POST':
        option = request.form['option']
        quantity = int(request.form['qty'])
        total=selectOneWhere("Price",t,"Name",prod)*quantity
        item=date.today()
        insert("Cart","Session,ItemNum,Name,Price,Size,Quantity,Total,Image",(session['csrf_token'],item,prod,price,option,quantity,total,dst))
        return redirect(url_for('cart'))
    return render_template('shop-single.html',prod=prod,cart=cart, subsciber_form=subsciber_form,menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        options=options,price=format(price, '.2f'),description=description,image=dst,
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))


@app.route('/cart.html',methods = ['POST', 'GET'])
def cart():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    if exists("Cart","Session",session['csrf_token']) == 0:
        sub = 0
    else:
        sub = float(selectOneWhere("SUM(Total)","Cart","Session",session['csrf_token']))
    if request.method == 'POST':
        #dropTable("Cart")
        createTable("Cart","Session TEXT,ItemNum TEXT,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")
        if removeitem("Cart","ItemNum",request.form['remove']):
            if len(selectAll("Cart")) == 0:
                sub = 0
            else:
                sub = float(selectOneWhere("SUM(Total)","Cart","Session",session['csrf_token']))
        ship = 5
        total = round(sub * 1.07,2)
        return render_template('cart.html',cart=cartSum(),subsciber_form=SubscriberForm(),menu=selectAll("Menu"),
            name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
            rows=selectAll("Cart"), subtotal=sub, total=total)
    ship = 5
    total = round(sub * 1.07,2)
    return render_template('cart.html',cart=cartSum(),subsciber_form=SubscriberForm(),menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        rows=selectAll("Cart"), subtotal=sub, total=total)

@app.route('/checkout.html',methods = ['POST', 'GET'])
def checkout():
    subsciber_form = SubscriberForm()
    coupon_form = CouponCodeForm()
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    rows = selectAll("Cart")
    sub = float(selectOne("SUM(Total)","Cart"))
    ship = 5
    total = round(sub * 1.07,2)
    sub = format(sub, '.2f')
    total = format(total, '.2f')
    if request.method == 'POST':
        return redirect(url_for('thankyou'))
    return render_template('checkout.html',cart=cartSum(), subsciber_form=subsciber_form,menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        rows=selectAll("Cart"), subtotal=sub, total=total)

@app.route('/thankyou.html',methods = ['POST', 'GET'])
def thankyou():
   subsciber_form = SubscriberForm()
   name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
   dropTable("Cart")
   createTable("Cart","ItemNum INTEGER,Name TEXT,Price REAL,Size TEXT,Quantity INTEGER,Total REAL,Image BLOB")
   return render_template('thankyou.html',cart=cartSum(),subsciber_form=subsciber_form,menu=selectAll("Menu"),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))))


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

@app.route('/editall',methods = ['POST', 'GET'])
def editall():
    name,email,address,phonenumber,about,backgroundcolor,textcolor=editinfo()
    c1ti,c1ta,c1p,c1l,dst1,c1bc,c1tc,c2h,c2t,c2l,dst2,c2bc,c2tc,c3h,c3t,c3l,dst3,c3bc,c3tc=homeinfo()
    if request.method == 'POST':
        return redirect(url_for('shopsingle', prod=request.form['product']))
    return render_template('editall.html', cart=cartSum(), subsciber_form=SubscriberForm(),
        name=name, email=email,address=address,phonenumber=phonenumber,about=about,backgroundcolor=backgroundcolor,
        rows=selectAll("Products"), rows2=selectAll("Services"),menu=selectAll("Menu"),
        header=Markup(header(backgroundcolor,textcolor,name,str(cartSum()))),
        card1=Markup(card1(c1bc,c1tc,c1ti,c1ta,c1p,c1l,dst1)),
        collection=Markup(carousel(selectAll("Services"),"Services")),
        card2=Markup(card2(c2bc,c2tc,c2h,c2t,c2l,dst2)),
        card3=Markup(card2(c3bc,c3tc,c3h,c3t,c3l,dst3)),
        footer=Markup(footer(backgroundcolor,textcolor,about,address,phonenumber,email,SubscriberForm())))

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
        ebackground = form.ebackground.data
        etextcolor = form.etextcolor.data
        dropTable("SiteInfo")
        createTable("SiteInfo","Name TEXT,Email TEXT,Address TEXT,PhoneNumber TEXT,About TEXT,BackgroundColor TEXT, TextColor TEXT")
        insert("SiteInfo","Name, Email, Address, PhoneNumber, About,BackgroundColor, TextColor",(ename,eemail, eaddress, ephone, eabout,ebackground,etextcolor))
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
        dst1 = uploadImage(form.card1Photo)
        c1bc = form.card1background.data
        c1tc = form.card1textcolor.data
        c2h = form.card2Hashtag.data
        c2t = form.card2Title.data
        c2l = form.card2Link.data
        dst2 = uploadImage(form.card2Photo)
        c2bc = form.card2background.data
        c2tc = form.card2textcolor.data
        c2bc = form.card2background.data
        c2tc = form.card2textcolor.data
        c3h = form.card3Hashtag.data
        c3t = form.card3Title.data
        c3l = form.card3Link.data
        dst3 = uploadImage(form.card3Photo)
        c3bc = form.card3background.data
        c3tc = form.card3textcolor.data
        dropTable("EditHome")
        createTable("EditHome","Card1Title TEXT,Card1Tagline TEXT,Card1Price TEXT,Card1Link TEXT,Card1Photo BLOB,Card1BackgroundColor TEXT, Card1TextColor TEXT,Card2Hashtag TEXT,Card2Title TEXT,Card2Link TEXT,Card2Photo BLOB,Card2BackgroundColor TEXT, Card2TextColor TEXT,Card3Hashtag TEXT,Card3Title TEXT,Card3Link TEXT,Card3Photo BLOB,Card3BackgroundColor TEXT, Card3TextColor TEXT")
        insert("EditHome","Card1Title, Card1Tagline, Card1Price, Card1Link, Card1Photo,Card1BackgroundColor,Card1TextColor, Card2Hashtag,Card2Title,Card2Link,Card2Photo,Card2BackgroundColor,Card2TextColor,Card3Hashtag,Card3Title,Card3Link,Card3Photo,Card3BackgroundColor,Card3TextColor",(c1ti,c1ta,c1p,c1l,dst1,c1bc,c1tc, c2h,c2t,c2l,dst2,c2bc,c2tc, c3h,c3t,c3l,dst3,c3bc,c3tc))
        return redirect(url_for('home'))
    return render_template("edithome.html", form=form)

@app.route('/editabout', methods = ['POST', 'GET'])
@flask_login.login_required
def editabout():
    form = EditAbout()
    if form.validate_on_submit():
        about = form.aboutPar.data
        title = form.title.data
        dst = uploadImage(form.cardPhoto)
        bc = form.backgroundcolor.data
        tc = form.textcolor.data
        t1n = form.team1Name.data
        t1p = form.team1Position.data
        t1a = form.team1About.data
        dst1 = uploadImage(form.team1Photo)
        t2n = form.team2Name.data
        t2p = form.team2Position.data
        t2a = form.team2About.data
        dst2 = uploadImage(form.team2Photo)
        t3n = form.team1Name.data
        t3p = form.team3Position.data
        t3a = form.team3About.data
        dst3 = uploadImage(form.team3Photo)
        t4n = form.team1Name.data
        t4p = form.team4Position.data
        t4a = form.team4About.data
        dst4 = uploadImage(form.team4Photo)
        dropTable("EditAbout")
        createTable("EditAbout","aboutPar TEXT,Title TEXT,cardPar TEXT,cardPhoto BLOB,BackgroundColor TEXT,TextColor TEXT,Team1Name TEXT,Team1Position TEXT,Team1About TEXT,Team1Photo BLOB,Team2Name TEXT,Team2Position TEXT,Team2About TEXT,Team2Photo BLOB,Team3Name TEXT,Team3Position TEXT,Team3About TEXT,Team3Photo BLOB,Team4Name TEXT,Team4Position TEXT,Team4About TEXT,Team4Photo BLOB")
        insert("EditAbout","aboutPar, Title, cardPar,cardPhoto,BackgroundColor,TextColor,Team1Name,Team1Position, Team1About,Team1Photo, Team2Name,Team2Position,Team2About,Team2Photo,Team3Name,Team3Position,Team3About,Team3Photo,Team4Name,Team4Position,Team4About,Team4Photo",(about,title,c1p,dst,bc,tc,t1n,t1p,t1a,dst1,t2n,t2p,t2a,dst2,t3n,t3p,t3a,dst3,t4n,t4p,t4a,dst4))
        return redirect(url_for('about'))
    return render_template("editabout.html", form=form)

@app.route('/add', methods = ['POST', 'GET'])
@flask_login.login_required
def add():
    form = ProductForm()
    form2 = RemoveForm()
    list=['Name', 'Price', 'Description', 'Small', 'Medium', 'Large', 'XL', 'Type', 'Image']
    if form.validate_on_submit():
        name = form.name.data
        price = float(form.price.data)
        description = form.description.data
        small = int(form.small.data)
        medium = int(form.medium.data)
        large = int(form.large.data)
        xl = int(form.xl.data)
        type = form.type.data
        dst = uploadImage(form.photo)
        insert("Products","Name, Price, Description, Small, Medium, Large, XL, Type, Image",(name,price, description, small, medium, large, xl, type, dst))
        return render_template("add.html", name="Products",url='/add',form=form, form2=form2, rows=selectAll("Products"),list=list)
    return render_template("add.html", name="Products",url='/add', form=form, form2=form2, rows=selectAll("Products"),list=list)

@app.route('/services', methods = ['POST', 'GET'])
@flask_login.login_required
def services():
    form = ServicesForm()
    form2 = RemoveForm()
    list=['Name', 'Price', 'Time', 'Description', 'Type', 'Image']
    if form.validate_on_submit():
        name = form.sname.data
        price = float(form.sprice.data)
        time = form.stime.data
        description = form.sdescription.data
        type = form.stype.data
        dst = uploadImage(form.sphoto)
        insert("Services","Name, Price, Time, Description, Type, Image",(name,price,time,description,type,dst))
        return render_template("add.html", name="Services",url='/services', form=form,form2=form2,rows=selectAll("Services"),list=list)
    return render_template("add.html", name="Services",url='/services', form=form,form2=form2,rows=selectAll("Services"),list=list)

@app.route('/menus', methods = ['POST', 'GET'])
@flask_login.login_required
def menus():
    form = MenuForm()
    createTable("Menu","Label TEXT,Link TEXT")
    form2 = RemoveForm()
    list=['Label', 'Link']
    if form.validate_on_submit():
        label = form.label.data
        link = form.link.data
        createTable("Menu","Label TEXT,Link TEXT")
        insert("Menu","Label, Link",(label,link))
        return render_template("add.html", name="Menu", url='/menus',form=form,form2=form2,rows=selectAll("Menu"),list=list)
    return render_template("add.html", name="Menu",url='/menus', form=form,form2=form2,rows=selectAll("Menu"),list=list)

@app.route('/addartist', methods = ['POST', 'GET'])
@flask_login.login_required
def addartist():
    form = ArtistForm()
    form2=RemoveForm()
    list=['Name', 'Email', 'Biography', 'Image', 'Image2']
    createTable("Artists","Name TEXT,Email TEXT,Biography TEXT,Image BLOB,Image2 BLOB")
    if form.validate_on_submit():
        an = form.artistname.data
        ae = form.artistemail.data
        ab = form.artistbio.data
        ai = uploadImage(form.artistimage)
        ai2 = uploadImage(form.artistimage2)
        insert("Artists","Name, Email, Biography, Image, Image2",(an,ae, ab, ai, ai2))
        return render_template("add.html", name="Artists",url='/addartist', form=form,form2=form2,rows=selectAll("Artists"),list=list)
    return render_template("add.html", name="Artists", form=form,form2=form2,rows=selectAll("Artists"),list=list)

@app.route('/addplaylist', methods = ['POST', 'GET'])
@flask_login.login_required
def addplaylist():
    form = PlaylistForm()
    form2=RemoveForm()
    list=['Name', 'Link', 'Image']
    createTable("Playlists","Name TEXT,Link TEXT,Image BLOB")
    if form.validate_on_submit():
        pn = form.playlistname.data
        pl = form.playlistlink.data
        pi = uploadImage(form.playlistimage)
        insert("Playlists","Name, Link, Image",(pn,pl, pi))
        return render_template("add.html", name="Playlists",url='/addplaylist', form=form,form2=form2,rows=selectAll("Playlists"),list=list)
    return render_template("add.html", name="Playlists", form=form,form2=form2,rows=selectAll("Playlists"),list=list)

@app.route('/addwatch', methods = ['POST', 'GET'])
@flask_login.login_required
def addwatch():
    form = WatchForm()
    form2=RemoveForm()
    list=['Name','Type', 'Link', 'Image']
    createTable("Watch","Name TEXT,Type TEXT,Link TEXT,Image BLOB")
    if form.validate_on_submit():
        n = form.addname.data
        t = form.addtype.data
        l = form.addlink.data
        f = uploadImage(form.addfile)
        insert("Watch","Name, Type, Link, Image",(n,t,l,f))
        return render_template("add.html", name="Watch",url='/addwatch', form=form,form2=form2,rows=selectAll("Watch"),list=list)
    return render_template("add.html", name="Watch", form=form,form2=form2,rows=selectAll("Watch"),list=list)

@app.route('/remove', methods = ['POST', 'GET'])
@flask_login.login_required
def remove():
    form = ProductForm()
    form2 = RemoveForm()
    if form2.validate_on_submit():
        name = form2.name.data
        if removeitem("Menu","Label",name):
            return redirect(url_for('menus'))
        if removeitem("Products","Name",name):
            return redirect(url_for('add'))
        if removeitem("Services","Name",name):
            return redirect(url_for('services'))
        if removeitem("Artists","Name",name):
            return redirect(url_for('addartist'))
        if removeitem("Watch","Name",name):
            return redirect(url_for('addwatch'))
        if removeitem("Playlist","Name",name):
            return redirect(url_for('addplaylist'))

        return redirect(url_for('add'))

    return redirect(url_for('add'))

@app.route('/orders', methods = ['POST', 'GET'])
@flask_login.login_required
def orders():
    list=['FName','LName','Address','State','ProductsOption']
    return render_template("orders.html", name="Orders",rows=selectAll("Orders"),list=list)

@app.route('/subscribers', methods = ['POST', 'GET'])
@flask_login.login_required
def subscribers():
    list=['Email']
    return render_template("orders.html", name="Subscribers", rows=selectAll("Subscribers"),list=list)

@app.route('/contactList', methods = ['POST', 'GET'])
@flask_login.login_required
def contactList():
    list=['FName','LName','Email','Subject','Message']
    return render_template("orders.html", name="Contacts", rows=selectAll("Contact"),list=list)

@app.route('/logout', methods = ['POST', 'GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':  #function for if this were main

   app.run(debug = True)    #run application
