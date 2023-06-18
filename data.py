import sqlite3

db_path = "ess.db"

def connect_to_db(path):
    conn = sqlite3.connect(path)
    conn.execute("create table if not exists user(pid integer primary key,name text,address text,contact integer,mail text)")
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

def read_stories_by_story_type(story_type):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM stories WHERE story_kind = ?'
    value = story_type
    results = cur.execute(query,(value,)).fetchall()
    conn.close()
    return results

def read_story_by_story_number(story_number):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM stories WHERE number = ?'
    value = story_number
    result = cur.execute(query,(value,)).fetchone()
    conn.close()
    return result

def insert_story(story_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO stories (story_kind, title, genre, status, description, url) VALUES (?,?,?,?,?,?)'
    values = (story_data['story_type'], story_data['title'],
              story_data['genre'], story_data['status'],
              story_data['description'], story_data['url'])
    cur.execute(query,values)
    conn.commit()
    conn.close()

def delete_story(story_number):
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM stories WHERE number = ?"
    values = (story_number,)
    cur.execute(query, values)
    conn.commit()
    conn.close()

def update_story(story_data):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE stories SET story_kind=?, title=?, genre=?, status=?, description=?, url=? WHERE number=?"
    values = (story_data['story_type'], story_data['title'],
              story_data['genre'], story_data['status'],
              story_data['description'], story_data['url'],
              story_data['story_number'])
    cur.execute(query, values)
    conn.commit()
    conn.close()