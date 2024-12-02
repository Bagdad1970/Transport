import sqlite3

connection = sqlite3.connect('../transport.db')
cursor = connection.cursor()

def create_table_drivers():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DRIVERS (
        DRIVER_ID INTEGER PRIMARY KEY,
        SURNAME VARCHAR(40) NOT NULL,
        FIRSTNAME VARCHAR(40) NOT NULL,
        LASTNAME VARCHAR(100) NULL,
        BIRTHDATE DATE NOT NULL,
        PHONE_NUMBER VARCHAR(20) UNIQUE NOT NULL,
        LICENSE_NUM VARCHAR(20) UNIQUE NOT NULL,
        LICENSE_EXP DATE MOT NULL
    );
    ''')

    connection.commit()


def create_table_vehicles():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS VEHICLES (
        VEHICLE_ID INTEGER PRIMARY KEY,
        DRIVER_ID INTEGER NOT NULL,
        BRAND VARCHAR(40) NOT NULL,
        MODEL VARCHAR(40) NOT NULL,
        RELEASE_YEAR INTEGER NOT NULL,
        SERIAL_NUMBER TEXT UNIQUE UNIQUE NOT NULL,
        COLOR VARCHAR(20),
        FOREIGN KEY (DRIVER_ID) REFERENCES DRIVERS(DRIVER_ID)
    );
    ''')

    connection.commit()

def create_table_routes():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROUTES (
        ROUTE_ID INTEGER PRIMARY KEY,
        DRIVER_ID INTEGER NOT NULL,
        START_LOCATION VARCHAR(100) NOT NULL,
        END_LOCATION VARCHAR(100) NOT NULL,
        DISTANCE DECIMAL(5, 2),
        START_DATETIME TIMESTAMP NOT NULL,
        END_DATETIME TIMESTAMP NOT NULL,
        FOREIGN KEY (DRIVER_ID) REFERENCES Drivers(DRIVER_ID)
    );
    ''')

    connection.commit()


def main():
    create_table_drivers()
    create_table_vehicles()
    create_table_routes()

    connection.close()

if __name__ == "__main__":
    main()


