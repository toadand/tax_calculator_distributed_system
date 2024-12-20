import pyodbc 
import Pyro4
import json

#Configure SQL Server Details

@Pyro4.expose
class db(object):
    #Perform Database Lookup
    def __sqlQuery(self, q, arg):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                'Server='+SQL_SERVER_NAME+';'
                                'Database='+SQL_SERVER_DB+';'
                                'Trusted_Connection=yes;')

            cursor = conn.cursor()
            cursor.execute(q, arg)
            return cursor
        except:
            print('sql query failed')
            return None
        
    def getUserDetails(self, person_id):
        try:
            info = []
            cursor = self.__sqlQuery('SELECT * FROM [tfn_data].[dbo].[tfnDataTable] WHERE personId = ?', [person_id])
            for i in cursor:
               #add the grades to the list
               info.append(i[0])
            return info
        except:
            print("from Server2: SA2 -> SA1 : Sending Database Error")
            return None
    
    def addRecord(self, tfn, date, gross_pay, net_pay, tax_witheld):
        print('attempting to add record')
        try:
            cursor = self.__sqlQuery('INSERT INTO [tfn_data].[dbo].[payrollData] (TFN, DateIssued, GrossPay, NetPay, TaxWitheld) VALUES (?,?,?,?, ?)', [tfn, date, gross_pay, net_pay, tax_witheld])
            cursor.commit()
            print("from Server2: SA1 -> SA2: Record added successfully")

            return True
        except:
            print("from Server2: SA2 -> SA1 : Record upload failed")
            return False
        
    def getPayrollRecords(self, TFN):
        try:
            payrolls = []
            cursor = self.__sqlQuery('SELECT * FROM [tfn_data].[dbo].[payrollData] WHERE TFN = ?', TFN)
            for i in cursor:
               payrolls.append((i[1], i[3], i[4], i[5]))
            print("from Server2: SA1 -> SA2 : Sending payroll data")
            return payrolls
        except:
            print("from Server2: SA2 -> SA1 : Failed to retrieve payroll data from SQL Database")
            return None


#"DESKTOP-DS63712"
#"tfn_data"
# 51516
SQL_SERVER_NAME = input('Enter SQL Server Name: ')
SQL_SERVER_DB = input('Enter SQL Server Database Name: ')
SA2_PORT = int(input('Enter Server2 Port Number (#####): '))
HOST = input('Enter SA2 server IP address or localhost: ')
#Set Server2 Serving Details
#Accept RMI
taxDb=db()
daemon=Pyro4.Daemon(host=HOST, port=SA2_PORT)                
uri=daemon.register(taxDb, "taxDb")

print("-----------------------------")
print(" Server2 - Interface ")
print("-----------------------------")
print()
print("Ready. Object uri =", uri)
daemon.requestLoop()

