import json
from flask import Flask, render_template, request, redirect, url_for, Response
from lib.client_db import Client_DB
db = Client_DB('transport.db')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/driver_page')
def visit_driver_page():
    return render_template('driver_page.html')

@app.route('/vehicle_page')
def visit_vehicle_page():
    return render_template('vehicle_page.html')

@app.route('/route_page')
def visit_route_page():
    return render_template('route_page.html')

@app.route('/vehicles_list')
def vehicles_list():
    vehicles = db.fetchall('SELECT * FROM VEHICLES')
    vehicles_list = [dict(row) for row in vehicles]

    return render_template('vehicles_list.html', vehicles=vehicles_list)

@app.route('/drivers_list')
def drivers_list():
    # Получаем все строки из таблицы VEHICLES
    drivers = db.fetchall('SELECT * FROM DRIVERS')
    drivers_list = [dict(row) for row in drivers]

    return render_template('drivers_list.html', drivers=drivers_list)

@app.route('/routes_list')
def routes_list():
    routes = db.fetchall('SELECT * FROM ROUTES')
    routes_list = [dict(row) for row in routes]

    return render_template('routes_list.html', routes=routes_list)


@app.route('/driver_form', methods=['GET', 'POST'])
def insert_into_drivers():
    if request.method == 'POST':
        surname = request.form['surname']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        phone_number = request.form['phone_number']
        license_num = request.form['license_num']
        license_exp = request.form['license_exp']

        db.execute('INSERT INTO DRIVERS (SURNAME, FIRSTNAME, LASTNAME, BIRTHDATE, PHONE_NUMBER, LICENSE_NUM, LICENSE_EXP) VALUES  (?, ?, ?, ?, ?, ?, ?)', (surname, firstname, lastname, birthdate, phone_number, license_num, license_exp))

        return redirect(url_for('success'))

    return render_template('driver_form.html')

@app.route('/vehicle_form', methods=['GET', 'POST'])
def insert_into_vehicles():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        brand = request.form['brand']
        model = request.form['model']
        release_year = request.form['release_year']
        serial_number = request.form['serial_number']
        color = request.form['color']

        db.execute('INSERT INTO VEHICLES (DRIVER_ID, BRAND, MODEL, RELEASE_YEAR, SERIAL_NUMBER, COLOR) VALUES (?, ?, ?, ?, ?, ?)', (driver_id, brand, model, release_year, serial_number, color))

        return redirect(url_for('success'))

    return render_template('vehicle_form.html')

@app.route('/route_form', methods=['GET', 'POST'])
def insert_into_routes():
    if request.method == 'POST':
        driver_id = request.form['driver_id']
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        distance = request.form['distance']
        start_datetime = request.form['start_datetime']
        end_datetime = request.form['end_datetime']

        db.execute('INSERT INTO ROUTES (DRIVER_ID, START_LOCATION, END_LOCATION, DISTANCE, START_DATETIME, END_DATETIME) VALUES (?, ?, ?, ?, ?, ?)', (driver_id, start_location, end_location, distance, start_datetime, end_datetime))

        return redirect(url_for('success'))

    return render_template('route_form.html')

@app.route('/export_vehicles')
def export_vehicles():
    vehicles = db.fetchall('SELECT * FROM VEHICLES')

    if not vehicles:
        return "<h3>Нет данных для экспорта</h3>", 404

    vehicles_list = [dict(row) for row in vehicles]

    return Response(
        json.dumps(vehicles_list, indent=4, ensure_ascii=False),  # ensure_ascii=False для поддержки Unicode
        mimetype='application/json',
        headers={"Content-Disposition": "attachment;filename=vehicles.json"}
    )

@app.route('/import_vehicles', methods=['GET', 'POST'])
def import_vehicles():
    if request.method == 'POST':
        try:
            json_file = request.files['json_file']
            if not json_file:
                return "<h3>Ошибка: файл не предоставлен</h3>", 400

            data = json.load(json_file)

            for vehicle in data:
                if not all(key in vehicle for key in ['DRIVER_ID', 'BRAND', 'MODEL', 'RELEASE_YEAR', 'SERIAL_NUMBER', 'COLOR']):
                    return "<h3>Ошибка: некорректный формат данных</h3>", 400

                db.execute(
                    '''INSERT INTO VEHICLES (DRIVER_ID, BRAND, MODEL, RELEASE_YEAR, SERIAL_NUMBER, COLOR) 
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (vehicle['DRIVER_ID'], vehicle['BRAND'], vehicle['MODEL'], vehicle['RELEASE_YEAR'],
                     vehicle['SERIAL_NUMBER'], vehicle['COLOR'])
                )

            return redirect(url_for('success'))
        except json.JSONDecodeError:
            return "<h3>Ошибка: некорректный JSON-файл</h3>", 400
        except Exception as e:
            return f"<h3>Ошибка: {e}</h3>", 500

    return render_template('import_vehicles.html')

@app.route('/export_routes')
def export_routes():
    routes = db.fetchall('SELECT * FROM ROUTES')

    if not routes:
        return "<h3>Нет данных для экспорта</h3>", 404

    routes_list = [dict(row) for row in routes]

    return Response(
        json.dumps(routes_list, indent=4, ensure_ascii=False),
        mimetype='application/json',
        headers={"Content-Disposition": "attachment;filename=routes.json"}
    )


@app.route('/import_routes', methods=['GET', 'POST'])
def import_routes():
    if request.method == 'POST':
        try:
            json_file = request.files['json_file']
            if not json_file:
                return "<h3>Ошибка: файл не предоставлен</h3>", 400

            data = json.load(json_file)

            for route in data:
                if not all(key in route for key in ['DRIVER_ID', 'START_LOCATION', 'END_LOCATION', 'DISTANCE', 'START_DATETIME', 'END_DATETIME']):
                    return "<h3>Ошибка: некорректный формат данных</h3>", 400

                db.execute(
                    '''INSERT INTO ROUTES (DRIVER_ID, START_LOCATION, END_LOCATION, DISTANCE, START_DATETIME, END_DATETIME) 
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (route['DRIVER_ID'], route['START_LOCATION'], route['END_LOCATION'], route['DISTANCE'],
                     route['START_DATETIME'], route['END_DATETIME'])
                )

            return redirect(url_for('success'))
        except json.JSONDecodeError:
            return "<h3>Ошибка: некорректный JSON-файл</h3>", 400
        except Exception as e:
            return f"<h3>Ошибка: {e}</h3>", 500

    return render_template('import_routes.html')

@app.route('/export_drivers')
def export_drivers():
    drivers = db.fetchall('SELECT * FROM DRIVERS')

    if not drivers:
        return "<h3>Нет данных для экспорта</h3>", 404

    drivers_list = [dict(row) for row in drivers]

    return Response(
        json.dumps(drivers_list, indent=4, ensure_ascii=False),
        mimetype='application/json',
        headers={"Content-Disposition": "attachment;filename=drivers.json"}
    )

@app.route('/import_drivers', methods=['GET', 'POST'])
def import_drivers():
    if request.method == 'POST':
        try:
            json_file = request.files['json_file']
            if not json_file:
                return "<h3>Ошибка: файл не предоставлен</h3>", 400

            data = json.load(json_file)

            for driver in data:
                if not all(key in driver for key in ['SURNAME', 'FIRSTNAME', 'LASTNAME', 'BIRTHDATE', 'PHONE_NUMBER', 'LICENSE_NUM', 'LICENSE_EXP']):
                    return "<h3>Ошибка: некорректный формат данных</h3>", 400

                db.execute(
                    '''INSERT INTO DRIVERS (SURNAME, FIRSTNAME, LASTNAME, BIRTHDATE, PHONE_NUMBER, LICENSE_NUM, LICENSE_EXP)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (driver['SURNAME'], driver['FIRSTNAME'], driver['LASTNAME'], driver['BIRTHDATE'],
                     driver['BIRTHDATE'], driver['LICENSE_NUM'], driver['LICENSE_EXP'])
                )

            return redirect(url_for('success'))
        except json.JSONDecodeError:
            return "<h3>Ошибка: некорректный JSON-файл</h3>", 400
        except Exception as e:
            return f"<h3>Ошибка: {e}</h3>", 500

    return render_template('import_drivers.html')

@app.route('/success')
def success():
    return "<h3>Данные успешно добавлены!</h3>"

if __name__ == '__main__':
    app.run(debug=True)
