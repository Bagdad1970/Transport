import sqlite3

connection = sqlite3.connect('transport.db')
cursor = connection.cursor()

def insert_into_drivers():
    cursor.execute('''
        INSERT INTO DRIVERS (SURNAME, FIRSTNAME, LASTNAME, BIRTHDATE, PHONE_NUMBER, LICENSE_NUM, LICENSE_EXP)
        VALUES 
        ('Иванов', 'Иван', 'Петрович', '1980-01-15', '+79991234567', 'A12345678', '2025-01-15'),
        ('Смирнов', 'Пётр', 'Александрович', '1985-05-22', '+79992345678', 'B23456789', '2027-05-22'),
        ('Кузнецова', 'Елена', 'Ивановна', '1990-09-10', '+79993456789', 'C34567890', '2026-09-10'),
        ('Соколова', 'Мария', 'Сергеевна', '1992-03-05', '+79994567890', 'D45678901', '2028-03-05'),
        ('Попов', 'Алексей', 'Владимирович', '1988-07-18', '+79995678901', 'E56789012', '2024-07-18');
    ''')

    connection.commit()

def insert_into_routes():
    cursor.execute('''
        INSERT INTO ROUTES (DRIVER_ID, START_LOCATION, END_LOCATION, DISTANCE, START_DATETIME, END_DATETIME)
        VALUES 
        (1, 'Москва', 'Санкт-Петербург', 712.5, '2023-10-01 08:00:00', '2023-10-01 16:30:00'),
        (2, 'Екатеринбург', 'Пермь', 350.0, '2023-10-02 09:00:00', '2023-10-02 13:00:00'),
        (3, 'Казань', 'Нижний Новгород', 396.2, '2023-10-03 07:30:00', '2023-10-03 12:15:00'),
        (4, 'Самара', 'Тольятти', 89.4, '2023-10-04 10:00:00', '2023-10-04 11:30:00'),
        (5, 'Новосибирск', 'Томск', 265.7, '2023-10-05 06:45:00', '2023-10-05 10:00:00');
    ''')

    connection.commit()

def insert_into_vehicles():
    cursor.execute('''
        INSERT INTO VEHICLES (DRIVER_ID, BRAND, MODEL, RELEASE_YEAR, SERIAL_NUMBER, COLOR)
        VALUES 
        (1, 'Lada', 'Vesta', 2018, 'Z12XY34F', 'Red'),
        (2, 'Kia', 'Ceed', 2020, 'A45BC67D', 'Blue'),
        (3, 'Toyota', 'Camry', 2019, 'B89DF23H', 'White'),
        (4, 'Hyundai', 'Solaris', 2021, 'C56EF78I', 'Black'),
        (5, 'Ford', 'Focus', 2017, 'D12GH45J', 'Silver');
    ''')

    connection.commit()

def main():
    insert_into_drivers()
    insert_into_routes()
    insert_into_vehicles()

if __name__ == '__main__':
    main()