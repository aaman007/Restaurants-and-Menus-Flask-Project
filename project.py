from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind = engine)
# session = DBsession()

@app.route('/')
@app.route('/restaurants')
def allRestaurants():
    session = DBsession()
    restaurants = session.query(Restaurant).all()
    session.close()
    return render_template('allRestaurants.html', restaurants = restaurants)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        session = DBsession()
        name = request.form['name']
        restaurant = Restaurant(name = name)
        session.add(restaurant)
        session.commit()
        session.close()
        flash("New restaurant created!!")
        return redirect(url_for('allRestaurants'))
    return render_template('newRestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = DBsession()
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
            session.commit()
            flash("Restaurant details updated!!")
        session.close()
        return redirect(url_for('allRestaurants'))
    session.close()
    return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = DBsession()
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    if request.method == 'POST':
        items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
        session.delete(restaurant)
        session.commit()
        flash("Restaurant deleted!!")
        for item in items:
            session.delete(item)
            session.commit()
        session.close()
        return redirect(url_for('allRestaurants'))
    session.close()
    return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    session = DBsession()
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()

    items = session.query(MenuItem).filter(restaurant.id == MenuItem.restaurant_id)
    session.close()
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        session = DBsession()
        name = request.form['name']
        price = request.form['price']
        course = request.form['course']
        description = request.form['description']
        newMenu = MenuItem(name = name, price = price, course = course,
                           description = description, restaurant_id = restaurant_id)
        session.add(newMenu)
        session.commit()
        session.close()
        flash("New menu item created!!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    return render_template('newMenuItem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = DBsession()
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['price'] and request.form['course'] and request.form['description']:
            item.name = request.form['name']
            item.price = request.form['price']
            item.course = request.form['course']
            item.description = request.form['description']
            session.add(item)
            session.commit()
            flash("Menu Item details updated!!")
        session.close()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    session.close()
    return render_template('editMenuItem.html', restaurant_id = restaurant_id, item = item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = DBsession()
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        session.close()
        flash("Menu Item deleted!!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    session.close()
    return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, item = item)

# JSONifying
@app.route('/restaurants/JSON/')
def allRestaurantsJSON():
    session = DBsession()
    restaurants = session.query(Restaurant).all()
    session.close()
    return jsonify(Restaurant=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>/JSON/')
def restaurantMenuJSON(restaurant_id):
    session = DBsession()
    items = session.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    session.close()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    session = DBsession()
    item = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    session.close()
    return jsonify(MenuItem=[item.serialize])

if __name__ == '__main__':
    app.secret_key = 'ultimate_key'
    app.debug = True
    app.run('127.0.0.1', '8080')