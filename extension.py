import os
import re
import sys

# https://github.com/microsoft/vscode-extension-samples/blob/main/document-editing-sample/src/extension.ts
import vscode

from ciphers.RSA import generate_rsa_key, rsa_decryption, rsa_encryption
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
            hex = keccak(text).hex()
            print(hex)
            # encrypt
            ciphertext = rsa_encryption(hex, privkey)
            print(ciphertext)
            # append to end of file
            try:
                editor.insert(
                    editor.cursor,
                    f"<ds>{ciphertext}</ds>",
                )
            except Exception:
                pass
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
            inp = vscode.window.show_open_dialog(file_picker_option)
            print(inp)
            path = os.path.abspath(inp[0]['path'][1:])
            print(path)
            with open(path, 'r') as f:
                pubkey = list(map(int, f.read().split(",")))
            print(pubkey)
            # parse signature and text
            print(re.findall(r"^(.*)<ds>(.*)</ds>$", text, re.DOTALL))
            text, signature = re.findall(r"^(.*)<ds>(.*)</ds>$", text, re.DOTALL)[0]
            print(text, signature)
            if signature:
                # decrypt
                plaintext = rsa_decryption(signature, pubkey)
                print(plaintext)
                # check with original text
                hex = keccak(text.encode('utf-8')).hex()
                print(hex)
                if plaintext == hex:
                    vscode.window.show_info_message("Verified!")
                    return
    except Exception as e:
        print(e)
    vscode.window.show_info_message("Not verified!")


@ext.command()
def generate_key_pair():
    privkey, pubkey = generate_rsa_key()

    # input path
    pubkeypath = os.path.abspath(vscode.window.show_save_dialog({
        "title": "Public key file"
    })["path"][1:])
    privkeypath = os.path.abspath(vscode.window.show_save_dialog({
        "title": "Private key file"
    })["path"][1:])
    # write file
    with open(pubkeypath, "w") as f:
        f.write(",".join(map(str, pubkey)))
    with open(privkeypath, "w") as f:
        f.write(",".join(map(str, privkey)))
    # info
    vscode.window.show_info_message(f"Public and private key successfully saved at {pubkeypath}\n{privkeypath}")


def ipc_main():
    globals()[sys.argv[1]]()


ipc_main()
