import random
import sqlite3


class BankAccount:
    account_numbers = []

#  creates BankAccount object which creates an accurate credit card number
#  according to the industry specifications, and passage of the luhn algorithm.
#  a unique pin is also assigned.
    def __init__(self):

        random.seed()
        random_credit_number = "400000"

        self.balance = 0

        for i in range(9):
            random_credit_number = random_credit_number + str(random.randint(0, 9))

        odd_digit = True
        luhn_number = ""
        for i in range(15):
            if odd_digit:
                luhn_digit = int(random_credit_number[i]) * 2

                if luhn_digit > 9:
                    luhn_digit = luhn_digit - 9

                luhn_number = luhn_number + str(luhn_digit)

            else:
                luhn_number = luhn_number + str(int(random_credit_number[i]))

            odd_digit = not odd_digit

        card_numbers_sum = 0

        for i in range(15):
            card_numbers_sum = card_numbers_sum + int(luhn_number[i])

        if card_numbers_sum % 10 == 0:
            num_add_to_end = 0
        else:
            num_add_to_end = str(10 - (card_numbers_sum % 10))

        self.credit_card_number = random_credit_number + num_add_to_end

        self.pin = ""

        for i in range(4):
            self.pin = self.pin + str(random.randint(0, 9))

        BankAccount.account_numbers.append(self)


# creates a sqlLite data base to store card numbers and pins for future access.
conn = sqlite3.connect("cards.sqlite")
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, '
            'number TEXT,'
            'pin TEXT,'
            'balance INTEGER DEFAULT 0);')

conn.commit()

menu_selection = None

while menu_selection != 0:

    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    menu_selection = int(input())

    if menu_selection == 1:

        new_account = BankAccount()

        print("Your card has been created")
        print("Your card number:")
        print(new_account.credit_card_number)
        print("Your card PIN:")
        print(new_account.pin)

        cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);",
                    (new_account.credit_card_number, new_account.pin, new_account.balance))

        conn.commit()
        cur.execute("SELECT number FROM card;")
        print(cur.fetchone())
        print("Confirm this is the correct card number")

    elif menu_selection == 2:

        print("Enter your card number:")
        account_number = input()

        successful_login = False
        loggedin_account = None

        cur.execute("SELECT number, pin, balance FROM card WHERE number = ?;", (account_number,))

        sql_account = cur.fetchone()
        conn.commit()

        if sql_account is not None:
            print("Enter your PIN:")
            pin_number = input()

            if pin_number == sql_account[1]:
                print("You have successfully logged in!")
                successful_login = True

        if not successful_login:
            print("Wrong card number or PIN!")

        else:
            loggedin = True

            while loggedin:
                print("1. Check Balance")
                print("2. Log out")
                print("3. Update Balance")
                print("0. Exit")     

                account_login_selection = int(input())

                if account_login_selection == 1:
                    print("Your balance is:")
                    print(sql_account[2])

                elif account_login_selection == 2:
                    print("You have successfully logged out!")
                    loggedin_account = None
                    loggedin = False

                elif account_login_selection == 3:
                    print("Enter new account balance: ")
                    account_balance = int(input())

                    cur.execute("UPDATE card SET balance = ? WHERE number = ?;", (account_balance, sql_account[0]))
                    cur.execute("SELECT number, pin, balance FROM card WHERE number = ?;", (account_number,))
                    sql_account = cur.fetchone()
                    conn.commit()

                elif account_login_selection == 0:
                    menu_selection = 0
                    loggedin = False

print("Bye!")
