import sqlite3
import texts as texts

# import datetime


connection = sqlite3.connect('paymentservices.sqlite')
cursor = connection.cursor()


def create_db():
    cursor.execute(texts.CREATE_USER)
    cursor.execute(texts.CREATE_PAYMENT_INFO)
    cursor.execute(texts.CREATE_ADRESS)
    cursor.execute(texts.PAY_OF_USER)
    cursor.execute(texts.CREATE_REG)


def set_db_info():
    
    cursor.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?)", ('firstname','secondname','lastname','test','password','date1'))
    cursor.execute("INSERT INTO payment_info VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", ('test',0,0,0,0,4141144151646053,'date1','test_date'))
    cursor.execute("INSERT INTO registration VALUES (NULL, ?, ?, ?, ?)", ('test','test','password','date1'))
    cursor.execute("INSERT INTO adress VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", ('test','city','street','number','floor','apartment','date1'))
# set_db_info()
# adress = "SELECT * FROM adress"
# payment_adress = "SELECT * FROM payment_info"
# users = "SELECT * FROM users"
# registration = "SELECT * FROM registration"
# pays = "SELECT * FROM pay_of_user"
# for raw in cursor.execute(users):
#     print(raw)
create_db()
connection.commit()
connection.close()

# params = (userName, password, confirmPassword, firstName, lastName,
#           companyName, email, phoneNumber, addressLine1, addressLine2, 
#           addressLine3, zipCode, province, country, regDate)

