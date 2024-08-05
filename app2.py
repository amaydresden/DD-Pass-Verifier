from flask import Flask, jsonify, request
import time, lissi_req, qrcode

app = Flask(__name__)

current_proof_result = False
kompassProofTemplatID = '7e087848-4a92-4e7b-8d71-db3337415c1a' 
DDPassProofTemplateID = 'fef65028-f95f-49e4-bb5b-08fddb24cd0c'
global exchangeID

def create_qrcode(weblink_data, exchangeID):
    qrimg = qrcode.make(weblink_data)
    type(qrimg)
    qrimg.save("static/myimg"+str(exchangeID)+".png")
    return "myimg"+str(exchangeID)+".png"

@app.route('/qr-code', methods=['GET'])
def get_qr_code():
    # Hier würde normalerweise der QR-Code und der zugehörige Weblink abgerufen werden
    resp_data = lissi_req.get_proof_url(kompassProofTemplatID)
    proof_url = resp_data["url"]
    exchangeID = resp_data["exchangeId"]
    imagefilename = create_qrcode(weblink_data=proof_url, exchangeId=exchangeID)
    #qr_code = "example_qr_code.png"
    #weblink = "https://example.com"
    return jsonify({'qr_code': imagefilename, 'weblink': proof_url})

@app.route('/proof-result', methods=['POST'])
def receive_proof_result():
    global current_proof_result
    current_proof_result = True
    return 'Proof result received successfully', 200

@app.route('/check-proof-result', methods=['GET'])
def check_proof_result():
    resp_data = lissi_req.get_presentation_proof_result(exchangeID)
    status = resp_data["proof"]["state"]
    verified = resp_data["proof"]["verified"]
    
    if verified == True:        
        return jsonify({'proof_result':  'erfolgreich'})
    elif verified == False:
        return jsonify({'proof_result': 'ungultig'})
    elif verified == None:
        return jsonify({'proof_result': 'ausstehend'})

if __name__ == '__main__':
    app.run(debug=True)