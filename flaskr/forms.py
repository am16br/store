from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Length
from werkzeug.datastructures import CombinedMultiDict, ImmutableOrderedMultiDict
from wtforms_components import ColorField

class LoginForm(FlaskForm):
    username = StringField(id='Username', validators=[InputRequired('Username Required')])
    password = PasswordField(id='Password', validators=[InputRequired()])

class PostForm(FlaskForm):
    title = StringField(id='Title', validators=[InputRequired('Title Required')])
    body = TextAreaField(id='Body', validators=[InputRequired('Body Required')])
    file = FileField(id='Photo')

class CommentForm(FlaskForm):
    comment = TextAreaField(id='Comment', validators=[InputRequired('Text Required')])

class MessageForm(FlaskForm):
    name = StringField(id='Subject', validators=[InputRequired()])
    comment = TextAreaField(id='Comment', validators=[InputRequired('Text Required')])
    file = FileField(id='File')

class ProductForm(FlaskForm):
    name = StringField(id='Name', validators=[InputRequired()])
    price = DecimalField(id='Price', validators=[InputRequired()])
    description = TextAreaField(id='Description', validators=[InputRequired()])
    photo = FileField(id='Photo', validators=[FileRequired()])

class VariantForm(FlaskForm):
    type = SelectField('Type', choices=["Size", "Option"])
    name = StringField(id='Name', validators=[InputRequired('Name Required')])
    quantity = IntegerField('Quantity')
    file = FileField(id='File')

class CollectionForm(FlaskForm):
    name = StringField(id='Name', validators=[InputRequired()])
    photo = FileField(id='Photo', validators=[FileRequired()])

class ProfileForm(FlaskForm):
    name = StringField(id='Your Name', validators=[InputRequired()])
    email = StringField(id='Public Email')
    phone = StringField(id='Public Phone Number')
    location = StringField(id='Location/Area')
    ig = StringField(id='Instagram Tag: @')
    twitter = StringField(id='Twitter Tag: @')
    fb = StringField(id='Facebook Link')
    yt = StringField(id='Youtube Link')
    soundcloud = StringField(id='Soundcloud Link')
    spotify = StringField(id='Spotify Link')
    apple = StringField(id='Apple Music Link')
    bio = TextAreaField(id='Biography')
    image = FileField(id='Primary Image', validators=[FileRequired()])
    image2 = FileField(id='Secondary Image or Video')
    menu_color = ColorField(id='Menu Color')
    background_color = ColorField(id='Background Color')
    main_text_color = ColorField(id='Main Text Color')
    secondary_text_color = ColorField(id='Secondary Text Color')

class OrderForm(FlaskForm):
    Quantity = SelectField('Quantity', choices=[1,2,3,4,5,6,7,8,9])
    Size = RadioField('Size', choices=["Small", "Medium", "Large"])
    Option = RadioField('Option', choices=[])

class CheckoutForm(FlaskForm):
    Name = StringField(id='Name', validators=[InputRequired()])
    Address = TextAreaField(id='Address', validators=[InputRequired()])


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
