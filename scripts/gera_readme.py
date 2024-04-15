import sqlite3

conn = sqlite3.connect('../data/ies-feeds.db')

cur = conn.cursor()

tabela_markdown = '|IES|Feed|URL|Funcional|Verificado|\n|-|-|-|-|-|\n'

query = """SELECT ies.sigla, feeds.* FROM feeds JOIN ies ON ies.id = feeds.ies_id ORDER BY ies.sigla"""

for row in cur.execute(query):
    linha = '|'
    linha += row[0]
    linha += '|'
    linha += row[2]
    linha += '|'
    linha += row[3]
    linha += '|'
    linha += row[4]
    linha += '|'
    linha += row[5]
    linha += '|\n'
    tabela_markdown += linha

#print(tabela_markdown)

conn.close()

with open("../README.md", "w") as readme:
    readme.write(tabela_markdown)

