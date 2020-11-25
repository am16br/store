from flask import *
from flaskr.db import get_db

def MakeTable(list, table, where):
    string = "SELECT * FROM " + table
    if(where):
        string = string+where
    db = get_db()
    rows = db.execute(string).fetchall()
    labels = ""
    content = ""
    for x in list:
        labels = labels + "<th>"+x+"</th>"
    for row in rows:
        content = content + "<tr>"
        for x in list:
            if(x == "Image"):
                content = content + "<td><img width=200px src='"+url_for('static', filename=row['image']) +"' ></td>"
            elif(x == "Add Variant"):
                content = content + "<td><a class='action' href='"+url_for('blog.addVariant', id=row['id'])+"'>Add Variant</td>"
            elif(x == "Delete"):
                content = content + "<td><form action='"+url_for('blog.delete', id=row['id'], page=table)+"' method='post'><input class='danger' type='submit' value='Delete' onclick='return confirm('Are you sure?');'></form></td>"
            elif(x == "Visit Page"):
                content = content + "<td><a class='action' href='"+url_for('blog.profile', id=row['id'], name=row['name'])+"'>Visit</td>"
            else:
                content = content + "<td>"+str(row[x])+"</td>"
        content = content + "</tr>"
    return """<table border = 1 width="100%" cellspacing="0">
      <thead>
        <tr>
          """+labels+"""
      </thead>
      <tfoot>
        <tr>
          """+labels+"""
        </tr>
      </tfoot>
      <tbody>
        """+content+"""
      </tbody>
    </table>
    """

def carousel(rows,title):
    string=''
    for row in rows:
        p = str('%.2f' % row['Price'])
        #url=url_for('shopsingle',prod=row['Name'])
        url=url_for('blog.product',id=row['id'])
        string=string+"""<div class="product">
        <a href='"""+url+"""' class="item">
          <img alt="Embedded Image" width=200; height=200; object-fit:scale-down; src='"""+url_for('static', filename=row['image']) +"""' class="center"/>
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
                    <h1 class="text-uppercase">"""+title+"""</h1>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 block-3 products-wrap">
                    <div class="nonloop-block-3 owl-carousel">
                        """+string+"""
                    </div>
                  </div>
                </div>
              </div>
            </div>"""

def carousel2(rows,title):
    str=''
    for row in rows:
        url=url_for('blog.post',id=row['id'])
        str=str+"""<div class="product">
          <a href='"""+url+"""' class="item">
            <img alt="Embedded Image" width=200; height=200; object-fit:scale-down; src='"""+url_for('static', filename=row['file']) +"""'/>
            <div class="item-info">
              <h3>"""+row['title']+"""</h3>
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
