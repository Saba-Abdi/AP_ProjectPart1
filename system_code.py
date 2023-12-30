from base_objects import *
import random


print('Welcome to doctor online!')

username = input('Please enter your username: ')
user_position = input('Please enter your position: ')
user = User.sign_in(username=username, user_position=user_position)

if user is not None:
    user_password, user_email = user[4], user[3]
else:
    raise Exception('User not found')

sign_in_method = input('How do you want to sign in? password or opt? ')


# password
if sign_in_method == 'password':
    password = input('Please enter your password: ')
    if password != user_password:
        raise Exception('incorrect password!')
    else:
        print('Welcome to your account.')
        if user_position == 'patient':
            action = input('What do you wish to do? current appointment or appointments history or new appointment? ')


# opt
else:
    email = input('Please enter your email:')
    if email != user_email:
        raise Exception('Email does not match.')
    else:
        opt = random.randint(100000, 999999)
        print(f'Here is your password: {opt}')
        opt_password = input('Please enter your opt password: ')


