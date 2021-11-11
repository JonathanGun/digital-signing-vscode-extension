# https://github.com/microsoft/vscode-extension-samples/blob/main/document-editing-sample/src/extension.ts
import vscode
import hashlib

ext = vscode.Extension(name="digital-signing", display_name="Digital Signing", version="0.0.1")


@ext.command()
def sign():
    editor = vscode.window.ActiveTextEditor()
    if editor:
        text = editor.document.get_text().encode('utf-8')
        hex = hashlib.sha256(text).hexdigest()
        editor.insert(
            editor.cursor,
            f"<ds>{hex}</ds>",
        )


vscode.build(ext)
