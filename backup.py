from models import *


def save_data():

    with open('backup.csv', 'w') as f:  # Open file 'backup.csv' for writing

        for dessert in Dessert.query.all():
            # Create a comma separated line
            line = "{},{},{}\n".format(dessert.name, dessert.price,
                                       dessert.calories)
            # Write it to the file
            f.write(line)

def load_data():

    with open('backup.csv') as f:
        for line in f:
            name, price, calories = line.split(',')
            d = Dessert(name, price, calories)
            db.session.add(d)
    db.session.commit()


if __name__=="__main__":
    # save_data()
    load_data()
