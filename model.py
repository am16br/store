from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, RadioField
from wtforms.validators import InputRequired, Length
from werkzeug.datastructures import CombinedMultiDict, ImmutableOrderedMultiDict
from datetime import date,datetime
from werkzeug.utils import secure_filename

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
