import requests
import time
url = "http://0.0.0.0:5000/complete"

while True:
    ques=input("please enter the question(press q to exit):")
    if(ques=='q'):
        break
    t1 = time.time()
    data = {
    "code": ques,
    "cursor_position": 93
}
    response = requests.post(url, json=data)
    print(response.json())
    t2 = time.time()
    print(
        f"Time cost: {t2-t1} s"
    )