from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create a basic SQLite database for storing patient records
def init_db():
    with sqlite3.connect('hospital.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS patients
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         age INTEGER, 
                         gender TEXT,
                         condition TEXT,
                         admitted BOOLEAN)''')
@app.route('/')
def home():
    # Fetch all patients from the database
    with sqlite3.connect('hospital.db') as conn:
        patients = conn.execute('SELECT * FROM patients').fetchall()
    return render_template('Hospital management.html', patients=patients)

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    condition = request.form['condition']
    admitted = True if request.form.get('admitted') == 'on' else False
    with sqlite3.connect('hospital.db') as conn:
        conn.execute('INSERT INTO patients (name, age, gender, condition, admitted) VALUES (?, ?, ?, ?, ?)', (name, age, gender, condition, admitted))
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_patient():
    patient_id = int(request.form['id'])
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    condition = request.form['condition']
    admitted = True if request.form.get('admitted') == 'on' else False
    with sqlite3.connect('hospital.db') as conn:
        conn.execute('UPDATE patients SET name = ?, age = ?, gender = ?, condition = ?, admitted = ? WHERE id = ?', (name, age, gender, condition, admitted, patient_id))
    return 'Patient record updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_patient():
    patient_id = int(request.form['id'])
    with sqlite3.connect('hospital.db') as conn:
        conn.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
    return 'Patient record deleted successfully!'

@app.route('/search', methods=['GET'])
def search_patients():
    search_query = request.args.get('query', '')
    with sqlite3.connect('hospital.db') as conn:
        results = conn.execute('SELECT * FROM patients WHERE name LIKE ? OR condition LIKE ?', (f'%{search_query}%', f'%{search_query}%')).fetchall()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(port=9001)
