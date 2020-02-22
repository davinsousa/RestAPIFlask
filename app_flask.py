from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'appflask',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(dict(
    SECRET_KEY="1234",
    WTF_CSRF_SECRET_KEY="1234"
))

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#class with table information - basically 4 columns (ID, lender, borrower, amount)
class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer(), primary_key=True)
    lender = db.Column(db.String(80))
    borrower = db.Column(db.String(255))
    amount=db.Column(db.Numeric())

    def __init__(self, lender, borrower, amount):
        self.lender = lender
        self.borrower=borrower
        self.amount=amount


#Form to get information about a new transaction
class TransactionForm(FlaskForm):
    lender = StringField('Lender', validators=[DataRequired()])
    borrower=StringField('Borrower', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])

#index route
@app.route('/')
def welcome():
    return render_template("index.html")

#route to print all the transactions into db
@app.route('/transactions', methods=['GET', 'POST'])
def viewtransactions():
    trans = Transactions.query.all()
    return render_template('viewtransactions.html', trans=trans)

#route to add new transaction
@app.route('/add', methods=['GET', 'POST'])
def add():
    t_form = TransactionForm()
    if request.method == 'POST':
        nt = Transactions(
            t_form.lender.data,
            t_form.borrower.data,
            t_form.amount.data
        )
        db.session.add(nt)
        db.session.commit()
        return redirect(url_for('viewtransactions'))
        
    return render_template('transaction.html', t_form=t_form)   

if __name__ == '__main__':
    manager.run()