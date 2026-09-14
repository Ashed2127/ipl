# IPL (Intelligent Programming Language) for Visual Studio Code

Official Visual Studio Code extension providing syntax highlighting, language configuration, and keyword coloring for the **IPL (Intelligent Programming Language / Aether)** neuro-symbolic language.

## Features

- **Syntax Highlighting**: Supports `.ipl` and `.aether` source files.
- **Keywords**: Highlights `intent`, `where`, `sanitize`, `trusted`, `import`, `as`, `fn`, `let`, `var`, `print`, `return`, `if`, `else`, `while`, `for`, `in`.
- **Semantic Types**: Highlights native semantic types (`Currency`, `Sentiment`, `Quantity`, `Prob`, `Intent`).
- **Standard Library Primitives**: Highlighting for `sha256`, `md5`, `base64_encode`, `base64_decode`, `json_encode`, `json_decode`, `now`, `db_write`, `audit_trace`.
- **Automatic Bracket Matching & Comment Toggling**: Using standard `//` and `/* */`.

## Installation (Local Development)

To load the extension into your local VS Code installation:

```bash
# Symlink or copy the extension directory to your VS Code extensions folder:
ln -s "$(pwd)/vscode-ipl" ~/.vscode/extensions/vscode-ipl
```

Then restart Visual Studio Code or reload your window (`Ctrl+Shift+P` -> `Developer: Reload Window`). Any `.ipl` file will immediately have full syntax highlighting.

## Packaging

To package into a `.vsix` bundle:

```bash
npx @vscode/vsce package
```
