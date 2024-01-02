from base_objects import *

clinic1 = Clinic.add_clinic("Clinic A", "123 Main St", "123-456-7890", 0, True, False, True, False, 50, 0, 30, 0)
clinic2 = Clinic.add_clinic("Clinic B", "456 Oak St", "987-654-3210", 0, False, True, False, True, 0, 60, 0, 40)
clinic3 = Clinic.add_clinic("Health Center", "789 Elm St", "555-123-4567", 0, True, True, True, True, 45, 55, 25, 35)
clinic4 = Clinic.add_clinic("Dental Clinic", "321 Pine St", "333-999-8888", 0, False, False, True, False, 0, 0, 40, 0)
clinic5 = Clinic.add_clinic("Clinic C", "225 Main St", "231-824-9999", 0, True, False, True, False, 50, 0, 35, 0)
clinic6 = Clinic.add_clinic("Clinic D", "128 Main St", "321-784-2316", 0, False, False, True, False, 0, 0, 95, 0)
clinic7 = Clinic.add_clinic("Clinic E", "433 Main St", "222-979-7890", 0, True, True, True, True, 50, 65, 30, 32)
clinic1.getting_clinic_availability()
clinic2.getting_clinic_availability()
clinic3.getting_clinic_availability()
clinic4.getting_clinic_availability()
clinic5.getting_clinic_availability()
clinic6.getting_clinic_availability()
clinic7.getting_clinic_availability()


p1 = Payment.add_payment(1, 6037, 9, 605, 4545)
i1 = Insurance.add_insurance('hel', '0930', 20)

doctor1 = User.sign_up('Luke Evans', 'luke58', 'l.evans@gmail.com', '58911958', 'doctor')
doctor2 = User.sign_up('Mark Black', 'mark15', 'm.black@gmail.com', '1578578', 'doctor')
doctor3 = User.sign_up('Gina Watson', 'gina79', 'ginawatson@gmail.com', '79844567',
                       'doctor')
doctor4 = User.sign_up('Emma Chamber', 'emma48', 'emma1948@gmail.com', '48484848',
                       'doctor')
doctor5 = User.sign_up('Marin White', 'martin99', 'martin.w@gmail.com', '99889988',
                       'doctor')
doctor6 = User.sign_up('Edward Brown', 'edward65', 'edi_brown@gmail.com', '659659',
                       'doctor')
doctor7 = User.sign_up('Samantha Stark', 'saman45', 's_stark_5.evans@gmail.com',
                       'SS4554SS', 'doctor')
doctor8 = User.sign_up('Minerva Gomez',  'minerva45', 'minervagomez@gmail.com', '45123669',
                       'doctor')
doctor9 = User.sign_up('Rosa Diaz', 'rosa54', 'rosadiaz.lapd@gmail.com', 'r.z.la54',
                       'doctor')
doctor10 = User.sign_up('Nacho Vargas', 'nacho45', 'ignasio.v@gmail.com', 'verne452',
                        'doctor')
doctor11 = User.sign_up('Amanda West', 'amanda12', 'amwe789@gmail.com', '12west21',
                        'doctor')
doctor12 = User.sign_up('Walter White', 'walter56', 'wwh9119@gmail.com', '56988887',
                        'doctor')
doctor13 = User.sign_up('Hailey helder', 'hailey45', 'h.h.b78@gmail.com', 'hail4545',
                        'doctor')


patient1 = User.sign_up('Liam Harrison', 'liam54', 'liamharrison@gamil.com', 'li5445li',
                        'patient')
patient2 = User.sign_up('Liam Ford', 'liam89', 'liamford@gamil.com', '54899286',
                        'patient')
patient3 = User.sign_up('Ava Baker', 'ava35', 'ava_becker@gamil.com', '12354896',
                        'patient')
patient4 = User.sign_up('Noah Garcia',  'noah58','noah5445@gamil.com', '58846932',
                        'patient')
patient5 = User.sign_up('Emma Wright', 'emma47', 'e.wright@gamil.com', '47756556',
                        'patient')
patient6 = User.sign_up('Oliver Perez', 'oliver12', 'oliv_perez@gamil.com', '12211221',
                        'patient')
patient7 = User.sign_up('Sophia Carter', 'sophia34', 'sophia.l.carter@gamil.com', '123456',
                        'patient')
patient8 = User.sign_up('Ethan Mitchell', 'ethan89', 'iamethan@gamil.com', '123489',
                        'patient')
patient9 = User.sign_up('Isabella Turner', 'isa45', 'isaturn@gamil.com', 'Isa45544',
                        'patient')
patient10 = User.sign_up('Lucas Phillips', 'lucas78', 'luke_philip@gamil.com', 'luke7887',
                         'patient')


secretary1 = User.sign_up('Maddox Gibson', 'maddox66', 'maddiegibson@gmail.com', '456654',
                          'secretary')
secretary2 = User.sign_up('Aria Henderson', 'aria85', 'aria_hende@gmail.com', '854625',
                          'secretary')
secretary3 = User.sign_up('Lila Barnes', 'lila47', 'lila.barnes@gmail.com', '476952',
                          'secretary')
secretary4 = User.sign_up('Sarai Huffman', 'sarai13', 'msaraihuf@gmail.com', '591367',
                          'secretary')
secretary5 = User.sign_up('Kasey Duran', 'kasey31', 'imkaseyduran@gmail.com', '316479',
                          'secretary')
