from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from templates.formatter import TxtOutput

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class testModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
class equipmentBii(db.Model):

    UUID = db.Column(db.Integer, primary_key=True, nullable=False)
    SERIAL_NUMBER = db.Column(db.String(50))
    ITEM_DESCRIPTION = db.Column(db.String(255))
    ASSOCIATED_END_ITEM = db.Column(db.String(255))
    ITEM_QUANTITY = db.Column(db.Integer)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id    

class adminClass:
    admin_to = 'A'
    admin_from = 'B'
    admin_packedby = 'C'

currentAdmin = adminClass()
itemsEntered = {}
testDict = {}

@app.context_processor
def inject_admin():
    return dict(currentAdmin=currentAdmin)
def inject_items():
    return dict(itemsEntered=itemsEntered)

@app.route('/', methods=['POST', 'GET'])
def index():
    showEquipment = equipmentBii.query.order_by(equipmentBii.SERIAL_NUMBER).all()
    return render_template('index.html', itemsEntered=itemsEntered)

@app.route('/add_equipment' , methods=['POST', 'GET'])
def add_equipment():
    if request.method == 'POST':
        form_data = request.form['content']
        new_item = equipmentBii(SERIAL_NUMBER=form_data)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR'
    else:
        showEquipment = equipmentBii.query.order_by(equipmentBii.SERIAL_NUMBER).all()
        return render_template('index.html', showEquipment=showEquipment)
    
@app.route('/update_admin' , methods=['POST', 'GET'])
def update_admin():
    if request.method == 'POST':
        newItems = request.form
        newItems = newItems.to_dict(flat=False)
        newItems.pop('to')
        newItems.pop('from')
        newItems.pop('packed_by')
        ctr = 1
        lst = []
        for x,y in newItems.items():
            lst.append(str(y[0]))
            if ctr == 3:
                if lst[0] == ''  and (lst[1] == '' and lst[2] == ''):
                    lst = []
                    ctr = 1
                    continue                    
                newLen = len(itemsEntered) + 1
                itemsEntered[newLen]=lst
                lst = []
                ctr = 1
                print(itemsEntered)
                continue  
            ctr = ctr + 1
        if request.form['to'] != '':
            currentAdmin.admin_to = request.form['to']
        if request.form['from'] != '':
            currentAdmin.admin_from = request.form['from']
        if request.form['packed_by'] != '':
            currentAdmin.admin_packedby = request.form['packed_by']
        try:
            return redirect('/')
        except:
            return 'ERROR'
    else:
        showEquipment = equipmentBii.query.order_by(equipmentBii.SERIAL_NUMBER).all()
        return render_template('index.html', showEquipment=showEquipment)

@app.route('/generate_txt' , methods=['POST', 'GET'])
def generate_txt():
    o = TxtOutput('test', currentAdmin.admin_from, currentAdmin.admin_to, currentAdmin.admin_packedby, itemsEntered)
    o.fromForm()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)