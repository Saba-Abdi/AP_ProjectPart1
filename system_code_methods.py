import random
from base_objects import *
from new_appoitment import *
from Secretary import manoeuvre
from previous_current_appointments import previous_appointments, current_appointment


def enter(situation):
    if situation == 1:
        print("Let's create an account!")
        position = input("Please enter your position: ")
        username = input('Please enter a username: ')
        user = User.sign_in(username=username, user_position=position)
        if user is None:
            name = input("Please enter a name: ")
            password = input("Please enter a password: ")
            email = input("Please enter an email: ")
            User.sign_up(name=name, username=username, email=email, password=password, user_position=position)
            print("Account successfully created!")
        else:
            print('User already exists!')
    
    elif situation == 2:
        user_position = input('Please enter your position: ')
        username = input('Please enter your username: ')
        
        user = User.sign_in(username=username, user_position=user_position)
        if user is not None:
            
            user_password, user_email = user[4], user[3]

            sign_in_method = input('How do you want to sign in password or opt?')

            # Password
            if sign_in_method.lower() == 'password':
                password = input('Please enter your password: ')
                while password != user_password:
                    print('Incorrect password!')
                    password = input('Please enter your password again:')
                
                print('Welcome to your account.')
                if user_position == "patient":
                    action2 = input(
                        "What do wish to do? 1.Your current appointment  2. Your previous appoitments  3.Reserve a new appoitment ")
                    if action2 == '3':
                        return choose_service(user_position, username)
                    elif action2 == '2':
                        return previous_appointments(user[0])
                    elif action2 == '1':
                        return current_appointment(user[0])
                elif user_position == 'secretary':
                    request = int(input('How may I assist you today? Please enter: 1 to see current appiontments, 2 to cancel an appointment or 3 to increase the number of availabe beds of a clinic'))
                    return manoeuvre(request)
            # Opt
            elif sign_in_method.lower() == 'opt':
                email = input('Please enter your email:')
                while email != user_email:
                    print('Email does not match.')
                    email = input('Please enter your email again:')
                
                opt = random.randint(100000, 999999)
                print(f'Here is your password: {opt}')
                opt_password = input('Please enter your opt password: ')
                print("Login successful!")
                if user_position == "patient":
                    action2 = input(
                        "What do wish to do? 1.Your current appointment  2. Your previous appoitments  3.Reserve a new appoitment ")
                    if action2 == '3':
                        return choose_service(user_position, username)
                    elif action2 == '2':
                        return previous_appointments(user[0])
                    elif action2 == '1':
                        return current_appointment(user[0])
                elif user_position == 'secretary':
                    request = int(input('How may I assist you today? Please enter: 1 to see current appiontments, 2 to cancel an appointment or 3 to increase the number of availabe beds of a clinic'))
                    return manoeuvre(request)
            
            else:
                print('Invalid option for sign-in method.')
        
        else:
            print('Invalid username or password!')
    
    else:
        print("Invalid option. Please enter 1 for sign-up or 2 for sign-in.")

