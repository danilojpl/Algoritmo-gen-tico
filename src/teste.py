import csv 


lista = ()

with open ('src/itens.csv', encoding = 'utf-8') as itens:
    fieldnames = ['nome', 'peso', 'tempo', 'valor', 'cidade']
    lista = csv.DictWriter(itens, fieldnames=fieldnames)
    print ('hehe')
