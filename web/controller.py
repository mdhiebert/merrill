from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os.path import exists
from templates.formatter import txtHeader, txtBody


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)




class testModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
class equipmentTemp(db.Model):

    UUID = db.Column(db.Integer, primary_key=True, nullable=False)
    SERIAL_NUMBER = db.Column(db.String(500))
    ITEM_DESCRIPTION = db.Column(db.String(255))
    ASSOCIATED_END_ITEM = db.Column(db.String(255))
    ITEM_QUANTITY = db.Column(db.Integer)
    DATE_CREATED = db.Column(db.DateTime, default=datetime.utcnow)
    BOX_NUMBER = db.Column(db.Integer)

    def __repr__(self):
        return '{}, {}, {}'.format(self.ITEM_QUANTITY, self.ITEM_DESCRIPTION, self.SERIAL_NUMBER)

if exists('/instance/test.db') == False:
    with app.app_context():
        db.create_all()

class adminClass:
    admin_to = 'A'
    admin_from = 'B'
    admin_packedby = 'C'

currentAdmin = adminClass()
itemsEntered = {}

@app.context_processor
def inject_admin():
    return dict(currentAdmin=currentAdmin)
@app.context_processor
def inject_items():
    return dict(itemsEntered=itemsEntered)


@app.route('/', methods=['POST', 'GET'])
def index():
    showEquipment = equipmentTemp.query.order_by(equipmentTemp.UUID).all()
    return render_template('index.html', showEquipment=showEquipment)

@app.route('/add_equipment' , methods=['POST', 'GET'])
def add_equipment():
    if request.method == 'POST':
        form_data = request.form['content']
        new_item = equipmentTemp(SERIAL_NUMBER=form_data)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR'
    else:
        return render_template('index.html')
    
@app.route('/update_admin' , methods=['POST', 'GET'])
def update_admin():
    if request.method == 'POST':
        newItems = request.form
        newItems = newItems.to_dict(flat=False)
        newItems.pop('to')
        newItems.pop('from')
        newItems.pop('packed_by')
        allDB = equipmentTemp.query.order_by(equipmentTemp.UUID).all()
        dbuuids = []
        for uuid in allDB:
            dbuuids.append(uuid.UUID)
        if 'UUID' in newItems:
            uuids = newItems['UUID']            
            print(len(dbuuids))
            for x in range(len(uuids)):
                uuids[x] = int(uuids[x])
            for y in dbuuids:
                if y not in uuids:
                    del_item = equipmentTemp.query.filter_by(UUID=y).first()
                    print(del_item)
                    try:
                        db.session.delete(del_item)
                        db.session.commit()
                    except:
                        return 'Error'
            newItems.pop('UUID')
        elif len(dbuuids) > 0:
            for x in dbuuids:
                del_item = equipmentTemp.query.filter_by(UUID=x).first()
            try:
                db.session.delete(del_item)
                db.session.commit()
            except:
                return 'Error'
        tmpItems = newItems.copy()
        curItems = newItems.copy()
        for x in newItems.keys():
            if 'new' in x:
                curItems.pop(x)
            else: 
                tmpItems.pop(x)
        ctr = 1
        lst = []
        for x,y in tmpItems.items():
            lst.append(str(y[0]))
            if ctr == 4:
                if lst[0] == ''  and (lst[1] == '' and lst[2] == ''):
                    lst = []
                    ctr = 1
                    continue                    
                newLen = len(itemsEntered) + 1
                itemsEntered[newLen]=lst
                new_item = equipmentTemp(SERIAL_NUMBER=lst[2], ITEM_DESCRIPTION=lst[1], ITEM_QUANTITY=lst[0], BOX_NUMBER=lst[3])
                try:
                    db.session.add(new_item)
                    db.session.commit()
                except:
                    return 'Error'
                lst = []
                ctr = 1
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
        return render_template('index.html')

@app.route('/generate_txt' , methods=['POST', 'GET'])
def generate_txt():
    allDB = equipmentTemp.query.order_by(equipmentTemp.BOX_NUMBER, equipmentTemp.UUID).all()
    header = txtHeader('test', currentAdmin.admin_from, currentAdmin.admin_to, currentAdmin.admin_packedby)
    outDB = {}
    for x in allDB:
        if x.BOX_NUMBER not in outDB:
            content = {x.UUID: [x.ITEM_QUANTITY, x.SERIAL_NUMBER, x.ITEM_DESCRIPTION]}
            outDB.update({x.BOX_NUMBER:content})
        else:
            content = outDB[x.BOX_NUMBER]
            ncon = [x.ITEM_QUANTITY, x.SERIAL_NUMBER, x.ITEM_DESCRIPTION]
            content[x.UUID] = ncon
            outDB.update({x.BOX_NUMBER:content})

    print(outDB)
    textContent = txtBody(outDB)    
    output = header + textContent
    with open('test_output/testoutput.txt', 'w+') as f:
        f.write('{}'.format(output))
        f.close
    return redirect('/')

@app.route('/delete_row', methods=['POST', 'GET'] )
def delete_row():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)