import sys
# https://github.com/microsoft/vscode-extension-samples/blob/main/document-editing-sample/src/extension.ts
import vscode
# import hashlib
import re
import os
from ciphers.RSA import rsa_encryption, rsa_decryption

from hash_algo.sha3 import keccak

ext = vscode.Extension(name="digital-signing", display_name="Digital Signing", version="0.0.1")

file_picker_option = {
    "can_select_many": True,
    "open_label": "Open",
    "filters": {
        "Text files": ['pub', 'pri', 'txt'],
        "All files": ['*'],
    }
}


@ext.command()
def sign():
    try:
        editor = vscode.window.ActiveTextEditor()
        if editor:
            text = editor.document.get_text().encode('utf-8')
            print(text)
            # input private key
            path = os.path.abspath(vscode.window.show_open_dialog(file_picker_option)[0]['path'][1:])
            print(path)
            with open(path, 'r') as f:
                privkey = list(map(int, f.read().split(",")))
            # digest / hash
            hex = keccak(512, 512, text, 0x06, 256 // 8).hex()
            print(hex)
            # encrypt
            ciphertext = rsa_encryption(hex, privkey)
            print(ciphertext)
            # append to end of file
            editor.insert(
                editor.cursor,
                f"<ds>{ciphertext}</ds>",
            )
            vscode.window.show_info_message("Sign success!")
    except Exception as e:
        print(e)
        vscode.window.show_info_message("Failed to sign!")


@ext.command()
def verify():
    try:
        editor = vscode.window.ActiveTextEditor()
        if editor:
            text = editor.document.get_text()
            print(text)
            # input public key
            path = os.path.abspath(vscode.window.show_open_dialog(file_picker_option)[0]['path'][1:])
            print(path)
            with open(path, 'r') as f:
                pubkey = list(map(int, f.read().split(",")))
            # parse signature and text
            print(re.findall("^(.*)<ds>(.*)</ds>$", text))
            text, signature = re.findall("^(.*)<ds>(.*)</ds>$", text)[0]
            print(text, signature)
            if signature:
                # decrypt
                plaintext = rsa_decryption(signature, pubkey)
                print(plaintext)
                # check with original text
                hex = keccak(512, 512, text.encode('utf-8'), 0x06, 256 // 8).hex()
                print(hex)
                if plaintext == hex:
                    vscode.window.show_info_message("Verified!")
                    return
    except Exception as e:
        print(e)
        vscode.window.show_info_message("Not verified!")


vscode.build(ext)
