import sqlite3
import sys

conn = sqlite3.connect('../data/ies-feeds.db')

regioes = {'NE': '_nordeste', 'N': '_norte', 'CO': '_centro-oeste', 'SE': '_sudeste', 'S': '_sul'}

condicao = ''
sufixo_arquivo = ''
pasta = '../'
sufixo_grupo = ''

if(len(sys.argv) > 1):
    regiao = sys.argv[1].upper()
    if(regiao in regioes.keys()):
        condicao = "AND ufs.regiao = '" + regiao + "'\n    "
        sufixo_arquivo = regioes[regiao]
        pasta += 'regioes/'
        sufixo_grupo += ' - ' + regiao
    else:
    	print('região não encontrada')
    	sys.exit()

feeds = '<opml version="2.0">\n\t<body>\n\t\t<outline text="IES Feeds'+ sufixo_grupo +'" title="IES Feeds'+ sufixo_grupo +'">\n'

cur = conn.cursor()

query = """
    SELECT feeds.id, feeds.titulo, feeds.url
    FROM feeds 
    JOIN ies_ufs on ies_ufs.ies_id = feeds.ies_id 
    JOIN ufs on ufs.id = ies_ufs.uf_id
    WHERE funcional = 'S'
    """ + condicao + """
    GROUP BY feeds.id
    ORDER BY feeds.titulo"""
	
#print(query)

for row in cur.execute(query):
    nome = row[1]
    url_utf8 = row[2].replace("'b", "").replace("''", "'").replace("&", "&amp;").replace("&amp;amp;", "&amp;")
    linha = f"\t\t\t\t<outline title='{nome}' xmlUrl='{url_utf8}' />\n"
    feeds += linha

conn.close()

feeds += '\t\t</outline>\n\t</body>\n</opml>'

with open(pasta+'ies-feeds'+sufixo_arquivo+'.xml', 'w', encoding="utf-8") as feeds_file:
    feeds_file.write(feeds)
