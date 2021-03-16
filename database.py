import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''   

class Database(object):
    
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco+".db")
        self.connection = self.conn.cursor()
        self.connection.execute("CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL)")
    
    def add(self, note):
        resp = "INSERT INTO note(title,content) VALUES ('{}','{}')".format(note.title,note.content)
        self.connection.execute(resp)
        self.conn.commit()
        
    def get_all(self):
        
        cursor = self.connection.execute("SELECT id, title, content FROM note")
        lista = []
        for linha in cursor:
            identificador = linha[0]
            title = linha[1]
            content = linha[2]
            lista.append(Note(linha[0],linha[1],linha[2]))
        return lista
            
    def update(self, entry):
        self.connection.execute("UPDATE note SET title = '{}' WHERE id = '{}'".format(entry.title,entry.id))
        self.connection.execute("UPDATE note SET content = '{}' WHERE id = '{}'".format(entry.content,entry.id))
        self.conn.commit()
        
    def delete(self, note_id):
        self.connection.execute("DELETE FROM note WHERE id = '{}'".format(note_id))
        self.conn.commit()    
