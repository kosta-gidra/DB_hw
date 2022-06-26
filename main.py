import psycopg2

#Вспомогательная функция
def read_password():
    with open('pass.txt', 'r') as file:
        password = file.readlines()
        return password

def create_table():
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            create table if not exists client (
                id serial primary key,
                name VARCHAR(20) not null,
                surname VARCHAR(20) not null,
                email VARCHAR(50) not null
            );
            ''')
            cur.execute('''
            create table if not exists phone (
                id serial primary key,
                phone bigint not null,
                client_id integer references client(id)
            );
            ''')
            conn.commit()
            return

def client_add(name,surname,email):
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
            insert into client(name,surname,email)
            values('{name}','{surname}','{email}')
            RETURNING id, name, surname, email;
            ''')
            return cur.fetchone()

def phone_add(phone,client_id):
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
            insert into phone(phone,client_id)
            values({phone},{client_id})
            RETURNING id, phone, client_id;
            ''')
            return cur.fetchone()

def client_phone_add(name,surname,email,phone):
    id=client_add(name,surname,email)
    phone_add(phone,id[0])
    return

def client_changes(client_id,name=None,surname=None,email=None):
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            if name!=None:
                cur.execute(f'''
                UPDATE client
                SET name = '{name}'
                WHERE id = {client_id};
                ''')
            if surname!=None:
                cur.execute(f'''
                UPDATE client
                SET surname = '{surname}'
                WHERE id = {client_id};
                ''')
            if email!=None:
                cur.execute(f'''
                UPDATE client
                SET email = '{email}'
                WHERE id = {client_id}
                RETURNING id, name, surname, email;
                ''')
            return cur.fetchone()

def phones_del(client_id):
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
            delete from phone
            where client_id = {client_id};
            ''')
            conn.commit()
            return

def phone_del(phone_id):
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
            delete from phone
            where id = {phone_id};
            ''')
            conn.commit()
            return

def client_del(client_id):
    phones_del(client_id)
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
            delete from client
            where id = {client_id};
            ''')
            conn.commit()
            return

#Вспомогательная функция
def client_find_helper(column, name_column):
    with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                select name,surname,email,id from client
                where {name_column} = '{column}';
                ''')
                result = cur.fetchone()
                if result == None:
                    print(f'\n{name_column} {column} does not exist')
                else:
                    print(f'Name: {result[0]}, Surname: {result[1]}, Email: {result[2]}')
                    cur.execute(f'''
                    select phone from phone
                    where client_id = {result[3]};
                    ''')
                    result = cur.fetchall()
                    print(f'\nPhone(s): {result[0]}')
                    return

def client_find(name=None,surname=None,email=None,phone=None):
    if phone != None:
        with psycopg2.connect(database='client_base_hw', user='postgres', password=read_password()[0].strip()) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''
                select id, phone, client_id from phone
                where phone = {phone};
                ''')
                result = cur.fetchone()
                if result == None:
                    print('\nPhone number does not exist')
                else:
                    print(f'Phone: {result[1]}')
                    cur.execute(f'''
                    select name,surname,email from client
                    where id = {result[2]};
                    ''')
                    result = cur.fetchone()
                    print(f'\nName: {result[0]}, Surname: {result[1]}, Email: {result[2]}')
                    return
    if email != None:
        namecolumn = 'email'
        client_find_helper(email, namecolumn)
        return
    if surname != None:
        namecolumn = 'surname'
        client_find_helper(surname, namecolumn)
        return
    if name != None:
        namecolumn = 'name'
        client_find_helper(name, namecolumn)
        return
    else:
        print('\nrequest is empty!')
        return

def interface():
    print('Создайте БД и внесите пароль в файл pass.txt')
    input_ = True
    while input_:
        print('\nСписок доступных операций с БД:\n'
          '1 - создать структуру БД\n'
          '2 - добавить нового клиента\n'
          '3 - добавить телефон для существующего клиента\n'
          '4 - добавить нового клиента и телефон\n'
          '5 - изменить данные о клиенте (имя, фамилия, почта)\n'
          '6 - удалить конкретный телефон для существующего клиента\n'
          '7 - удалить все телефоны для существующего клиента\n'
          '8 - удалить существующего клиента\n'
          '9 - найти клиента по имени, фамилии, телефону или email-у\n'
          '0 - выход')
        input_ = int(input('Введите номер операции: '))
        if input_ == 1:
            create_table()
        elif input_ == 2:
            name = input('Введите имя :')
            surname = input('Введите фамилию :')
            email = input('Введите почту :')
            client_add(name, surname, email)
        elif input_ == 3:
            phone = input('Введите телефон :')
            client_id = input('Введите id клиента :')
            phone_add(phone, client_id)
        elif input_ == 4:
            name = input('Введите имя :')
            surname = input('Введите фамилию :')
            email = input('Введите почту :')
            phone = input('Введите телефон :')
            client_phone_add(name, surname, email, phone)
        elif input_ == 5:
            client_id = input('Введите id клиента :')
            name = input('Введите имя (или нажмите Enter):')
            if name == '':
                name = None
            surname = input('Введите фамилию (или нажмите Enter):')
            if surname == '':
                surname = None
            email = input('Введите почту (или нажмите Enter):')
            if phone == '':
                phone = None
            client_changes(client_id, name, surname, email)
        elif input_ == 6:
            phone_id = input('Введите id телефона :')
            phone_del(phone_id)
        elif input_ == 7:
            client_id = input('Введите id клиента :')
            phones_del(client_id)
        elif input_ == 8:
            client_id = input('Введите id клиента :')
            client_del(client_id)
        elif input_ == 9:
            name = input('Введите имя (или нажмите Enter):')
            if name == '':
                name = None
            surname = input('Введите фамилию (или нажмите Enter):')
            if surname == '':
                surname = None
            email = input('Введите почту (или нажмите Enter):')
            if email == '':
                email = None
            phone = input('Введите телефон (или нажмите Enter):')
            if phone == '':
                phone = None
            client_find(name,surname,email,phone)
        elif input_ == 0:
            break

interface()
