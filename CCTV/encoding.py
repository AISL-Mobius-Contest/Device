import base64

def encode_img(filename):
    with open(filename, "rb") as imageFile:
        msg = base64.b64encode(imageFile.read())
    return msg