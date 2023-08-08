from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IT_log.db'

db = SQLAlchemy(app)

class device_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    e_code = db.Column(db.String(200), nullable=False)
    e_name = db.Column(db.String(200), nullable=False)
    device_type = db.Column(db.String(200), nullable=False)
    borrow_return = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        e_code = request.form['employee_code']
        e_name = request.form['employee_name']
        device_type = request.form['device_type']
        borrow_return = request.form['borrow_return']
        new_device = device_log(e_code=e_code, e_name=e_name, device_type=device_type, borrow_return=borrow_return)

        try:
            db.session.add(new_device)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding your task'
        
    else:
        tasks = device_log.query.order_by(device_log.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    log_to_delete = device_log.query.get_or_404(id)

    try:
        db.session.delete(log_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem deleting'


if __name__ == "__main__":
    app.run(debug=True)