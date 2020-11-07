from flask import *
import sqlite3


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
