import json
import requests  # Import the requests library to handle HTTP requests

def emotion_detector(text_to_analyse):
    # URL of the emotion detection service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # Constructing the request payload in the expected format
    myobj = { "raw_document": { "text": text_to_analyse } }
    # Custom header specifying the model ID for the emotion detection service
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    # Sending a POST request to the emotion detection API
    response = requests.post(url, json=myobj, headers=header, timeout=5)

    # If the response status code is 200, extract the label and score from the response
    if response.status_code == 200:
        # Parse the response from the API
        formatted_response = json.loads(response.text)
        anger_score = formatted_response['emotionPredictions'][0]['emotion']['anger']
        disgust_score = formatted_response['emotionPredictions'][0]['emotion']['disgust']
        fear_score = formatted_response['emotionPredictions'][0]['emotion']['fear']
        joy_score = formatted_response['emotionPredictions'][0]['emotion']['joy']
        sadness_score = formatted_response['emotionPredictions'][0]['emotion']['sadness']
        output = {'anger': anger_score, 'disgust': disgust_score, 'fear': fear_score, \
            'joy': joy_score, 'sadness': sadness_score}
        output['dominant_emotion'] = max(output, key=output.get)
    # If the response status code is 400, set all keys to None
    elif response.status_code == 400:
        output = {'anger': None, 'disgust': None, 'fear': None, \
            'joy': None, 'sadness': None, 'dominant_emotion': None}
    # For any other unexpected status codes, set label and score to None
    else:
        output = {'anger': None, 'disgust': None, 'fear': None, \
            'joy': None, 'sadness': None, 'dominant_emotion': None}

    return output
    