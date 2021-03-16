from utils import load_template, build_response, add_Entry, all_data, delete_Entry, update_Entry
import urllib

def index(request):
    request = request.replace('\r', '')  # Remove caracteres indesejados
    # Cabeçalho e corpo estão sempre separados por duas quebras de linha
    partes = request.split('\n\n')
    try:
        corpo = partes[1]
        final = partes[-1]
        selecionar_str = final[-1]
    except:
        selecionar_str = "0"     
    if selecionar_str == "1":
        id_corpo = corpo.split("&")
        id_init = id_corpo[0].split("=")
        id_corpo_str = id_init[1]
        id_corpo_int = int(id_corpo_str)
        note_template = load_template('components/update_note.html')
        note_template2 = load_template('components/note.html')
        dados = all_data("data/banco_notes")
        dados_mod = dados
        for index, item in enumerate(dados):
            if item.id == id_corpo_int:
                id_dados = item.id
                title_dados = item.title
                content_dados = item.content
                dados_mod.remove(item)
        notes_li = [note_template.format(id= id_dados, title=title_dados, details=content_dados)] 
        notes_li2 = [note_template2.format(title=dados.title, details=dados.content, id= dados.id,) for dados in dados_mod]
        notes_total = notes_li + notes_li2
        notes = '\n'.join(notes_total)
        return build_response(load_template('index.html').format(notes=notes)) 
    elif selecionar_str == "2":
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        id_corpo = corpo.split("&")
        id_init = id_corpo[0].split("=")
        id_corpo_str = id_init[1]
        delete_Entry(id_corpo_str,"data/banco_notes")
        note_template = load_template('components/note.html')
        notes_li = [
            note_template.format(title=dados.title, details=dados.content, id= dados.id,)
            for dados in all_data("data/banco_notes")
            ]
        notes = '\n'.join(notes_li)
        return build_response(code=303, reason='See Other', headers='Location: /')
    elif selecionar_str == "3":  
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params_1 = {}
        for chave_valor in corpo.split('&'):
            half = chave_valor.split("=")  
            chave = urllib.parse.unquote_plus(half[0], encoding='utf-8', errors='replace')
            valor = urllib.parse.unquote_plus(half[1], encoding='utf-8', errors='replace')
            params_1[chave] = valor 
        params = dict(params_1)
        del params["selecionar"]   
        update_Entry(params,"data/banco_notes")    
        return build_response(code=303, reason='See Other', headers='Location: /')     
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    else:
        if request.startswith('POST'):
            request = request.replace('\r', '')  # Remove caracteres indesejados
            # Cabeçalho e corpo estão sempre separados por duas quebras de linha
            partes = request.split('\n\n')
            corpo = partes[1]
            params = {}
            for chave_valor in corpo.split('&'):
                half = chave_valor.split("=")  
                chave = urllib.parse.unquote_plus(half[0], encoding='utf-8', errors='replace')
                valor = urllib.parse.unquote_plus(half[1], encoding='utf-8', errors='replace')
                params[chave] = valor 
            add_Entry(params,"data/banco_notes")    
            return build_response(code=303, reason='See Other', headers='Location: /')

        elif request.startswith('GET'):
            note_template = load_template('components/note.html')
            notes_li = [
            note_template.format(title=dados.title, details=dados.content, id= dados.id,)
            for dados in all_data("data/banco_notes")
            ]
            notes = '\n'.join(notes_li)
            return build_response(load_template('index.html').format(notes=notes)) 

