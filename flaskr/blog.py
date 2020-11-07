#. venv/bin/activate
#export FLASK_APP=flaskr
#export FLASK_ENV=development
#flask run
#flask init-db
import os
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename


from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.forms import *
from flaskr.models import *


bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

def build_query(option, fields, table, order):
    if(option == "SELECT"):
        string = "SELECT "+fields+" FROM "+table
    elif(option == "DELETE"):
        string = "DELETE FROM "+table
    elif(option == "UPDATE"):
        string = "UPDATE "+table+" SET "+ fields
    if(where):
        string = string + " WHERE "+where+" = ?"
    if(order):
        string = string + " ORDER BY "+order
    return string


def get_post(id, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (get_db().execute(
            "SELECT p.id, title, body, created, file, author_id, username"
            " FROM Post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",(id,),).fetchone())
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    return post

def get_profile(id, check_author=True):
    post = (get_db().execute(
            "SELECT p.id, Name, Email, Phone, Location, Instagram, Twitter, Facebook, Youtube, Soundcloud, Spotify, AppleMusic, Biography, Image, Image2, menu_color, background_color, main_text_color, secondary_text_color, author_id"
            " FROM Profile p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",(id,),).fetchone())
    if post is None:
        abort(404, f"Profile id {id} doesn't exist.")
    if check_author and post["author_id"] != g.user["id"]:
        abort(403)
    return post

def get_product(id, check_author=True):
    post = (get_db().execute(
            "SELECT v.Name, v.Image, p.Name, p.Price, p.Description"
            " FROM variant v JOIN Product p ON v.product_id = p.id"
            " WHERE p.id = ?",(id,),).fetchone())
    if post is None:
        abort(404, f"Product id {id} doesn't exist.")
    return post

def get_add_page(page):
    if(page == "Post"):
        form = PostForm()
        string = "title, body, file, author_id"
        values = "?, ?, ?, ?"
        mark=""
    elif(page == "Product"):
        form = ProductForm()
        string = "name, price, description, image, author_id"
        values = "?, ?, ?, ?, ?"
        mark = Markup(MakeTable(["Delete", "Add Variant", "Name", "Price", "Description", "Image"], "Product",""))
    elif(page == "Profile"):
        form = ProfileForm()
        string = "Name, Email, Phone, Location, Instagram, Twitter, Facebook, Youtube, Soundcloud, Spotify, AppleMusic, Biography, Image, Image2, menu_color, background_color, main_text_color, secondary_text_color, author_id"
        values = "?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"
        mark = Markup(MakeTable(["Visit Page", "Name", "Email", "Biography", "Image"], "Profile", ""))
    elif(page == "Message"):
        form = MessageForm()
        string = "author_id, receiver_id, body, file"
        values = "?, ?, ?, ?"
        mark = ""
    return form, string, values, mark

def get_update_page(id, page):
    if(page == "Post"):
        form = PostForm()
        string = "title = ?, body = ? WHERE id = ?"
        post = get_post(id)
    elif(page == "Product"):
        form = ProductForm()
        string = "name = ?, description = ?, price = ?, image = ?"
        post = get_post(id)
    elif(page == "Profile"):
        form = ProfileForm()
        string = "Name = ?, Email = ?, Phone = ?, Location = ?, Instagram = ?, Twitter = ?, Facebook = ?, Youtube = ?, Soundcloud = ?, Spotify = ?, AppleMusic = ?, Biography = ?, Image = ?, Image2 = ?, menu_color =?, background_color = ?, main_text_color = ?, secondary_text_color = ?"
        post = get_profile(id)
    return form, string, post

def get_table(page):
    if(page == "Product"):
        list = ["Delete Product", "Add Variant", "Name", "Price", "Description", "Image"]
    elif(page == "Profile"):
        list = ["Visit Page", "Name", "Email", "Biography", "Image"]
    elif(page == "Message"):
        list = ["author_id", "body", "file", "created"]
    return list

@bp.route("/post/<int:id>", methods=("GET", "POST"))
def post(id):
    form = CommentForm()
    post = get_post(id)
    db = get_db()
    comments = (db.execute("SELECT c.id, body, created, post_id, author_id, username FROM Comment c JOIN user u ON c.author_id = u.id WHERE post_id = ?",(id,),).fetchall())
    if form.validate_on_submit():
        comment = form.comment.data
        error = None
        if error is not None:
            flash(error)
        else:
            db.execute("INSERT INTO Comment (author_id, post_id, body) VALUES (?, ?, ?)",(g.user["id"],id, comment),)
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/post.html", post=post, form=form, comments=comments)

@bp.route("/add/<path:page>", methods=("GET", "POST"))
@login_required
def add(page):
    """Create a new post for the current user."""
    form, fields, values, mark = get_add_page(page)
    if form.validate_on_submit():
        t=()
        for field in form:
            if(field.type == "FileField"):
                if(field.data):
                    filename = secure_filename(field.data.filename)
                    file_path=os.path.join("flaskr/static/images", filename)
                    field.data.save(file_path)
                    t =  t + ("static/images/"+filename,)
                else:
                    t = t + ("",)
            elif (field.type == "ColorField"):
                t =  t + (str(field.data),)
            elif (field.type == "DecimalField"):
                t =  t + (float(field.data),)
            elif (field.type == "StringField" or field.type == "TextAreaField"):
                t =  t + (field.data,)
        t = t + (g.user["id"],)
        error = None
        if error is not None:
            flash(error)
        else:
            string = "INSERT INTO "+page+" ("+fields+") VALUES ("+values+")"
            db = get_db()
            db.execute(string,(t),)
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/add.html", form=form, page=page, mark=mark)


@bp.route("/<int:id>/update/<path:page>", methods=("GET", "POST"))
@login_required
def update(id, page):
    form, fields, post = get_update_page(id, page)
    if post["author_id"] != g.user["id"]:
        abort(403)
    if form.validate_on_submit():
        t=()
        for field in form:
            if(field.type == "FileField"):
                if(field.data):
                    filename = secure_filename(field.data.filename)
                    file_path=os.path.join("flaskr/static/images", filename)
                    field.data.save(file_path)
                    t =  t + ("static/images/"+filename,)
                else:
                    t = t + ("",)
            elif (field.type == "ColorField"):
                t =  t + (str(field.data),)
            elif (field.type == "DecimalField"):
                t =  t + (float(field.data),)
            elif (field.type == "StringField" or field.type == "TextAreaField"):
                t =  t + (field.data,)
        t = t + (id,)
        error = None
        if error is not None:
            flash(error)
        else:
            string = "UPDATE "+page+" SET "+fields+" WHERE id = ?"
            db = get_db()
            db.execute(string, (t))
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/update.html", page=page, form=form, post=post)


@bp.route("/<int:id>/delete/<path:page>", methods=("POST",))
@login_required
def delete(id, page):
    #ensure user is owner...
    form, fields, post = get_update_page(id, page)
    if post["author_id"] != g.user["id"]:
        abort(403)
    db = get_db()
    string = "DELETE FROM "+page+" WHERE id = ?"
    db.execute(string, (id,))
    db.commit()
    return redirect(url_for("blog.index"))


@bp.route("/<int:id>/addVariant", methods=("GET", "POST"))
@login_required
def addVariant(id):
    form = VariantForm()
    db = get_db()
    list = ["Delete","Name", "Image"]
    name = (db.execute("SELECT Name FROM Product WHERE id = ?",(id,),).fetchone())[0] + " Variant"
    where=" WHERE product_id = " + str(id)
    """Create a new variant for the current product."""
    if form.validate_on_submit():
        t=()
        for field in form:
            if(field.type == "FileField"):
                if(field.data):
                    filename = secure_filename(field.data.filename)
                    file_path=os.path.join("flaskr/static/images", filename)
                    field.data.save(file_path)
                    t =  t + ("static/images/"+filename,)
                else:
                    t = t + ("",)
            elif (field.type == "ColorField"):
                t =  t + (str(field.data),)
            elif (field.type == "DecimalField"):
                t =  t + (float(field.data),)
            elif (field.type == "StringField" or field.type == "TextAreaField"):
                t =  t + (field.data,)
        t = t + (id,)
        error = None
        if error is not None:
            flash(error)
        else:
            db.execute(
                "INSERT INTO variant (name, image, product_id) VALUES (?, ?, ?)",
                (t),
            )
            db.commit()
        return render_template("blog/add.html", form=form, page=name, mark=Markup(MakeTable(list,'variant', where)))
    return render_template("blog/add.html", form=form, page=name, mark=Markup(MakeTable(list,'variant', where)))

@bp.route("/table/<path:page>", methods=("GET", "POST"))
def table(page):
    list = get_table(page)
    string = "SELECT * FROM " + page
    db = get_db()
    rows = db.execute(string).fetchall()
    return render_template("blog/table.html", list=list, rows=rows, page=page)

@bp.route("/<int:id>/<path:name>", methods=("GET", "POST"))
def profile(id, name):
    """Show all the posts, most recent first."""
    db = get_db()
    post = (db.execute("SELECT * FROM Profile WHERE id = ?",(id,),).fetchone())
    products = (db.execute("SELECT * FROM Product WHERE author_id = ?",(post['author_id'],),).fetchall())
    if(products == []):
        products=""
    else:
        products=Markup(carousel(products, "Products"))
    media = (db.execute("SELECT * FROM Post WHERE author_id = ?",(post['author_id'],),).fetchall())
    if(media == []):
        media=""
    else:
        media=Markup(carousel2(media, "Media"))
    return render_template("blog/profile.html", post=post, products=products, media=media)

@bp.route("/product/<int:id>", methods=("GET", "POST"))
def product(id):
    form=OrderForm()
    string = "SELECT * FROM Product WHERE id = " + str(id)
    db = get_db()
    product = db.execute(string).fetchone()
    string = "SELECT * FROM variant WHERE product_id = " + str(id)
    rows = db.execute(string).fetchall()
    list=[]
    for row in rows:
        list.append(row['Name'])
    form.Option.choices=list
    return render_template("blog/product.html", product=product, rows=rows, form=form)
