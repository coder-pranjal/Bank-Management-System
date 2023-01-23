import mysql.connector as sql
import sys
from random import randint
mydb=sql.connect (host="localhost",user="root", passwd="12345")
mycursor=mydb.cursor()
mycursor.execute('create database if not exists kv_bank')
mycursor.execute('use kv_bank')

if mydb.is_connected():
    print("Succesfully connected to KV Bank Database\n\n")


mycursor.execute("create table if not exists customer(Account_Num int NOT NULL, LastName varchar(255),FirstName varchar(255),Username varchar(255),Password varchar(15),Mobile_Number varchar(10),Balance int(11))")
mydb.commit()

print("\t\t**** WELCOME TO KV BANK ****\n\n")


def menu():
    print("You are identified as:")
    print("1. Admin")
    print("2. Customer")
    print("3. Exit")
    
    return  int(input(""))

def admin():
    password = str(input("Enter password:"))
    adminpass='KVadmin'
    if password==adminpass:
        print("## You are now in admin mode ## \n\n")
        print("---> Detail of ALL ACCOUNTS:\n")
        mycursor.execute("select*From customer")
        result=mycursor.fetchall()
        print('Account no.\t LastName\t      FirstName\t    \t\tUsername\t    Password\t  \t  Mobile no.\t   \t Balance')
        for i in result:
            print()
            customize=list(i)
            
            for j in customize:
                print(j,'\t\t',end='')
        print('\n\n')
        main()
    else:
        print('Invalid credentials!!')
        print('\n\n')
        main()


def adminOperations():
     print("1. Display all accounts")
    

def customer():
    print("\n## Welcome to KV Bank ## \n\n")
    print("1. Existing Customer")
    print("2. New Customer")
    print("3. Exit")
    ch=int(input(""))
    if(ch==1):
        existingCustomer()
    elif(ch==2):
        newCustomer()
    elif(ch==3):
        quit()
    else:
       print("Invalid Choice\: Please enter valid choice\n\n")
       main()
 
    
def existingAccountOperations(customer,username, password):
    print("1.View Account Details")
    print("2.View current Balance")
    print("3.Deposit amount")
    print("4.Withdraw amount")
    print("5. Logout")
    ch=int(input("\nEnter your choice:"))
    if ch==1:
        print("\nAccount no.:",customer[0])
        print("Customer username:",customer[3])
        print("Customer Name:",customer[2],customer[1])
        print("Customer Mobile no.(10-digit):",customer[5])
        print("Current Balance:",customer[6],'\n')
        existingAccountOperations(customer,username, password)
    elif ch==2:
        print("Your current balance is:",customer[6],"\n")
        existingAccountOperations(customer,username, password)
    elif ch==3:
        amount = int(input("Enter amount to be deposited:"))
        deposited_amount= amount
        amount+=customer[6]
        mycursor.execute("update customer set Balance=%s where Username=%s and Password=%s",(amount,username,password))
        customer[6]= amount
        mydb.commit()
        print("\nRs.",deposited_amount,"has been successfully deposited.")
        print("Your current balance is:",amount,'\n')

        existingAccountOperations(customer,username, password)

    elif ch==4:
        amount = int(input("Enter amount to withdraw:"))
        withdrawn_amount= amount
        if(customer[6]==500):
            print("Your current balance is the minimum balance. Invalid operation!!\n")
        elif(amount>customer[6]):
            print("Your entered amount is greater than the current balance. Invalid operation!!\n")
        elif(customer[6]-amount<500):
            print("Your cannot withdraw Rs.",amount, "Minimum balance of Rs.500 is required. Invalid operation!!\n")
        else:
            amount= customer[6]-amount
            mycursor.execute("update customer set Balance=%s where Username=%s and Password=%s",(amount,username,password))
            mydb.commit()
            print("Rs.",withdrawn_amount,"has been successfully withdrawn.")
            print("Your current balance is:",amount)
            customer[6]= amount
                
        existingAccountOperations(customer,username, password)

    elif ch==5:
        print("You have been successfully logged out!\n")
        print("\t\t******************************************\n\n\n")
        main()
    else:
        print("Invalid Input!!")
        existingCustomer()


    
def existingCustomer():
    username = str(input("Enter your username:"))
    password = str(input("Enter your password:"))
    mycursor.execute("select * from customer where Username=%s and Password=%s",(username, password))
    existing_customer= mycursor.fetchall()
    if(len(existing_customer)==0):
        print("Invalid Username/Password!\n")
        customer()
    else:
        customerDetails=list( existing_customer[0])
        print("\nWelcome back! ",customerDetails[2],customerDetails[1],"\n")
        existingAccountOperations(customerDetails,username,password)


    
def newCustomer():
    print("Thank you for choosing KV Bank.\n Please enter your details for new account creation\n")
    FirstName = str(input("Enter your first name:"))
    LastName = str(input("Enter your last name:"))
    Mobile_Number = str(input("Enter your 10-digit mobile number:"))
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
    print("Congratulations!! You new account has been created.\nYour account number is:",Account_Num)
    print("Kindly save it for future reference\n")
   
    insert_stmt= ("INSERT INTO customer(Account_Num, LastName, FirstName, Username, Password, Mobile_Number,Balance) VALUES (%s,%s,%s,%s,%s,%s,%s)")
    data= (Account_Num, LastName, FirstName, Username, Password, Mobile_Number,500)
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
    elif(choice==3):
        quit()
    else:
      print("Invalid Choice\: Please enter valid choice\n\n")
      main()

main()


