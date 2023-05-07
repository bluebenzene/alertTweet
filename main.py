import requests
import os
import json
import subprocess
import datetime
#
bearer_token = os.environ.get("twitterbearer")
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r
def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()
def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None
    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))

def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "from:PineprosI", "tag": "PineprosI"},
        {"value": "from:fomocapdao", "tag": "fomocapdao"},
        {"value": "from:zerohedge", "tag": "zerohedge"},
        {"value": "from:DeItaone", "tag": "DeItaone"},

    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


# def get_stream(set):
#     response = requests.get(
#         "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
#     )
#     print(response.status_code)
#     if response.status_code != 200:
#         raise Exception(
#             "Cannot get stream (HTTP {}): {}".format(
#                 response.status_code, response.text
#             )
#         )
#     for response_line in response.iter_lines():
#         if response_line:
#             json_response = json.loads(response_line)
#             print(json.dumps(json_response, indent=4, sort_keys=True))
def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)

            # Extract the message data and matching rule tag
            message = json_response.get("data", {}).get("text", "")
            tag = json_response.get("matching_rules", [{}])[0].get("tag", "")

            # Get the current time in hh:mm format
            time_str = datetime.datetime.now().strftime("%H:%M:%S")

            # Print the formatted message output
            output = f"{time_str}:{tag}:{message}"
            print(output)

            # Play the alert sound for the matching rule tag
            if tag:
                play_alert(tag)


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


# {"data": [{"value": "from:zerohedge", "id": "1654163977012649990"}, {"value": "from:DeItaone", "id": "1654163977012649993"}, {"value": "from:PineprosI", "id": "1654163977012649992"}, {"value": "from:fomocapdao", "id": "1654163977012649991"}], "meta": {"sent": "2023-05-04T16:40:01.122Z", "summary": {"created": 4, "not_created": 0, "valid": 4, "invalid": 0}}}

# user  data id store
# PineprosI 1654192412288339980
# fomocapdao 1654193909109608465
# zerohedge 1654198491516751873
# DeItaone 1654163977012649993
def play_alert(tag):
    # Map each tag to a corresponding alert file name
    alert_files = {
        "PineprosI": "iamwayalert.mp3",
        "fomocapdao": "maybealertr.mp3",
        "zerohedge": "ShutdownNextok.mp3",
        "DeItaone": "aenergyEnergy.mp3"
    }

    # Check if the given tag has a corresponding alert file
    if tag in alert_files:
        file_name = alert_files[tag]
        # play the alert sound for the given tag
        proc = subprocess.Popen(["play", f"alert_sound/{file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()


if __name__ == "__main__":
    main()
    # play_alert("whatalert.mp3")
    # play_alert("maybealertr.mp3")
