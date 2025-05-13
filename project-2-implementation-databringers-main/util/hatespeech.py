import requests
import json
def hs_check_comment(text):

  CONF_THRESHOLD = 0.9
  print(text)

  data = {
    "token": "dc56a8decef1c160b82629ab89efccc4",
    "text": text
  }

  try:
        response = requests.post("https://api.moderatehatespeech.com/api/v1/moderate/", json=data).json()

        # Check if the expected keys are in the response
        if 'class' in response and 'confidence' in response:
            return response["class"] == "flag" and float(response["confidence"]) > CONF_THRESHOLD
        else:
            # Handle unexpected response structure
            print("Unexpected response structure:", response)
            return False

  except Exception as e:
        # Handle exceptions such as network errors
        print("Error during API request:", e)
        return False
