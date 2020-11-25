#python3 -m venv venv
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
        string = "sender_id, receiver_id, subject, message, file"
        values = "?, ?, ?, ?, ?"
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
    elif(page == "Cart"):
        list = ["Name", "Quantity", "Price", "Image", "Delete Product",]
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
                    t =  t + ("images/"+filename,)
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
            return render_template("blog/add.html", form=form, page=page, mark=mark)
    return render_template("blog/add.html", form=form, page=page, mark=mark)

@bp.route("/sendMessage/<int:id>", methods=("GET", "POST"))
@login_required
def sendMessage(id):
    """Create a new post for the current user."""
    form, fields, values, mark = get_add_page('Message')
    if form.validate_on_submit():
        t=()
        t=(g.user['id'], id,)
        for field in form:
            if(field.type == "FileField"):
                if(field.data):
                    filename = secure_filename(field.data.filename)
                    file_path=os.path.join("flaskr/static/images", filename)
                    field.data.save(file_path)
                    t =  t + ("images/"+filename,)
                else:
                    t = t + ("",)
            elif (field.type == "ColorField"):
                t =  t + (str(field.data),)
            elif (field.type == "DecimalField"):
                t =  t + (float(field.data),)
            elif (field.type == "StringField" or field.type == "TextAreaField"):
                t =  t + (field.data,)
        error = None
        if error is not None:
            flash(error)
        else:
            string = "INSERT INTO Message ("+fields+") VALUES ("+values+")"
            db = get_db()
            db.execute(string,(t),)
            db.commit()
            return redirect(url_for("blog.inbox"))
    return render_template("blog/add.html", form=form, page="Message", mark=mark)

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
                    t =  t + ("images/"+filename,)
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
                    t =  t + ("images/"+filename,)
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
            return redirect(url_for('blog.index'))
    return render_template("blog/add.html", form=form, page=name, mark=Markup(MakeTable(list,'variant', where)))

@bp.route("/table/<path:page>", methods=("GET", "POST"))
def table(page):

    if(page == "order"):
        list = ["Name", "Address", "Product", "Quantity", "Price"]
        string = "SELECT * FROM " + page
        #string = "SELECT o.id, p.Name, ca.Quantity, cu.Name, cu.Address FROM order o JOIN product p ON o.product_id = p.product_id JOIN cart ca ON "
    else:
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
    if request.method == "POST":

        error = None
        if error is not None:
            flash(error)
        else:
            db.execute(
                "INSERT INTO cart (product_id, cookie) VALUES (?, ?)",
                (id, str(request.cookies),),
            )
            db.commit()
        return redirect(url_for("blog.cart"))
    return render_template("blog/product.html", product=product, rows=rows, form=form)

@bp.route("/cart", methods=("GET", "POST"))
def cart():
    print(request.cookies)
    form = CheckoutForm()
    list = get_table("Cart")
    db = get_db()
    rows = db.execute("SELECT c.id, p.Name, p.Image, c.created, p.Price"
    " FROM cart c JOIN product p ON c.product_id = p.id"
    " WHERE c.cookie = ?",(str(request.cookies),)).fetchall()
    if form.validate_on_submit():
        name = form.Name.data
        address = form.Address.data
        error = None
        if error is not None:
            flash(error)
        else:
            db.execute(
                "INSERT INTO customer (Name, Address, cart_id) VALUES (?, ?, ?)",
                (name, address, str(request.cookies),),
            )
            db.commit()
        return redirect(url_for("blog.orders"))
    return render_template("blog/cart.html", form=form, list=list, rows = rows)

@bp.route("/deletecart/<int:id>", methods=("GET", "POST"))
def deletecart(id):
    db = get_db()
    db.execute("DELETE FROM cart WHERE id = ?",(id,))
    db.commit()
    return redirect(url_for("blog.cart"))

@bp.route("/orders", methods=("GET", "POST"))
@login_required
def orders(id):
    if(g.user_id['username'] == 'admin'):
        db = get_db()
        rows = db.execute("SELECT * FROM customer").fetchall();
        return redirect(url_for("blog.table"))
    return redirect(url_for("blog.index"))

@bp.route('/inbox', methods = ['POST', 'GET'])
@login_required
def inbox():
    db = get_db()
    sentcount = db.execute('SELECT count(*) FROM message WHERE sender_id = ?', (g.user['id'],)).fetchone()[0]
    inboxcount=db.execute('SELECT count(*) FROM message WHERE receiver_id = ?', (g.user['id'],)).fetchone()[0]
    rows = db.execute('SELECT m.id, m.subject, m.created, u.username '
            'FROM message m JOIN user u ON m.sender_id = u.id '
            'WHERE receiver_id = ? ORDER BY created DESC ', (g.user['id'],)).fetchall()
    return render_template("blog/inbox.html",
        inboxcount=inboxcount, sentcount=sentcount, rows=rows)

@bp.route('/sent', methods = ['POST', 'GET'])
@login_required
def sent():
    db = get_db()
    sentcount = db.execute('SELECT count(*) FROM message WHERE sender_id = ?', (g.user['id'],)).fetchone()[0]
    inboxcount=db.execute('SELECT count(*) FROM message WHERE receiver_id = ?', (g.user['id'],)).fetchone()[0]
    rows = db.execute('SELECT m.id, m.subject, m.created, u.username '
            'FROM message m JOIN user u ON m.sender_id = u.id '
            'WHERE sender_id = ? ORDER BY created DESC ', (g.user['id'],)).fetchall()
    return render_template("blog/inbox.html",
        inboxcount=inboxcount, sentcount=sentcount, rows=rows)

@bp.route('/deletemessage/<int:id>')
@login_required
def deletemessage(id):
    db = get_db()
    flag=db.execute('SELECT receiver_id FROM message WHERE id = ?', (id,)).fetchone()[0]
    if(flag == g.user['id']):
        flag=db.execute('SELECT sender_id FROM message WHERE id = ?', (id,)).fetchone()[0]
        if(flag == -1):
            db.execute('DELETE FROM message WHERE id =?', (id,))
        else:
            db.execute('UPDATE message SET receiver_id = ? WHERE id =?', (-1, id,))
    else:
        flag=db.execute('SELECT receiver_id FROM message WHERE id = ?', (id,)).fetchone()[0]
        if(flag == -1):
            db.execute('DELETE FROM message WHERE id =?', (id,))
        else:
            db.execute('UPDATE message SET sender_id = ? WHERE id =?', (-1, id,))
    db.commit()
    return redirect(url_for('blog.inbox'))

@bp.route('/message/<int:id>', methods = ['POST', 'GET'])
@login_required
def message(id):
    db = get_db()
    sentcount = db.execute('SELECT count(*) FROM message WHERE sender_id = ?', (g.user['id'],)).fetchone()[0]
    inboxcount=db.execute('SELECT count(*) FROM message WHERE receiver_id = ?', (g.user['id'],)).fetchone()[0]
    sender = db.execute('SELECT sender_id FROM message WHERE id = ?', (id,)).fetchone()[0]
    user = db.execute('SELECT username FROM user WHERE id = ?', (sender,)).fetchone()[0]
    subject = db.execute('SELECT subject FROM message WHERE id = ?', (id,)).fetchone()[0]
    message = db.execute('SELECT message FROM message WHERE id = ?', (id,)).fetchone()[0]
    return render_template("blog/message.html", inboxcount=inboxcount, sentcount=sentcount,
        user=user,subject=subject,message=message, sender=sender)


@bp.route("/contenteditable", methods=("GET", "POST"))
def contenteditable():

    return render_template("blog/contenteditable.html")
