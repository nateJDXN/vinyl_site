import sqlite3
from flask import Flask, session, render_template, request, url_for, redirect

app = Flask('app')
app.secret_key = "secret"
app.name = ""

@app.route('/')
def index():
  print("Index route, current session: ", session)

  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM products')
  rows = cursor.fetchall()

  connection.commit()
  connection.close()
  
  if 'loggedin' not in session:
    session['loggedin'] = False
    
  if 'cart' not in session:
    session['cart'] = []
    
  in_stock = []
  for product in rows:
    print(product['name'])
    product_in_cart = False
    for item in session['cart']:
      if item['name'] == product['name']:
        product_in_cart = True
        if item['quantity'] > 0 and product['quantity'] >= item['quantity']:
          in_stock.append(True)
        else:
          in_stock.append(False)
        break
    if product_in_cart == False:
      in_stock.append(True)
  
  return render_template("store.html", in_stock = in_stock, rows = rows)


@app.route('/login', methods=['GET', 'POST'])
def login():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()

  if request.method == 'POST':
    uname = request.form['username']
    pword = request.form['password']

    print("Username: " + uname + " Password: " + pword)    

    cursor.execute("SELECT * FROM users WHERE username = ? and password = ?", (uname, pword))
    user = cursor.fetchone()
    connection.commit()
    
    if user != None:
      session['name'] = user['fname']
      #session['history'] = user['history']
      cursor.execute('SELECT * FROM products')
      rows = cursor.fetchall()

      session['loggedin'] = True

      if 'cart' not in session:
        session['cart'] = []

      connection.commit()
      connection.close()
      in_stock = []
      for product in rows:
        print(product['name'])
        product_in_cart = False
        for item in session['cart']:
          if item['name'] == product['name']:
            product_in_cart = True
            if item['quantity'] > 0 and product['quantity'] > item['quantity']:
              in_stock.append(True)
            else:
              in_stock.append(False)
            break
        if product_in_cart == False:
          in_stock.append(True)
      
      return render_template("store.html", in_stock = in_stock, rows = rows)
    else:
      print("Incorrect username or password")
      return render_template("login.html")
    
  return render_template("login.html")
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()

  if request.method == 'POST':
    fname = request.form['firstname']
    lname = request.form['lastname']
    uname = request.form['username']
    pword = request.form['password']

    #make sure no one is using the same username
    cursor.execute("SELECT * FROM users WHERE username = ?", (uname,))
    user = cursor.fetchone()
    connection.commit()

    if user == None:
      cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (uname, pword, fname, lname))
      session['name'] = fname
      #session['history'] = history

      cursor.execute('SELECT * FROM products')
      rows = cursor.fetchall()

      session['loggedin'] = True

      if 'cart' not in session:
        session['cart'] = []

      connection.commit()
      connection.close()
      
      in_stock = []
      for product in rows:
        print(product['name'])
        product_in_cart = False
        for item in session['cart']:
          if item['name'] == product['name']:
            product_in_cart = True
            if item['quantity'] > 0 and product['quantity'] > item['quantity']:
              in_stock.append(True)
            else:
              in_stock.append(False)
            break
        if product_in_cart == False:
          in_stock.append(True)
      return render_template("store.html", in_stock = in_stock, rows = rows)

    else:
      print("Username already exists, please choose another")
      return render_template("signup.html")
  
  return render_template("signup.html")

@app.route('/store', methods=['GET', 'POST'])
def store():

  print("Store route, current session: ", session)
  
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  
  cursor = connection.cursor()

  if request.method == 'POST':
    search_query = request.form['search-query']
    
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (search_query + '%',))
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    
    in_stock = []
    for product in rows:
      print(product['name'])
      product_in_cart = False
      for item in session['cart']:
        if item['name'] == product['name']:
          product_in_cart = True
          if item['quantity'] > 0 and product['quantity'] > item['quantity']:
            in_stock.append(True)
          else:
            in_stock.append(False)
          break
      if product_in_cart == False:
        in_stock.append(True)
        
    return render_template("store.html", in_stock = in_stock, rows = rows)
    

  cursor.execute("SELECT * FROM products")
  rows = cursor.fetchall()
  connection.commit()
  connection.close()
  
  in_stock = []
  for product in rows:
    print(product['name'])
    product_in_cart = False
    for item in session['cart']:
      if item['name'] == product['name']:
        product_in_cart = True
        if item['quantity'] > 0 and product['quantity'] > item['quantity']:
          in_stock.append(True)
        else:
          in_stock.append(False)
        break
    if product_in_cart == False:
      in_stock.append(True)
  
  return render_template("store.html", in_stock = in_stock, rows = rows)


@app.route('/cart', methods=['GET', 'POST'])
def cart():

  print("Cart route, current session: ", session)
  if session['loggedin'] == False:
    print("not logged in")
    return render_template("login.html")
    
  if request.method == 'POST':
    product_name = request.form['product_name']

    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    #add new item to cart
    cursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
    product = cursor.fetchone()

    product_dict = {key: product[key] for key in product.keys()}
    
    for i, item in enumerate(session['cart']):
      if item['name'] == product_name:
        print("Product already in cart")
        session['cart'][i]['quantity'] += 1
        session.modified = True
        # print(session['cart'])
        return render_template("cart.html", cart = session['cart'])

    product_dict['quantity'] = 1
    session['cart'].append(product_dict)
    session.modified = True
    # print(session['cart'])
    return render_template("cart.html", cart = session['cart'])
  
  # print(session['cart'])
  return render_template("cart.html", cart = session['cart'])
    
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
  
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()

  for item in session['cart']:
    name = item['name']
    cursor.execute("UPDATE products SET quantity = quantity - ? WHERE name = ?", (item['quantity'], name))
  
  session['cart'] = []
  session.modified = True
  
  cursor.execute("SELECT * FROM products")
  rows = cursor.fetchall()
  connection.commit()
  
  in_stock = []
  for product in rows:
    print(product['name'])
    product_in_cart = False
    for item in session['cart']:
      if item['name'] == product['name']:
        product_in_cart = True
        if item['quantity'] > 0 and product['quantity'] > item['quantity']:
          in_stock.append(True)
        else:
          in_stock.append(False)
        break
    if product_in_cart == False:
      in_stock.append(True)
  
  
  return render_template("store.html", in_stock = in_stock, rows = rows)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
  
  if request.method == 'POST':
    product_name = request.form['product_name']

    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    for i, item in enumerate(session['cart']):
      if product_name == item['name']:
        if item['quantity'] > 1:
          item['quantity'] -= 1
          session.modified = True
          break
          
        session['cart'].pop(i)
        session.modified = True
        break
    
  cursor.execute("SELECT * FROM products")
  rows = cursor.fetchall()
  connection.commit()
  
  in_stock = []
  for product in rows:
    print(product['name'])
    product_in_cart = False
    for item in session['cart']:
      if item['name'] == product['name']:
        product_in_cart = True
        if item['quantity'] > 0 and product['quantity'] > item['quantity']:
          in_stock.append(True)
        else:
          in_stock.append(False)
        break
    if product_in_cart == False:
      in_stock.append(True)
  
  return render_template("store.html", in_stock = in_stock, rows = rows)
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
  
  session.clear()
  return redirect(url_for('index'))
  
app.run(host='0.0.0.0', port=8080)()
