import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
def request_api_members(idBranch):
    """
    CHAMADA PARA A API, PASSANDO A URL_API QUE ESTÁ NO .ENV E IdBranch da unidade correspondente
    """
    try:
        MEMBER_API_URL = os.getenv('MEMBER_API_URL')
        url = f'{MEMBER_API_URL}idBranch={idBranch}'
        authorization = os.getenv('AUTHORIZATION_API')

        print(url)
        headers = {
            "accept": "application/json",
            "authorization": authorization
        }
        response = requests.get(url, headers=headers)
        print(authorization)
        print(response.status_code)
        return  response
    except:
        raise Exception
    
def extract_members(idBranch):
    data = []
    response = request_api_members(idBranch)
    if response.status_code == 200:
        data.append(response.json())


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



if __name__ == '__main__':
    extract_members(1)