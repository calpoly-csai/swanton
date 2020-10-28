import json
import requests
import sys

RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook" 
CONFIDENCE = 0.25

def Get_Intent(
                question_str:str,
                endpoint:str=RASA_ENDPOINT) -> str:
    '''
    Takes the input question string and makes the API call to the Rasa server
    to predict the intent. If the intent is above the confidence threshold,
    it will return the predicted intent. Otherwise, it returns a generic 
    response.
    
    :param      question_str: string of the STT question
    :param      endpoint:     string of the desired endpoint
    :returns    response_str: string of Rasa's predicted response
    '''

    # Defining body content type
    headers = {
        'Content-type': 'application/json'
    }

    # Question input data
    data = {
        "sender": "test",
        "message" : question_str
    } 
    
    # Make the post request
    r = requests.post(
        url = endpoint, 
        headers=headers, 
        data = json.dumps(data)) 

    # Jsonify the response JSON 
    rasa_response = json.loads(r.text)

    print(rasa_response)

    # Checks if the confidence score is above the threshold 
    if (rasa_response != []):
        return rasa_response[0]['text']

    else: 
        return "Sorry, I do not know the answer to your question."

if __name__ == "__main__":
    intent = Get_Intent(sys.argv[1])
    print("Intent: %s" % intent)
