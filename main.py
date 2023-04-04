from PyQt5 import QtWidgets

import sys
# import threading
import datetime
import sqlite3
from client.GUI.dropbox import Ui_MainWindow as ud
from client.GUI.login import Ui_MainWindow as login
from client.GUI.admin import Ui_MainWindow as adm
from client.GUI.itscorrect import Ui_MainWindow as pay
from client.GUI.mainwindow import Ui_mainWindow as mw
# from client.checkDB import create_db
from client.handlers.table import Table
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super(MainWindow, self).__init__()
                self.ui = login()
                self.ui.setupUi(self)
                self.main_window()
                self.ui.pushButton.clicked.connect(self.btn_clicked)
                self.ui.pushButton_2.clicked.connect(self.btn_registration)


        def main_window(self):
                self.show()

        def btn_registration(self):
                self.registrationUi()

        def get_adress_id(self):
                return self.ui.lineEdit.text()

        def btn_clicked(self):
                adress_id = self.ui.lineEdit.text()
                password = self.ui.lineEdit_2.text()
                self.button_presses = 0
                self.variables_from_gui = None

                if adress_id == 'avoid' and password == 'aoijoinf32jIJHIoh423iofsdfjo4*2':
                        self.adm_ui_show()
                else:
                        self.connection = sqlite3.connect('paymentservices.sqlite')
                        self.cursor = self.connection.cursor()
                        info_check = 0
                        users = f"SELECT * FROM registration"
                        for raw in self.cursor.execute(users):
                                if adress_id in raw and password in raw:
                                        info_check += 1
                        if info_check == 1:  
                                alert = QMessageBox()
                                text = f"""
                                Information is correct. check your information.                    
                                """
                                alert.setText(text)
                                self.ui.label.adjustSize()
                                alert.exec()
                                self.second_ui_show()
                                alert = QMessageBox()
                                text = f"""
                                Enter current counter value
                                We calculate your debt
                                And u can pay, just click on the button 'Pay'                    
                                """
                                alert.setText(text)
                                self.ui.label.adjustSize()
                                alert.exec()
                                self.connection.commit()
                                self.connection.close()
                        else:
                                alert = QMessageBox()
                                text = f"""
                                We don`t have this user in database.
                                Or text is empty.
                                Push button registration please.             
                                And registration your adress_id                              
                                """
                                alert.setText(text)
                                alert.exec()


        def second_ui_show(self):
                self.w = SecondUi(self.get_adress_id())
                self.w.show()
                self.hide()
                

        def registrationUi(self):
                self.w = MyWindow()
                self.w.show()
                self.hide()


        def adm_ui_show(self):
                self.w = AdminUi()
                self.w.show()
                self.hide()



class SecondUi(QtWidgets.QMainWindow):
        def __init__(self,adress_id: str):
                super(SecondUi, self).__init__()
                self.ui = ud()
                self.ui.setupUi(self)
                self.adress_id = adress_id
                self.ui.dateEdit.setDate(datetime.date.today())
                self.ui.label_10.setText(' uah')
                self.ui.pushButton.clicked.connect(self.btn_click)
                self.ui.pushButton_2.clicked.connect(self.payment_ui_show)
                self.connection = sqlite3.connect('paymentservices.sqlite')
                self.cursor = self.connection.cursor()
                # #print(self.adress_id)
                users = f"SELECT * FROM payment_info WHERE adress_id = '{self.adress_id}'"
                for raw in self.cursor.execute(users):
                        # #print(raw)
                        if self.adress_id in raw:
                                self.ui.label_9.setText('Its card payment number\n'+'4141144151646053'+'\n Gas eval in m³'+'\n Water eval in m³'+'\n Electrecity eval in kW*h'+'\n Enter all symbols without "0"')
                                self.ui.label_5.setText(str('%.0f' % raw[2]))
                                self.ui.label_6.setText(str('%.0f' % raw[3]))
                                self.ui.label_7.setText(str('%.0f' % raw[4]))
                                self.ui.label_8.setText(str('%.1f' % raw[5]))
                                self.connection.commit()
                                self.connection.close()
                                break


        def get_adress_id(self):
                return self.adress_id


        def payment_ui_show(self):
                self.w = Payment(self.get_adress_id())
                self.w.show()
                self.hide()
                alert = QMessageBox()
                text = f"""
                Enter the amount you paid.
                We will check the receipt later.                             
                """
                alert.setText(text)
                alert.exec()



        def btn_click(self):
                new_gas = self.ui.lineEdit.text()
                new_water = self.ui.lineEdit_2.text()
                new_electrecity = self.ui.lineEdit_3.text()
                gas = self.ui.label_5.text()
                water = self.ui.label_6.text()
                electrecity = self.ui.label_7.text()
                debt = float(self.ui.label_8.text())
                try:
                        if len(new_gas) > 7 or len(new_water) > 7 or len(new_electrecity) > 6:
                                alert = QMessageBox()
                                text = f"""
                                You entered encorrect value.
                                Or text is empty.
                                Enter correct value and press button again.                                           
                                """
                                alert.setText(text)
                                alert.exec()
                        elif float(new_gas) < float(gas) or float(new_water) < float(water) or float(new_electrecity) < float(electrecity):
                                alert = QMessageBox()
                                text = f"""
                                Current counter can`t be smaller than old
                                Please enter correct value and press button again.                                            
                                """
                                alert.setText(text)
                                alert.exec()
                        else:
                                self.connection = sqlite3.connect('paymentservices.sqlite')
                                self.cursor = self.connection.cursor()
                                self.ui.label_5.setText(str(new_gas))
                                self.ui.label_6.setText(str(new_water))
                                self.ui.label_7.setText(str(new_electrecity))
                                # #print(type(new_water), type(water))
                                debt_water = (float(new_water)-float(water))*17.916
                                # #print(debt_water)
                                debt_electrecity = (float(new_electrecity)-float(electrecity))*1.68
                                #print(debt_electrecity)
                                debt_gas = (float(new_gas)-float(gas))*6.33
                                # #print(debt_gas)
                                # #print(debt_water,'water', debt_electrecity,'eletcricity', debt_gas,'gas')
                                new_debt = debt_gas + debt_electrecity + debt_water
                                # #print(new_debt,'to rr',debt)
                                new_debt = '%.1f' % new_debt
                                self.ui.label_8.setText(str(float(new_debt)+float(debt)))
                                #print(new_debt, debt)
                                self.cursor.execute(f"""
                                                        UPDATE payment_info
                                                        SET 
                                                                counter_water = {float(new_water)},
                                                                counter_gas = {float(new_gas)},
                                                                counter_electricity = {float(new_electrecity)},
                                                                debt = {float(new_debt)+float(debt)}
                                                        WHERE adress_id = '{self.adress_id}'
                                                """)
                                self.connection.commit()
                                self.connection.close()
                                alert = QMessageBox()
                                text = f"""
                                New counter added correctly
                                Your adress_ID: {self.adress_id}                     
                                """
                                alert.setText(text)
                                alert.exec()
                                self.ui.lineEdit.setText('')
                                self.ui.lineEdit_2.setText('')
                                self.ui.lineEdit_3.setText('')

                except ValueError as ve:
                        #print(ve)
                        alert = QMessageBox()
                        text = f"""
                        You entered encorrect value.
                        Or text is empty.
                        Enter correct value and press button again.                                           
                        """
                        alert.setText(text)
                        self.ui.label.adjustSize()
                        alert.exec()


class AdminUi(QtWidgets.QMainWindow):
        def __init__(self):
                super(AdminUi, self).__init__()
                self.ui = adm()
                self.ui.setupUi(self)
                self.ui.pushButton.clicked.connect(self.check_database)
                self.ui.pushButton_2.clicked.connect(self.delete_info)
                self.ui.pushButton_3.clicked.connect(self.second_ui_show)


        def check_database(self):
                self.w = Table()
                self.w.show()
                # self.hide()


        def delete_info(self):
                self.connection = sqlite3.connect('paymentservices.sqlite')
                self.cursor = self.connection.cursor()
                self.user_id = self.ui.lineEdit.text()
                #print(self.user_id)
                self.cursor.execute(f"DELETE FROM users WHERE adress_id = '{self.user_id}'")
                self.cursor.execute(f"DELETE FROM payment_info WHERE adress_id = '{self.user_id}'")
                self.cursor.execute(f"DELETE FROM adress WHERE adress_id = '{self.user_id}'")
                self.cursor.execute(f"DELETE FROM registration WHERE adress_id = '{self.user_id}'")
                self.cursor.execute(f"DELETE FROM pay_of_user WHERE adress_id = '{self.user_id}'")
                self.connection.commit()
                self.connection.close()
                alert = QMessageBox()
                text = f"""
                User with {self.user_id} deleted successfully                      
                """
                alert.setText(text)
                alert.exec()
                self.ui.lineEdit.setText('')

        def second_ui_show(self):
                self.w = MyWindow()
                self.w.show()
                self.hide()


# class Controller(threading.Thread):

#     def __init__(self):
#         super(Controller, self).__init__(daemon = True)


class MyWindow(QtWidgets.QMainWindow):

        def __init__(self):
                super(MyWindow, self).__init__()
                self.list_info = None
                self.ui = mw()
                self.ui.setupUi(self)
                # connect click signal in btnClicked
                self.ui.pushButton.clicked.connect(self.btn_clicked)
                self.ui.pushButton_2.clicked.connect(self.back_button)
                self.ui.dateEdit.setDate(datetime.date.today())


        def set_list_info(self, list_info: str):
                self.list_info = list_info


        def btn_clicked(self):
                secondname = self.ui.lineEdit_2.text()
                firstname = self.ui.lineEdit.text()
                lastname = self.ui.lineEdit_3.text()
                street = self.ui.lineEdit_4.text()
                number = self.ui.lineEdit_5.text()
                floor = self.ui.lineEdit_6.text()
                apartment = self.ui.lineEdit_7.text()
                city = self.ui.lineEdit_8.text()
                password = self.ui.lineEdit_9.text()
                adress_id = street+number+floor+apartment
                date1 = self.ui.dateEdit.text()
                #print(adress_id,"this is your login and adress_id")
                label_text = [secondname, firstname, lastname,street,number,floor,apartment,city,password,adress_id,date1]

                for text in label_text:
                        if len(text) == 0:
                                alert = QMessageBox()
                                text = f"""
                                Information is empty. Please try again.                    
                                """
                                alert.setText(text)
                                self.ui.label.adjustSize()
                                alert.exec()
                                return
                        
  
                self.connection = sqlite3.connect('paymentservices.sqlite')
                self.cursor = self.connection.cursor()
                users = f"SELECT * FROM users WHERE adress_id = '{adress_id}'"
                user = self.cursor.execute(users).fetchone()
                # #print(list_inf)
                if user:
                        alert = QMessageBox()
                        text = f"""
                        This user now registered. 
                        Please login in main window                    
                        """
                        alert.setText(text)
                        self.ui.label.adjustSize()
                        alert.exec()
                else:  
                        self.cursor.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, ?)", (firstname,secondname,lastname,adress_id,password,date1))
                        self.cursor.execute("INSERT INTO payment_info VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (adress_id,0,0,0,0,4141144151646053,date1,adress_id))
                        self.cursor.execute("INSERT INTO registration VALUES (NULL, ?, ?, ?, ?)", (adress_id,adress_id,password,date1))
                        self.cursor.execute("INSERT INTO adress VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (adress_id,city,street,number,floor,apartment,date1))
                        alert = QMessageBox()
                        text = f"""
                        Registration successful. 
                        Please enter in your account in main window.
                        Your adress_ID: {adress_id}                     
                        """
                        alert.setText(text)
                        self.ui.label.adjustSize()
                        alert.exec()
                        self.connection.commit()
                        self.connection.close()
                        self.back_button()


        def back_button(self):
                self.w = MainWindow()
                self.w.show()
                self.hide()


class Payment(QtWidgets.QMainWindow):
        def __init__(self,adress_id: str):
                super(Payment, self).__init__()
                self.ui = pay()
                self.ui.setupUi(self)
                self.adress_id = adress_id
                self.ui.pushButton.clicked.connect(self.back_button)
                self.ui.pushButton_2.clicked.connect(self.pay_debt)


        def get_adress_id(self):
                return self.adress_id


        def back_button(self):
                self.w = SecondUi(self.get_adress_id())
                self.w.show()
                self.hide()


        def pay_debt(self):
                try:
                        sum_debt = self.ui.lineEdit.text()
                        self.connection = sqlite3.connect('paymentservices.sqlite')
                        self.cursor = self.connection.cursor()
                        users = f"SELECT debt FROM payment_info WHERE adress_id = '{self.adress_id}'"
                        for raw in self.cursor.execute(users):
                                #print(raw[0])
                                pass
                        result = raw[0] - float(sum_debt)
                        if float(sum_debt) > raw[0]:
                                alert = QMessageBox()
                                text_full = "You have paid off your debt in full\n"
                                alert.setText(text_full)
                                alert.exec()
                        self.cursor.execute(f"""
                                                UPDATE payment_info
                                                SET debt = {float(result)}
                                                WHERE adress_id = '{self.adress_id}'
                        """)
                        self.cursor.execute("INSERT INTO pay_of_user VALUES (NULL, ?, ?, ?)", (self.adress_id, float(sum_debt), datetime.datetime.today()))
                        alert = QMessageBox()
                        text = f"""
                        We have received payment information for {self.adress_id}.
                        The information is being processed.
                        You can see the result in real time in the main window.                             
                        """
                        alert.setText(text)
                        alert.exec()
                        self.ui.lineEdit.setText('')

                        self.connection.commit()
                        self.connection.close()
                except ValueError as ve:
                        #print(ve)
                        alert = QMessageBox()
                        text = f"""
                        You entered encorrect value.
                        Or text is empty.
                        Enter correct value and press button again.                                           
                        """
                        alert.setText(text)
                        alert.exec()

if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        w = MainWindow()
        app.exec()