
import random
import database
import validation
from getpass import getpass


account_number_from_user = None


def init():
    print("Welcome to bankPHP")

    have_account = int(input("Do you have an account with us? 1 (Yes)  2 (No) \n"))

    if have_account == 1:
        login()

    elif have_account == 2:
        register()

    else:
        print("You have selected an invalid option")
        init()


def login():
    print("******** Login ********")

    global account_number_from_user
    account_number_from_user = input("What is your account number? \n")

    is_valid_account_number = validation.account_number_validation(account_number_from_user)

    if is_valid_account_number:

        password = getpass("What is your password \n")

        user = database.authenticated_user(account_number_from_user, password)

        if user:
            database.login_auth_session(account_number_from_user, user)
            bank_operation(user)

        login()
    else:
        print("Account number is invalid. Account numbers must contain 10 digits and can only be integers. \n")
        init()


def register():
    print("****** Register ******")

    email = input("What is your e-mail address? \n")
    first_name = input("What is your first name? \n")
    last_name = input("What is your last name? \n")
    password = getpass("Create a new password. \n")

    account_number = generate_account_number()

    is_user_created = database.create(account_number, first_name, last_name, email, password)

    if is_user_created:
        print("Your account has been created")
        print("== ==== ====== ===== ===")
        print("Your account number is: %d" % account_number)
        print("Make sure to keep it safe")
        print("== ==== ====== ===== ===")

        login()
    else:
        print("Please try again")
        register()


def bank_operation(user):
    print("Welcome %s %s " % (user[0], user[1]))
    selected_option = int(
        input("Please select an option. \n 1. Deposit \n 2. Withdrawal \n 3. Get Balance \n 4. Log Out \n 5. Exit \n"))

    if selected_option == 1:
        deposit_operation(user)

    elif selected_option == 2:
        withdrawal_operation(user)

    elif selected_option == 3:
        print_current_balance(user)

    elif selected_option == 4:
        logout()

    elif selected_option == 5:
        print("Goodbye")
        exit()

    else:
        print("Invalid option entered")
        bank_operation(user)


def deposit_operation(user):

    current_balance = int(get_current_balance(user))
    amount_to_deposit = int(input("How much would you like to deposit? \n"))
    current_balance += amount_to_deposit
    set_current_balance(user, str(current_balance))

    if database.update(account_number_from_user, user):
        print("Your new account balance is ${}".format(current_balance))
        bank_operation(user)

    else:
        print("Transaction was not successful")
        bank_operation(user)


def withdrawal_operation(user):
    current_balance = int(get_current_balance(user))
    amount_to_withdraw = int(input("How much would you like to withdraw? \n"))

    if amount_to_withdraw < current_balance:
        current_balance -= amount_to_withdraw
        set_current_balance(user, str(current_balance))
        if database.update(account_number_from_user, user):
            print("Your new account balance is ${}".format(current_balance))
            bank_operation(user)

        else:
            print("Transaction was not successful.")
            bank_operation(user)

    elif amount_to_withdraw <= 0:
        print("Invalid entry. Withdrawal amount must be greater than zero.")
        bank_operation(user)
    elif amount_to_withdraw > current_balance:
        print("Withdrawal amount must be less than current balance.")
        bank_operation(user)


def generate_account_number():
    return random.randrange(1111111111, 9999999999)


def set_current_balance(user_details, balance):
    user_details[4] = balance


def get_current_balance(user_details):
    return user_details[4]


def print_current_balance(user):
    current_balance = int(get_current_balance(user))
    print("Your account balance is ${}".format(current_balance))
    bank_operation(user)


def logout():
    database.logout_auth_session()
    login()


init()
