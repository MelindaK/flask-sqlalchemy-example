from flask import render_template, request

from models import Dessert, create_dessert, delete_dessert, update_dessert
from app import app


@app.route('/')
def index():

    desserts = Dessert.query.all()

    return render_template('index.html', desserts=desserts)


@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'GET':
        return render_template('add.html')

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    # Get the incoming data from the request.form dictionary.
    # The values on the right, inside get(), correspond to the 'name'
    # values in the HTML form that was submitted.

    dessert_name = request.form.get('name_field')
    dessert_price = request.form.get('price_field')
    dessert_cals = request.form.get('cals_field')

    # Now we are checking the input in create_dessert, we need to handle
    # the Exception that might happen here.

    # Wrap the thing we're trying to do in a 'try' block:
    try:
        dessert = create_dessert(dessert_name, dessert_price, dessert_cals)
        return render_template('add.html', dessert=dessert)
    except Exception as e:
        # Oh no, something went wrong!
        # We can access the error message via e.message:
        return render_template('add.html', error=e.message)


@app.route('/desserts/<id>')
def view_dessert(id):
    # if request.method == "Post":
    #     dessert_name = request.form.get('search-name')
    #     dessert = Dessert.query.filter_by(name=dessert_name)
    #     if dessert:
    #         dessert = dessert
    #         return render_template('details.html', )

    # We could define this inside its own function but it's simple enough
    # that we don't really need to.
    dessert = Dessert.query.get(id)

    return render_template('details.html', dessert=dessert)


@app.route('/delete/<id>')
def delete(id):

    message = delete_dessert(id)

    return index()  # Look at the URL bar when you do this. What happens?


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    dessert = Dessert.query.get(id)

    if request.method == 'GET':
        return render_template('update.html', dessert=dessert, id=id)

    dessert_name = request.form.get('name_field')
    dessert_price = request.form.get('price_field')
    dessert_cals = request.form.get('cals_field')

    try:
        dessert = update_dessert(id, dessert_name, dessert_price, dessert_cals)
        return index()
    except Exception as e:
        # Oh no, something went wrong!
        # We can access the error message via e.message:
        return render_template('update.html', error=e.message)
