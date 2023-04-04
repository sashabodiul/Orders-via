CREATE_PAYMENT_INFO ="""
            CREATE TABLE IF NOT EXISTS payment_info (    
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adress_id VARCHAR(100),
            counter_water FLOAT,
            counter_gas FLOAT,
            counter_electricity FLOAT,
            debt FLOAT,
            payment_adress VARCHAR(20) DEFAULT '4141144151646053',
            date_add DATETIME,
            latest_payment DATETIME
        );"""

CREATE_ADRESS ="""
            CREATE TABLE IF NOT EXISTS adress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adress_id VARCHAR(100),
            city VARCHAR(50),
            street VARCHAR(50),
            number_street VARCHAR(50),
            floor VARCHAR(50),
            apartment VARCHAR(50),
            created_date DATETIME
        );"""

CREATE_USER ="""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            firstname VARCHAR(50), 
            secondname VARCHAR(50), 
            lastname VARCHAR(50),
            adress_id VARCHAR(100), 
            password VARCHAR(50),
            created_date DATETIME
        );"""

CREATE_REG ="""
            CREATE TABLE IF NOT EXISTS registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            login_user VARCHAR(50), 
            adress_id VARCHAR(50), 
            password VARCHAR(50),
            created_date DATETIME
        );"""

PAY_OF_USER = """
            CREATE TABLE IF NOT EXISTS pay_of_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            adress_id VARCHAR(50), 
            sum_of_pay VARCHAR(50),
            created_date DATETIME
        );"""