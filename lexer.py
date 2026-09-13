"""
Lexer for IPL (Intelligent Programming Language / Aether).
Tokenizes source code into a stream of Token objects.
"""
from typing import List
from tokens import Token, TokenType


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at line {line}, column {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    KEYWORDS = {
        "let": TokenType.LET,
        "var": TokenType.VAR,
        "print": TokenType.PRINT,
        "where": TokenType.WHERE,
        "for": TokenType.FOR,
        "as": TokenType.AS,
        "prob": TokenType.PROB,
        "Prob": TokenType.PROB,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "in": TokenType.IN,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "null": TokenType.NULL,
        "secure": TokenType.SECURE,
        "sanitize": TokenType.SANITIZE,
        "trusted": TokenType.TRUSTED,
    }

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.pos = 0
        self.line = 1
        self.column = 1

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= self.length:
            return ""
        return self.source[idx]

    def advance(self) -> str:
        if self.pos >= self.length:
            return ""
        char = self.source[self.pos]
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def skip_whitespace_and_comments(self):
        while self.pos < self.length:
            char = self.peek()
            if char in (" ", "\t", "\r", "\n"):
                self.advance()
            elif char == "/" and self.peek(1) == "/":
                # Single-line comment
                while self.pos < self.length and self.peek() != "\n":
                    self.advance()
            elif char == "#":
                # Alternative comment syntax
                while self.pos < self.length and self.peek() != "\n":
                    self.advance()
            else:
                break

    def read_number(self) -> Token:
        start_col = self.column
        num_str = ""
        is_float = False

        while self.pos < self.length:
            ch = self.peek()
            if ch.isdigit():
                num_str += self.advance()
            elif ch == "." and not is_float and self.peek(1).isdigit():
                is_float = True
                num_str += self.advance()
            else:
                break

        val = float(num_str) if is_float else int(num_str)
        return Token(TokenType.NUMBER, val, self.line, start_col)

    def read_string(self, quote: str) -> Token:
        start_col = self.column
        self.advance()  # consume opening quote
        res = []

        while self.pos < self.length:
            ch = self.peek()
            if ch == quote:
                self.advance()  # consume closing quote
                return Token(TokenType.STRING, "".join(res), self.line, start_col)
            elif ch == "\\":
                self.advance()
                esc = self.advance()
                if esc == "n":
                    res.append("\n")
                elif esc == "t":
                    res.append("\t")
                elif esc == "r":
                    res.append("\r")
                elif esc == "\\":
                    res.append("\\")
                elif esc == quote:
                    res.append(quote)
                else:
                    res.append(esc)
            elif ch == "\n":
                # Multi-line strings supported
                res.append(self.advance())
            elif ch == "":
                raise LexerError("Unterminated string literal", self.line, start_col)
            else:
                res.append(self.advance())

        raise LexerError("Unterminated string literal", self.line, start_col)

    def read_identifier_or_keyword(self) -> Token:
        start_col = self.column
        ident = ""

        while self.pos < self.length:
            ch = self.peek()
            if ch.isalnum() or ch == "_":
                ident += self.advance()
            else:
                break

        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        value = ident
        if token_type == TokenType.TRUE:
            value = True
        elif token_type == TokenType.FALSE:
            value = False
        elif token_type == TokenType.NULL:
            value = None

        return Token(token_type, value, self.line, start_col)

    def tokenize(self) -> List[Token]:
        tokens = []

        while self.pos < self.length:
            self.skip_whitespace_and_comments()
            if self.pos >= self.length:
                break

            ch = self.peek()
            col = self.column
            line = self.line

            # Numbers
            if ch.isdigit():
                tokens.append(self.read_number())
                continue

            # Strings
            if ch in ('"', "'"):
                tokens.append(self.read_string(ch))
                continue

            # Identifiers & Keywords
            if ch.isalpha() or ch == "_":
                tokens.append(self.read_identifier_or_keyword())
                continue

            # Two-character operators
            if ch == "=" and self.peek(1) == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.EQ, "==", line, col))
                continue
            if ch == "!" and self.peek(1) == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.NEQ, "!=", line, col))
                continue
            if ch == "<" and self.peek(1) == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.LTE, "<=", line, col))
                continue
            if ch == ">" and self.peek(1) == "=":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.GTE, ">=", line, col))
                continue
            if ch == "-" and self.peek(1) == ">":
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.ARROW, "->", line, col))
                continue

            # Single-character tokens
            if ch == "=":
                self.advance()
                tokens.append(Token(TokenType.ASSIGN, "=", line, col))
            elif ch == "+":
                self.advance()
                tokens.append(Token(TokenType.PLUS, "+", line, col))
            elif ch == "-":
                self.advance()
                tokens.append(Token(TokenType.MINUS, "-", line, col))
            elif ch == "*":
                self.advance()
                tokens.append(Token(TokenType.STAR, "*", line, col))
            elif ch == "/":
                self.advance()
                tokens.append(Token(TokenType.SLASH, "/", line, col))
            elif ch == "%":
                self.advance()
                tokens.append(Token(TokenType.PERCENT, "%", line, col))
            elif ch == "~":
                self.advance()
                tokens.append(Token(TokenType.TILDE, "~", line, col))
            elif ch == "<":
                self.advance()
                tokens.append(Token(TokenType.LT, "<", line, col))
            elif ch == ">":
                self.advance()
                tokens.append(Token(TokenType.GT, ">", line, col))
            elif ch == "(":
                self.advance()
                tokens.append(Token(TokenType.LPAREN, "(", line, col))
            elif ch == ")":
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ")", line, col))
            elif ch == "[":
                self.advance()
                tokens.append(Token(TokenType.LBRACKET, "[", line, col))
            elif ch == "]":
                self.advance()
                tokens.append(Token(TokenType.RBRACKET, "]", line, col))
            elif ch == "{":
                self.advance()
                tokens.append(Token(TokenType.LBRACE, "{", line, col))
            elif ch == "}":
                self.advance()
                tokens.append(Token(TokenType.RBRACE, "}", line, col))
            elif ch == ":":
                self.advance()
                tokens.append(Token(TokenType.COLON, ":", line, col))
            elif ch == ";":
                self.advance()
                tokens.append(Token(TokenType.SEMICOLON, ";", line, col))
            elif ch == ",":
                self.advance()
                tokens.append(Token(TokenType.COMMA, ",", line, col))
            elif ch == ".":
                self.advance()
                tokens.append(Token(TokenType.DOT, ".", line, col))
            else:
                self.advance()
                raise LexerError(f"Unexpected character '{ch}'", line, col)

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
