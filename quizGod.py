import pyautogui
import pytesseract
import requests
import openai
from pynput import keyboard
import asyncio

pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/Cellar/tesseract/5.3.3/bin/tesseract"

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


def chatGPT_answer(question):
    global answer
    openai.api_key = apiKey
    completion = openai.Completion.create(
        model="gpt-4",
        messages=[
            prompt,
            {"role": "user", "content": question},
        ])
    answer = completion.choices[0].message.content
    return answer


async def kahoot_god():
    global top_left, bottom_right, answer
    screen_width, screen_height = pyautogui.size()

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
    global top_left, bottom_right
    try:
        # Check if the combination of keys "control", "command", and "t" is pressed
        if all([key == getattr(keyboard.Key, k) for k in ['cmd']]):
            print("cmd pressed")
            asyncio.run(kahoot_god())

        elif key == keyboard.Key.shift_l:
            top_left = pyautogui.position()  # save position of mouse
            print(f'Top left position recorded: {top_left}')

        elif key == keyboard.Key.shift_r:
            bottom_right = pyautogui.position()  # save position of mouse
            print(f'Bottom right position recorded: {bottom_right}')
    except AttributeError:
        pass  # Ignore if the pressed key is not an attribute of Key


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
