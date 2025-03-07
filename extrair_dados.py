import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()
authorization = os.getenv('AUTHORIZATION_API')

def controle_requisições(url, headers):
    requisições = 0 
    while requisições <= 40:
            response = requests.get(url, headers)
            print(f"Requisição para {url} - Status: {response.status_code}")

            if response.status_code == 200:
                requisições += 1
                return response.json()
            elif response.status_code == 429:
                print('Limite de requisições atingidas aguarde 3 segundos ... ')
                time.sleep(3)
                print('Reiniciando requisições para 0')
                requisições = 0
            elif response.status_code == 404:
                print(f'Não existe essa venda, erro: {response.status_code}')
                break
            else:
                print(f'Ocorreu erro {response.status_code}')


    
def extract_members(idBranch):
    data = []
    MEMBER_API_URL = os.getenv('MEMBER_API_URL')
    skip = 0
    take = 50
    while True:
        url = f'{MEMBER_API_URL}take=50&skip={skip}&onlyPersonal=false&showActivityData=false&idBranch={idBranch}'

        headers = {
                "accept": "application/json",
                "authorization": authorization
            }
        
        resultado = controle_requisições(url, headers)
        data.append(resultado)
        if not resultado:
            break
        
        skip += take

    linhas = []
    count = 0
    for i in data:
        for alunos in i:
            idMember = alunos.get('idMember')
            firstName = alunos.get('firstName')
            lastName = alunos.get('lastName')
            branchName = alunos.get('branchName')
            gender = alunos.get('gender')
            birthDate = alunos.get('birthDate')
            memberships = alunos.get('memberships')
            
            for contrato in memberships:
                idMembership = contrato.get('idMembership')
                startDate = contrato.get('startDate')
                endDate = contrato.get('endDate')
                name = contrato.get('name')
                cancelDate = contrato.get('cancelDate')
                membershipStatus = contrato.get('membershipStatus')                                  
                idSale = contrato.get('idSale')
                saleDate = contrato.get('saleDate')
                linhas.append({
                'idMember':idMember,
                'firstName':firstName,
                'lastName':lastName,
                'branchName':branchName,
                'gender':gender,
                'birthDate':birthDate,
                'idMembership': idMembership,
                'name':name,
                'startDate':startDate,
                'endDate':endDate,
                'cancelDate':cancelDate,
                'membershipStatus':membershipStatus,
                'idSale':idSale,
                'saleDate':saleDate})
                count += 1
                print(linhas, count)
    df = pd.DataFrame(linhas)
    df.to_csv('membros.csv')

def extract_sales_by_id(file_with_idSale):

    idSale_df = pd.read_csv(file_with_idSale)
    idSale = idSale_df['idSale'].drop_duplicates()

    data = []

    for id in idSale:

        SALES_API_URL = os.getenv('SALES_API_URL')
        url = f'{SALES_API_URL}{id}'
        headers = {
            "accept": "application/json",
            "authorization": authorization
        }

        resultado = controle_requisições(url, headers)
        data.append(resultado)
            
            
    rows = []
    for itens in data:
        idSale = itens.get('idSale')
        idMember = itens.get('idMember',0)
        idProspect = itens.get('idProspect',0)
        saleDate = itens.get('saleDate',0)
        idBranch = itens.get('idBranch',0)
        saleItens = itens.get('saleItens',0)
        receivables = itens.get('receivables',0)
        saleItens = itens.get('saleItens',0)
        for sale in saleItens:
            description = sale.get('description', 0) 
            item = sale.get('item', 0)
            itemValue = sale.get('itemValue',0)
            saleValue = sale.get('saleValue',0)
            quantity = sale.get('quantity',0)
            discount = sale.get('discount',0)
            rows.append({'idSale':idSale,
                    'idMember':idMember,
                    'idProspect':idProspect,
                    'saleDate':saleDate,
                    'idBranch':idBranch,
                    'receivables':receivables,
                    'description':description,
                    'item':item,
                    'itemValue':itemValue,
                    'saleValue':saleValue,
                    'quantity':quantity,
                    'discount':discount
                    })


    dataframe = pd.DataFrame(rows)
    dataframe.to_csv('sales.csv')
           
            
def extract_receivables_by_id(file_with_idSale):

    idSale_df = pd.read_csv(file_with_idSale)
    idSale = idSale_df['idSale'].drop_duplicates()
    
    data = []

    for id in idSale:
        SALES_API_URL = os.getenv('SALES_API_URL')
        url = f'{SALES_API_URL}{id}'
        headers = {
                "accept": "application/json",
                "authorization": authorization
            }
        
        resultado = controle_requisições(url, headers)
        data.append(resultado)
                
    print(data)
    rows = []
    for itens in data:
        idSale = itens.get('idSale')
        idMember = itens.get('idMember',0)
        idProspect = itens.get('idProspect',0)
        idBranch = itens.get('idBranch',0)
        receivables = itens.get('receivables')
        for receivable in receivables:
            idReceivable = receivable.get('idReceivable',0)
            description = receivable.get('description', 'Não cadastrado')
            registrationDate = receivable.get('registrationDate',0)
            receivingDate = receivable.get('receivingDate',0)
            ammount = receivable.get('ammount',0)
            ammountPaid = receivable.get('ammountPaid',0)
            rows.append({'idSale':idSale,
                    'idMember':idMember,
                    'idProspect':idProspect,
                    'idReceivable':idReceivable,
                    'description':description,
                    'registrationDate':registrationDate,
                    'receivingDate':receivingDate,
                    'ammount':ammount,
                    'ammountPaid':ammountPaid,
                    'idBranch':idBranch})
            
                    

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv('receivables.csv')

if __name__ == '__main__':
    #extract_members(1)
    #extract_sales_by_id('membros.csv')
    extract_receivables_by_id('membros.csv')