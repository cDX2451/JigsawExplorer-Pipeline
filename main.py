import os
import sys
import requests
import re
import mimetypes
from os import path
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import win32clipboard

file_to_upload = str(sys.argv[2])
puzzle_pieces = int(sys.argv[1])

def _mimetype(file):
    _, extension = path.splitext(file.name)
    if extension == '':
        extension = '.txt'
    mimetypes.init()
    try:
        return mimetypes.types_map[extension]
    except KeyError:
        return 'plain/text'

def _multipart_post(data):
    encoder = MultipartEncoder(fields=data)
    monitor = MultipartEncoderMonitor(encoder)
    r = requests.post("https://litterbox.catbox.moe/resources/internals/api.php", data=monitor, headers={'Content-Type': monitor.content_type})
    return r

def uploadImage(name):
    file = open(name, 'rb')
    try:
        data = {
                'time': '1h',
                'reqtype': 'fileupload',
                'userhash': '',
                'fileToUpload': (file.name, file, _mimetype(file))
        }
        response = _multipart_post(data)
    finally:
        file.close()
    return response.text

def main():
    full_link = None
    url = 'https://www.jigsawexplorer.com/jigsaw-puzzle-result/'
    post = {'image-url': uploadImage(file_to_upload),
            'credit-line': '',
            'credit-url': '',
            'puzzle-nop': puzzle_pieces,
            'mystery-puzzle': 'mystery',
            'color': 'blue'}

    x = requests.post(url, data = post)

    reg_fulllink = r'<p>Full Link:</p><textarea id="full-link" class="result-url"(.*?)readonly="readonly">(.*?)</textarea>'

    y = re.search(reg_fulllink, x.text) 
    if y:
        full_link = y
        print(full_link[2])

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(full_link[2])
    win32clipboard.CloseClipboard()

if __name__ == '__main__':
    main()