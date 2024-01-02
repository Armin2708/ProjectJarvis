import pyautogui
import pytesseract
import requests
from openai import OpenAI
from pynput.keyboard import Key, Listener
import asyncio

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

top_left = None
bottom_right = None

answer = None
channelId = 1186852607113834616
apiKey = "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"
prompt = {"role": "system",
          "content": "You are a helpful assistant specialized in answering multiple-choice "
                     "questions who responds with 'My Answer :' always before an answer and with "
                     "the better choice corresponding to the most likely answer. If you are not given choices, "
                     "still answer with what you think is the right answer"
          }
keys = {
    "executeKey": Key.ctrl_l,
    "topLeftKey": Key.shift_l,
    "bottomRightKey": Key.shift_r
}  # This dictionary can map string keys to 'Key' enumeration


client = OpenAI(api_key=apiKey)


def chatGPT_answer(question):
    global answer

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            prompt,
            {"role": "user", "content": question},
        ])
    answer = completion.choices[0].message.content
    return answer


async def quiz_god():
    print("hello")
    global top_left, bottom_right, answer
    screen_width, screen_height = pyautogui.size()
    print("here")

    print(f"Width: {screen_width}, Height: {screen_height}")

    if top_left and bottom_right:
        x1, y1 = top_left
        x2, y2 = bottom_right
    else:
        return  # return if top_left and bottom_right are not set

    width = x2 - x1
    height = y2 - y1

    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    question_text = pytesseract.image_to_string(screenshot).strip()

    res = chatGPT_answer(f"Question: {question_text}")
    if res:
        print(answer)
        # Send the answer to the Discord bot via HTTP POST request
        requests.post('http://localhost:2345/post_message', json={'message': answer, 'channel_id': channelId})
    else:
        print("No answer was generated.")


def on_press(key):
    global top_left, bottom_right, keys  # global var is changed
    try:
        if key == keys["executeKey"]:  # Access key via string in dictionary
            print("execute pressed")
            asyncio.run(quiz_god())

        elif key == keys["topLeftKey"]:  # Access key via string in dictionary
            top_left = pyautogui.position()  # save position of mouse
            print(f'Top left position recorded: {top_left}')

        elif key == keys["bottomRightKey"]:  # Access key via string in dictionary
            bottom_right = pyautogui.position()  # save position of mouse
            print(f'Bottom right position recorded: {bottom_right}')
    except Exception as e:
        print(f"Exception occurred: {e}")


with Listener(on_press=on_press) as listener:
    listener.join()
