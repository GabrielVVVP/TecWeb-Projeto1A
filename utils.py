from database import Database
from database import Note

def extract_route(request): 
    inicio = request.find("/")+1
    mid = request[inicio:]
    end_to = mid.find(" ")
    res = mid[:end_to]
    
    return res

def read_file(Path):
    res = str(Path)
    appendix = [".txt",".html",".css"]
    if res.endswith(appendix[0]) or res.endswith(appendix[1]) or res.endswith(appendix[2]):
        file_r = open(Path,"rb")
    else:  
        file_r = open(Path,"rb")
    
    return file_r.read()
    
def load_template(template):
    temp = open("templates/"+template,'r+',encoding='utf8').read()
    return temp

def all_data(database_db):
    db = Database(database_db)
    notes = db.get_all()
    return notes

def add_Entry(params, database_db):
    db = Database(database_db)
    val_list = list(params.values())
    db.add(Note(title=val_list[0], content=val_list[1]))  
    
def delete_Entry(id_entry, database_db):
    db = Database(database_db)
    db.delete(id_entry)    

def update_Entry(params, database_db):
    db = Database(database_db)
    val_list = list(params.values())
    db.update(Note(title=val_list[0], content=val_list[1],id=val_list[2]))             

def build_response(body='', code=200, reason='OK', headers=''):
    
    if body=='' and code==200 and reason=='OK' and headers=='':
        return bytes('HTTP/1.1 {} {}\n\n'.format(code,reason), encoding='utf8')
    
    elif body!= '' and code==200 and reason=="OK" and headers=="":
        return bytes('HTTP/1.1 200 OK\n\n{}'.format(body), encoding='utf8')
    
    elif reason!='OK' and code!=200 and headers!='':
        return bytes('HTTP/1.1 {} {}\n{}\n\n'.format(code,reason,headers), encoding='utf8')
    
    if reason!='OK' and code!=200 and headers=='':
        return bytes('HTTP/1.1 {} {}\n\n'.format(code,reason), encoding='utf8')
      