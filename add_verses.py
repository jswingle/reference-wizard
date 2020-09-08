import psycopg2
import sys
import boto3

def add_verses(verse_set,translation):
    """ create tables in the PostgreSQL database"""
    table_create_command = (
        '''
        CREATE TABLE IF NOT EXISTS {} (
        Book varchar (20),
        Chapter integer,
        Verse integer,
        Translation varchar(10),
        Text varchar,
        Time float(2),
        CONSTRAINT {} PRIMARY KEY (Book,Chapter,Verse)
        )
        '''
        )

    row_create_command = "INSERT INTO {} (Book,Chapter,Verse,Translation,Text) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (Book,Chapter,Verse) DO UPDATE SET Text=Excluded.Text;"

    unique_id = translation + '1'
    table_create_command = table_create_command.format(translation,unique_id)

    ENDPOINT="bible.cvabaappcl34.us-west-2.rds.amazonaws.com"
    PORT="5432"
    USR="postgres"
    DBNAME="bible"
    with open('pw.txt',mode='r') as pw:
        PASSWORD=pw.read()

    try:
        conn =  psycopg2.connect(host=ENDPOINT, user=USR, password=PASSWORD, port=PORT, database=DBNAME)
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        cur.execute(table_create_command)
        for verse in verse_set:
            command = row_create_command.format(translation)
            cur.execute(command,(verse.book,verse.chapter,verse.verse,verse.translation,verse.text))
        conn.commit()
        conn.close()
        cur.close()
    except Exception as e:
        print("Database connection failed due to {}".format(e))          

if __name__ == '__main__':
    add_verses()