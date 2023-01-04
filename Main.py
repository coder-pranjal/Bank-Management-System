#creating database
import mysql.connector as sql
from random import randint
mydb=sql.connect (host="localhost",user="root", passwd="12345", database="kv_bank")
if mydb.is_connected():
    print("Succesfully connected to KV Bank Database\n\n")

#creating required tables 
mycursor=mydb.cursor()
#mycursor.execute("create table if not exists bank_master(acno char(4) primary key,name varchar(30),city char(20),mobileno char(10),balance int(6))")
#mycursor.execute("create table if not exists banktrans(acno char (4),amount int(6),dot date,ttype char(1),foreign key (acno) references bank_master(acno))")


#mydb.commit()

print("\t\t****WELCOME TO KV BANK MANAGEMENT SYSTEM****\n\n")

def menu():
    print("You are identified as:")
    print("1. Admin")
    print("2. Customer")
    return  int(input(""))

def admin():
    password = (str(input("Enter password:")),)
    mycursor.execute("select * from admin where Password=%s",password)
    pswd = mycursor.fetchall()
    if(len(pswd)==0):
        print("Invalid password!!\n\n")
        main()
    else:
        print("## You are now in admin mode ## \n\n")
        adminOperations()

 def adminOperations():
     print("1. Display all accounts")
    

def customer():
    print("\n## Welcome to KV Bank ## \n\n")
    print("1. Existing Customer")
    print("2. New Customer")
    ch=int(input(""))
    if(ch==1):
        existingCustomer()
    elif(ch==2):
        newCustomer()
    else:
       print("Invalid Choice\: Please enter valid choice\n\n")
       main()
 
    
def existingAccountOperations(customer,username, password):
    print("1.View Account Details")
    print("2.View current Balance")
    print("3.Deposit amount")
    print("4.Withdraw amount")
    print("5. Logout")
    ch=int(input("Enter your choice:"))
    match ch:
        case 1:
            print("Account no.:",customer[0])
            print("Customer username:",customer[3])
            print("Customer Name:",customer[2],customer[1])
            print("Customer Mobile no.:",customer[5])
            print("Current Balance:",customer[6])
            existingAccountOperations(customer,username, password)
        case 2:
            print("Your current balance is:",customer[6],"\n")
            existingAccountOperations(customer,username, password)
        case 3:
            amount = int(input("Enter amount to be deposited:"))
            deposited_amount= amount
            amount+=customer[6]
            mycursor.execute("update customer set Balance=%s where Username=%s and Password=%s",(amount,username,password))
            customer[6]= amount
            mydb.commit()
            print("Rs.",deposited_amount,"has been successfully deposited.")
            print("Your current balance is:",amount)

            existingAccountOperations(customer,username, password)

        case 4:
            amount = int(input("Enter amount to withdraw:"))
            withdrawn_amount= amount
            if(customer[6]==500):
                print("Your current balance is the minimum balance. Invalid operation!! ")
            elif(amount>customer[6]):
                print("Your entered amount is greater than the current balance. Invalid operation!! ")
            elif(customer[6]-amount<500):
                print("Your cannot withdraw Rs.",amount, "Minimum balance of Rs.500 is required. Invalid operation!! ")
            else:
                amount= customer[6]-amount
                mycursor.execute("update customer set Balance=%s where Username=%s and Password=%s",(amount,username,password))
                mydb.commit()
                print("Rs.",withdrawn_amount,"has been successfully withdrawn.")
                print("Your current balance is:",amount)
                customer[6]= amount
                
            existingAccountOperations(customer,username, password)

        case 5:
            print("You have been successfully logged out!\n")
            print("\t\t******************************************\n\n\n")
            main()
        case _:
            print("Invalid Input!!")
            existingCustomer()
    
def existingCustomer():
    username = str(input("Enter your username:"))
    password = str(input("Enter your password:"))
    mycursor.execute("select * from customer where Username=%s and Password=%s",(username, password))
    customer = mycursor.fetchall()
    customerDetails=list(customer[0])
    print("Welcome back! ",customerDetails[2],customerDetails[1],"\n")
    existingAccountOperations(customerDetails,username,password)
    
def newCustomer():
    print("Thank you for choosing KV Bank.\n Please enter your details for new account creation\n")
    FirstName = str(input("Enter your first name:"))
    LastName = str(input("Enter your last name:"))
    Mobile_Number = str(input("Enter your mobile number:"))
    if(len(Mobile_Number)!=10):
        print("Invalid mobile number! Please enter correct details.\n")
        customer()
    print("NOTE: You need to have minimum balance Rs. 500 in the bank account. Are you ready to submit Rs. 500? (Y/N) \n")
    isValid= checkIfAmountSubmitted(str(input("")))
    if(isValid==False):
        print("Please submit Rs. 500 as minimum balance. Account cannot be created. Please try again.\n")
        customer()
    else:
        print("Thank you for submitting Rs.500  Your account creation is in progress\n")
    Username = str(input("Choose your username:"))
    Password = str(input("Choose your password:"))
    Account_Num= getAccountNumber()
    print("Congratulations!! You new account has been created.\n You account number is:",Account_Num)
    print("Kindly save it for future reference\n")
   
    insert_stmt= ("INSERT INTO customer(Account_Num, LastName, FirstName, Username, Password, Mobile_Number) VALUES (%s,%s,%s,%s,%s,%s)")
    data= (Account_Num, LastName, FirstName, Username, Password, Mobile_Number)
    mycursor.execute(insert_stmt, data);
    mydb.commit()
    print("Kindly login to perform transaction.\n")
    customer()
    
def getAccountNumber():
    return randint(10000, 99999)
def getAccountNumber():
    return randint(10000, 99999)
def checkIfAmountSubmitted(ans):
    if(ans.lower()=='y'):
        return True
    else:
        return False


def main():
    choice= menu()
    if(choice==1):
        admin()
    elif(choice==2):
        customer()
    else:
      print("Invalid Choice\: Please enter valid choice\n\n")
      main()

main()



#Add exit accordingly
#Add spaces & beautify wherever required
#Add admin functionality



