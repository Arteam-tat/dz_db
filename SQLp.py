import psycopg2
import pprint

def create_db(conn):
        cur.execute("""
        DROP TABLE IF EXISTS Phone;
        DROP TABLE IF EXISTS Client;
        """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Client(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                surname VARCHAR(60) NOT NULL,
                e_mail VARCHAR(60) NOT NULL UNIQUE);
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Phone(
                number DECIMAL UNIQUE CHECK(number <= 99999999999),
                client_id INTEGER REFERENCES Client(client_id));
                """)
        conn.commit()


def add_client(conn, name, surname, e_mail, phones=None):
    cur.execute("""
            INSERT INTO Client(name, surname, e_mail)
            VALUES(%s, %s, %s)
            RETURNING client_id, name, surname, e_mail;
            """, (name, surname, e_mail))
    conn.commit()

def add_phone(conn, client_id, number):
        cur.execute("""
                INSERT INTO Phone(client_id, number)
                VALUES(client_id, number)
                RETURNING client_id, name, surname, e_mail
                """), (client_id, number)
        print(cur.fetchone())


def change_client(conn, client_id, name=None, surname=None, e_mail=None, number=None):
    conn.execute("""
        UPDATE Client
        SET name=%s, surname=%s, e_mail=%s
        WHERE client_id=%s
        RETURNING client_id, name, surname, e_mail;
        """, (name, surname, e_mail, client_id))

    conn.execute("""
        UPDATE Phone
        SET number=%s
        WHERE client_id=%s
        RETURNING client_id, number;
        """, (number, client_id))

def delete_phone(conn, client_id, number):

    cur.execute("""DELETE FROM Phone
            WHERE client_id=%s;
            """, (client_id,))
    print(cur.fetchall())

def delete_client(conn, client_id):
    cur.execute("""DELETE FROM Client
            WHERE client_id=%s;
            """, (client_id,))
    print(cur.fetchall())

def find_client(cur, name=None, surname=None, e_mail=None, number=None):
    if name is not None:
        cur.execute("""
                    SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone FROM clients AS c
                    LEFT JOIN phones AS p ON c.client_id = p.client_id
                    WHERE c.first_name LIKE %s""", (name,))
        pprint(cur.fetchall())






with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    if __name__ =="__main__":
        with conn.cursor() as cur:
            print(create_db(conn))
            print(add_client(conn, 'Murz', 'Bulkin', 'murz@mail.ru', '89999999999'))
            print(add_phone(conn, '1', '89999999997'))
            print(change_client(conn, '1', 'Kuzya', 'Murzikov', 'kuziaa@mail.ru', '89999999998'))
            print(delete_phone(conn, '1', '89999999998'))
            print(delete_client(conn, '1'))
            print(find_client(conn, 'Murz'))

        conn.close()
