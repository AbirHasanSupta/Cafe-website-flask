from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
from wtforms import SubmitField, StringField, SelectField
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor, CKEditorField
import random
random_cafe = ''

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'
Bootstrap5(app)
ckeditor = CKEditor(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Shop(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets?', choices=[(0), (1)], validators=[DataRequired()])
    has_toilet = SelectField('Has Toilet?', choices=[(0), (1)], validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi?', choices=[(0), (1)], validators=[DataRequired()])
    can_take_calls = SelectField('Can Take Calls?', choices=[(0), (1)], validators=[DataRequired()])
    seats = SelectField('Seats', choices=[('0-10'), ('10-20'), ('20-30'), ('30-40'), ('40-50'), ('50+')],
                        validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    description = CKEditorField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html", random_cafe=random_cafe)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/random_select')
def random_select():
    global random_cafe
    all_cafe = Cafe.query.all()
    random_cafe = random.choice(all_cafe)
    return redirect(url_for('home'))


@app.route('/add_cafe', methods=["GET", "POST"])
def add_cafe():
    cafe_form = Shop()
    if cafe_form.validate_on_submit():
        new_cafe = Cafe(
            name=cafe_form.name.data,
            map_url=cafe_form.map_url.data,
            img_url=cafe_form.img_url.data,
            location=cafe_form.location.data,
            has_sockets=cafe_form.has_sockets.data,
            has_toilet=cafe_form.has_toilet.data,
            has_wifi=cafe_form.has_wifi.data,
            can_take_calls=cafe_form.can_take_calls.data,
            seats=cafe_form.seats.data,
            coffee_price=cafe_form.coffee_price.data,
            description=cafe_form.description.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('coffee_shops'))
    return render_template("add_shop.html", form=cafe_form)


@app.route('/edit/<int:cafe_id>', methods=['GET', 'POST'])
def edit(cafe_id):
    cafe_edit = Cafe.query.get(cafe_id)
    edit_form = Shop(
        name=cafe_edit.name,
        map_url=cafe_edit.map_url,
        img_url=cafe_edit.img_url,
        location=cafe_edit.location,
        has_sockets=cafe_edit.has_sockets,
        has_toilet=cafe_edit.has_toilet,
        has_wifi=cafe_edit.has_wifi,
        can_take_calls=cafe_edit.can_take_calls,
        seats=cafe_edit.seats,
        coffee_price=cafe_edit.coffee_price,
        description=cafe_edit.description
    )
    if edit_form.validate_on_submit():
        cafe_edit.name = edit_form.name.data
        cafe_edit.map_url = edit_form.map_url.data
        cafe_edit.img_url = edit_form.img_url.data
        cafe_edit.location = edit_form.location.data
        cafe_edit.has_sockets = edit_form.has_sockets.data
        cafe_edit.has_toilet = edit_form.has_toilet.data
        cafe_edit.has_wifi = edit_form.has_wifi.data
        cafe_edit.can_take_calls = edit_form.can_take_calls.data
        cafe_edit.seats = edit_form.seats.data
        cafe_edit.coffee_price = edit_form.coffee_price.data
        cafe_edit.description = edit_form.description.data

        db.session.commit()
        return redirect(url_for('coffee_shops'))
    return render_template('add_shop.html', form=edit_form)


@app.route('/coffee_shops')
def coffee_shops():
    all_cafes = Cafe.query.all()
    return render_template("coffee_shops.html", cafes=all_cafes)


@app.route('/delete_cafe/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('coffee_shops'))


if __name__ == '__main__':
    app.run(debug=True)