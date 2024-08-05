import requests
from requests_oauthlib import OAuth2Session
from keycloak import KeycloakOpenID
import json



keycloak_url = r'https://v2viqwdlbnrwzxjpznkk.dresden.de/auth/'
auth_url = r'https://v2viqwdlbnrwzxjpznkk.dresden.de/auth/realms/lissi-cloud/protocol/openid-connect/auth' 
token_url = r'https://v2viqwdlbnrwzxjpznkk.dresden.de/auth/realms/lissi-cloud/protocol/openid-connect/token' 
presentation_proof_url = r'https://v2viqwdlbnrwzxjpznkk.dresden.de/ctrl/api/v1.0/presentation-proof/connectionless?proofTemplateId='

redirect_url = r'https://localhost:5000'
proxies = {
    "http": "anywhere",
    "https": "anywhere"
}
client_id = r'lissi-agent-client'
username = 'lhd'
password = '89kDK1!'
scope = ['openid', 'user', 'profile']
#oauth = OAuth2Session(client_id=client_id, redirect_uri='https://localhost:3000', scope=scope)
tenant = 'default_tenant'
proofTamplateID = '123'
exchangeID = '123'
proof_url = 'htpss:'
headerinformation = {"Content-Type": "*/*", "x-tenant-id": "default_tenant"}
kompassProofTemplatID = '7e087848-4a92-4e7b-8d71-db3337415c1a' 
DDPassProofTemplateID = 'fef65028-f95f-49e4-bb5b-08fddb24cd0c'

tokenBearer = 'Bearer'



def get_proof_url(proofTemplateID):
    full_proof_url = presentation_proof_url+proofTemplateID
    print("In getProof the full_proof_url: ",full_proof_url)
    #print("In getProof the Beare used: ",tokenBearer)
    headerinformation = {"accept": "*/*", "x-tenant-id": "default_tenant"}
    headerinformation['Authorization'] = "Bearer "+tokenBearer
    #print("In getProof the headerinformation: ",headerinformation)
    response = requests.post(url=full_proof_url, headers=headerinformation)
    #response = requests.post(url=full_proof_url, proxies=proxies, headers=headerdata)
    print("In getProof the response: ",response.text)
    resp_data = response.json()
    proof_url = resp_data["url"]
    exchangeID = resp_data["exchangeId"]
    print("exchangeID: ", resp_data["exchangeId"])
    #print(resp_data)
    return resp_data

def get_token():
    #token_url = 'https://v2viqwdlbnrwzxjpznkk.dresden.de/auth/realms/lissi-cloud/protocol/openid-connect/token' 
    #headerinformation = {"Content-Type": "*/*", "x-tenant-id": "default_tenant"}
    userdata = {'username' : username, 'password' : password, 'grant_type':'password', 'client_id' : client_id}
    response = requests.post(url=token_url, headers=headerinformation, data=userdata)
    resp_data = response.json()
    global tokenBearer 
    tokenBearer = resp_data["access_token"]
    #print("token: ", tokenBearer)
    #print(response.text)
    #return tokenBearer
def get_presentation_proof_result(exchangeID):
    #cbd90eee-ece3-41c5-a221-4d54d601aa37
    presentation_proof_url = 'https://v2viqwdlbnrwzxjpznkk.dresden.de/ctrl/api/v1.0/presentation-proof/'
    full_proof_url = presentation_proof_url+exchangeID
    print("In getPresentationProofResult the full_proof_url: ",full_proof_url)
    headerinformation = {"accept": "*/*", "x-tenant-id": "default_tenant"}
    headerinformation['Authorization'] = "Bearer "+tokenBearer
    response = requests.get(url=full_proof_url, headers=headerinformation)
    resp_data = response.json()
    print("In getPresentationProofResult the response: ",resp_data["proof"]["state"])
    print("In getPresentationProofResult the response: ",resp_data["proof"]["verified"])
    return resp_data

 
#get_proof_url(proofTemplateID)
#get_auth_token()
#get_token()
#get_proof_url(kompassProofTemplatID)
#display qr code for proof_url
#get_presentation_proof_result('cbd90eee-ece3-41c5-a221-4d54d601aa37') #--> resp_data["proof"]["state"] und verified
#interpret_proof_result(state, verified) --> return True/False/None (Pending) within check_proof_result():

