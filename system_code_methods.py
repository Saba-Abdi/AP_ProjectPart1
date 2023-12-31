import random
from base_objects import *

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

        #situation = input('How can I help you? For sign-up enter 1 and for sign-in enter 2: ')
        #return enter(int(situation))
    
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
                    #if user_position == 'patient':
                        #action = input('What do you wish to do? Current appointment, appointments history, or new appointment? ')
            
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
            
            else:
                print('Invalid option for sign-in method.')
        
        else:
            print('Invalid username or password!')
    
    else:
        print("Invalid option. Please enter 1 for sign-up or 2 for sign-in.")
        #return enter(int(input("How can I help you? For sign-up enter 1 and for sign-in enter 2: ")))
