from base_objects import *
from new_appoitment import getting_clinic_availability

clinic1 = Clinic.add_clinic("The Healing Place", "123 Main St", "123-456-7890",
                            0, True, False, True, False, 50, 0, 30, 0)
clinic2 = Clinic.add_clinic("YouthEncore", "456 Oak St", "987-654-3210", 0,
                            False, True, False, True, 0, 60, 0, 40)
clinic3 = Clinic.add_clinic("Health Center", "789 Elm St", "555-123-4567", 0,
                            True, True, True, True, 45, 55, 25, 35)
clinic4 = Clinic.add_clinic("Dental Clinic", "321 Pine St", "333-999-8888", 0,
                            False, False, True, False, 0, 0, 40, 0)
clinic5 = Clinic.add_clinic("WellSpring", "225 Main St", "231-824-9999", 0,
                            True, False, True, False, 50, 0, 35, 0)
clinic6 = Clinic.add_clinic("HealthFirst", "128 Main St", "321-784-2316", 0,
                            False, False, True, False, 0, 0, 95, 0)
clinic7 = Clinic.add_clinic("Gateway Clinic", "433 Main St", "222-979-7890", 0,
                            True, True, True, True, 50, 65, 30, 32)
getting_clinic_availability()

i1 = Insurance.add_insurance('Health Choice Insurance', '564-247-1111', 20)
i2 = Insurance.add_insurance('Liability Herd Gambler', '787-2233-4400', 35)
i3 = Insurance.add_insurance('Our Word Insurance Herb Liability',
                             '201-482-9999', 41)
i4 = Insurance.add_insurance('Liability Rhapsody', '989-428-9449', 25)
i5 = Insurance.add_insurance('Risk Reduction Alliance', '102-688-3636', 20)

doctor1 = User.sign_up('John Doe', 'JohnDoe123', 'JohnDoe123@gmail.com',
                       'a1b2c3d4e5', 'doctor')
doctor2 = User.sign_up('Mark Black', 'mark15', 'm.black@gmail.com',
                       'f6g7h8i9j0', 'doctor')
doctor3 = User.sign_up('Gina Watson', 'gina79', 'ginawatson@gmail.com',
                       'k1l2m3n4o5',
                       'doctor')
doctor4 = User.sign_up('Emma Chamber', 'emma48', 'emma1948@gmail.com',
                       'p6q7r8s9t0',
                       'doctor')
doctor5 = User.sign_up('Marin White', 'martin99', 'martin.w@gmail.com',
                       'u1v2w3x4y5',
                       'doctor')
doctor6 = User.sign_up('Edward Brown', 'edward65', 'edi_brown@gmail.com',
                       'z6a7b8c9d0',
                       'doctor')
doctor7 = User.sign_up('Samantha Stark', 'saman45', 's_stark_5.evans@gmail.com',
                       'e1f2g3h4i5', 'doctor')
doctor8 = User.sign_up('Minerva Gomez', 'minerva45', 'minervagomez@gmail.com',
                       'j6k7l8m9n0',
                       'doctor')
doctor9 = User.sign_up('Rosa Diaz', 'rosa54', 'rosadiaz.lapd@gmail.com',
                       'o1p2q3r4s5',
                       'doctor')
doctor10 = User.sign_up('Nacho Vargas', 'nacho45', 'ignasio.v@gmail.com',
                        't6u7v8w9x0',
                        'doctor')
doctor11 = User.sign_up('Amanda West', 'amanda12', 'amwe789@gmail.com',
                        'y1z2a3b4c5',
                        'doctor')
doctor12 = User.sign_up('Walter White', 'walter56', 'wwh9119@gmail.com',
                        'd6e7f8g9h0',
                        'doctor')
doctor13 = User.sign_up('Hailey helder', 'hailey45', 'h.h.b78@gmail.com',
                        'i1j2k3l4m5',
                        'doctor')

patient1 = User.sign_up('Liam Harrison', 'liam54', 'liamharrison@gamil.com',
                        'n6o7p8q9r0',
                        'patient')
patient2 = User.sign_up('Liam Ford', 'liam89', 'liamford@gamil.com',
                        's1t2u3v4w5',
                        'patient')
patient3 = User.sign_up('Ava Baker', 'ava35', 'ava_becker@gamil.com',
                        'x6y7z8a9b0',
                        'patient')
patient4 = User.sign_up('Noah Garcia', 'noah58', 'noah5445@gamil.com',
                        'c1d2e3f4g5',
                        'patient')
patient5 = User.sign_up('Emma Wright', 'emma47', 'e.wright@gamil.com',
                        'h6i7j8k9l0',
                        'patient')
patient6 = User.sign_up('Oliver Perez', 'oliver12', 'oliv_perez@gamil.com',
                        'm1n2o3p4q5',
                        'patient')
patient7 = User.sign_up('Sophia Carter', 'sophia34',
                        'sophia.l.carter@gamil.com', 'r6s7t8u9v0',
                        'patient')
patient8 = User.sign_up('Ethan Mitchell', 'ethan89', 'iamethan@gamil.com',
                        'w1x2y3z4a5',
                        'patient')
patient9 = User.sign_up('Isabella Turner', 'isa45', 'isaturn@gamil.com',
                        'b6c7d8e9f0',
                        'patient')
patient10 = User.sign_up('Lucas Phillips', 'lucas78', 'luke_philip@gamil.com',
                         'g1h2i3j4k5',
                         'patient')

secretary1 = User.sign_up('Maddox Gibson', 'maddox66', 'maddiegibson@gmail.com',
                          'l6m7n8o9p0',
                          'secretary')
secretary2 = User.sign_up('Aria Henderson', 'aria85', 'aria_hende@gmail.com',
                          'v6w7x8y9z0',
                          'secretary')
secretary3 = User.sign_up('Lila Barnes', 'lila47', 'lila.barnes@gmail.com',
                          'a1b2c3d4e5',
                          'secretary')
secretary4 = User.sign_up('Sarai Huffman', 'sarai13', 'msaraihuf@gmail.com',
                          'p6q7r8s9t0', 'secretary')
secretary5 = User.sign_up('Kasey Duran', 'kasey31', 'imkaseyduran@gmail.com',
                          'k1l2m3n4o5', 'secretary')
