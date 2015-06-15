from flask import render_template, request, session

from models import Dessert, User, create_dessert, delete_dessert, update_dessert, log_out
from app import app


@app.route('/')
def login():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        return render_template('menu.html', desserts=user.desserts)
    else:
        return render_template('login.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():

    user_entry = request.form.get('username')
    password_entry = request.form.get('password')

    user = User.query.filter_by(username=user_entry).first()

    if user:
        if user.password == password_entry:
            session["user_id"] = user.id
            return render_template('menu.html', desserts=user.desserts)


# Secret Key
app.secret_key = 'q<pskdn73&kj2d$'


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')

    dessert_name = request.form.get('name_field')
    dessert_price = request.form.get('price_field')
    dessert_cals = request.form.get('cals_field')
    user_id = session.get("user_id")

    if user_id:
        try:
            dessert = create_dessert(dessert_name, dessert_price, dessert_cals, user_id)
            return render_template("add.html", dessert=dessert)
        except Exception as e:
            return render_template('add.html', error=e.message)
    else:
        return render_template('login.html')


@app.route('/desserts/<id>')
def view_dessert(id):

    dessert = Dessert.query.get(id)
    return render_template('details.html', dessert=dessert)


@app.route('/desserts/<id>', methods="[POST]")
def search_dessert():
    dessert_name = request.form.get('search-name')
    dessert = Dessert.query.filter_by(name=dessert_name).first()
    dessert_id = dessert.id

    return render_template('details.html', dessert=dessert, dessert_id=dessert_id)


@app.route('/delete/<id>')
def delete(id):

    message = delete_dessert(id)

    return menu()  # Look at the URL bar when you do this. What happens?


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    dessert = Dessert.query.get(id)

    if request.method == 'GET':
        return render_template('update.html', dessert=dessert, id=id)

    dessert_name = request.form.get('name_field')
    dessert_price = request.form.get('price_field')
    dessert_cals = request.form.get('cals_field')

    # Figure out how to not show the success message before updating

    try:
        dessert = update_dessert(id, dessert_name, dessert_price, dessert_cals)
        return login()
    except Exception as e:
        # Oh no, something went wrong!
        # We can access the error message via e.message:
        return render_template('update.html', error=e.message)

@app.route('/login')
def logout():
    user_id = session.get("user_id")
    user_id = log_out(user_id)
    return render_template('login.html')
