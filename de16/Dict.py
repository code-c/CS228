import pickle


database = pickle.load(open('userData/database.p', 'rb'))

userName = raw_input('Please enter your name: ')
if userName in database:
    print('Welcome back ' + userName + '.')
    database[userName]['logins'] += 1
else:
    database[userName] = {}
    database[userName].update({'logins' : 1})
    print('Welcome ' + userName + '.')
print(database)
pickle.dump(database, open('userData/database.p', 'wb'))
