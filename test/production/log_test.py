import logging
import requests  # new import for making HTTP requests
logging.getLogger("ppocr").disabled = True


def log(message):
    """
    Prints the message locally and POSTs it to the log endpoint.
    """
    # Print the message to the console
    print(message)
    try:
        # URL for your logging endpoint; adjust port/hostname as needed
        url = "http://54.167.31.12:1337/logs"
        # Build the payload JSON
        payload = {"logs": message}
        # POST the message as JSON to the log endpoint
        response = requests.post(url, json=payload,verify=False)
        if response.status_code != 200:
            print("Error posting log:", response.text)
    except Exception as e:
        print("Failed to post log:", e)

if __name__ == "__main__":
    log(f'From GPU PULUMI ################################')
    
