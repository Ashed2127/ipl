"""
Parser for IPL (Intelligent Programming Language / Aether).
Parses tokens into an Abstract Syntax Tree (AST).
"""
from typing import List, Optional, Tuple
try:
    from .tokens import Token, TokenType
    from .ast_nodes import (
        Program, ASTNode, LetStatement, AssignStatement, PrintStatement, TypeAnnotation,
        Expr, Literal, Identifier, BinaryOp, UnaryOp, ListLiteral, DictLiteral, MemberAccess,
        IndexAccess, FunctionCall, Block, IfStatement, ForStatement, WhileStatement,
        BreakStatement, ContinueStatement, FunctionDef, ReturnStatement
    )
except (ImportError, ValueError):
    from tokens import Token, TokenType
    from ast_nodes import (
        Program, ASTNode, LetStatement, AssignStatement, PrintStatement, TypeAnnotation,
        Expr, Literal, Identifier, BinaryOp, UnaryOp, ListLiteral, DictLiteral, MemberAccess,
        IndexAccess, FunctionCall, Block, IfStatement, ForStatement, WhileStatement,
        BreakStatement, ContinueStatement, FunctionDef, ReturnStatement
    )


class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"ParserError at line {token.line}, column {token.column}: {message}")
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def peek_token(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self) -> Token:
        tok = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def match(self, *token_types: TokenType) -> bool:
        if self.current_token().type in token_types:
            self.advance()
            return True
        return False

    def expect(self, token_type: TokenType, err_msg: str) -> Token:
        tok = self.current_token()
        if tok.type == token_type:
            return self.advance()
        raise ParserError(f"{err_msg}. Got {tok.type.name} ('{tok.value}')", tok)

    def parse(self) -> Program:
        statements: List[ASTNode] = []
        while self.current_token().type != TokenType.EOF:
            # Skip empty semicolons
            if self.match(TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements=statements)

    def parse_statement(self) -> ASTNode:
        tok = self.current_token()
        if tok.type in (TokenType.LET, TokenType.VAR, TokenType.TRUSTED):
            return self.parse_let_statement()
        elif tok.type == TokenType.PRINT:
            return self.parse_print_statement()
        elif tok.type == TokenType.IF:
            return self.parse_if_statement()
        elif tok.type == TokenType.FOR:
            return self.parse_for_statement()
        elif tok.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif tok.type == TokenType.BREAK:
            return self.parse_break_statement()
        elif tok.type == TokenType.CONTINUE:
            return self.parse_continue_statement()
        elif tok.type == TokenType.FN:
            return self.parse_function_def()
        elif tok.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif tok.type == TokenType.LBRACE:
            return self.parse_block()
        elif tok.type == TokenType.IDENTIFIER and self.peek_token().type == TokenType.ASSIGN:
            return self.parse_assign_statement()
        else:
            expr = self.parse_expression()
            self.match(TokenType.SEMICOLON)
            return expr

    def parse_type_annotation(self) -> TypeAnnotation:
        """
        Parses type annotations like:
        : Int
        : Currency
        : Quantity
        : Sentiment
        : Prob<Sentiment>
        : Prob<Currency, 0.95>
        : Intent<Refund, Fraud, Support>
        """
        tok = self.current_token()
        if tok.type in (TokenType.IDENTIFIER, TokenType.PROB):
            type_name = str(tok.value)
            self.advance()
        else:
            raise ParserError("Expected type name in type annotation", tok)

        generic_args: List[str] = []
        min_conf = 0.0

        if self.match(TokenType.LT):
            # Generic arguments: e.g. <Currency, 0.95> or <Refund, Fraud, Support>
            while True:
                arg_tok = self.current_token()
                if arg_tok.type == TokenType.NUMBER:
                    min_conf = float(arg_tok.value)
                    self.advance()
                elif arg_tok.type in (TokenType.IDENTIFIER, TokenType.PROB, TokenType.STRING):
                    generic_args.append(str(arg_tok.value).strip('"\''))
                    self.advance()
                else:
                    raise ParserError("Expected generic type identifier or confidence number", arg_tok)

                if self.match(TokenType.COMMA):
                    continue
                break

            self.expect(TokenType.GT, "Expected '>' closing generic type arguments")

        generic_arg = generic_args[0] if generic_args else None

        return TypeAnnotation(
            name=type_name,
            generic_arg=generic_arg,
            generic_args=generic_args,
            min_confidence=min_conf
        )

    def parse_let_statement(self) -> LetStatement:
        start_tok = self.advance()  # consume 'let', 'var', or 'trusted'
        is_mutable = (start_tok.type == TokenType.VAR)
        is_trusted = (start_tok.type == TokenType.TRUSTED)

        ident_tok = self.expect(TokenType.IDENTIFIER, "Expected variable name after let/var/trusted")
        var_name = ident_tok.value

        type_ann = None
        if self.match(TokenType.COLON):
            type_ann = self.parse_type_annotation()

        refinement_expr = None
        if self.match(TokenType.WHERE):
            # Invariant condition, e.g. where (v >= 0 and v <= 100)
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                refinement_expr = self.parse_expression()
                self.expect(TokenType.RPAREN, "Expected ')' after refinement condition")
            else:
                refinement_expr = self.parse_expression()

        self.expect(TokenType.ASSIGN, "Expected '=' in variable declaration")
        val_expr = self.parse_expression()
        self.match(TokenType.SEMICOLON)

        return LetStatement(
            name=var_name,
            type_annotation=type_ann,
            refinement_expr=refinement_expr,
            value_expr=val_expr,
            is_mutable=is_mutable,
            is_trusted=is_trusted,
            line=start_tok.line
        )

    def parse_assign_statement(self) -> AssignStatement:
        ident_tok = self.advance()  # consume identifier
        self.expect(TokenType.ASSIGN, "Expected '=' in assignment")
        val_expr = self.parse_expression()
        self.match(TokenType.SEMICOLON)
        return AssignStatement(name=ident_tok.value, value_expr=val_expr, line=ident_tok.line)

    def parse_print_statement(self) -> PrintStatement:
        """
        Parses print statements:
        print x
        print "summary of" x
        print x, y
        print x for "executive"
        print x as table
        print x for "executive" as card
        print x as card for "executive"
        """
        start_tok = self.advance()  # consume 'print'
        query_str = None

        # Check if first item is a semantic query string followed by an expression
        if self.current_token().type == TokenType.STRING:
            next_tok = self.peek_token(1)
            # If next token is an expression starter (not comma, for, as, semicolon, eof)
            if next_tok.type in (TokenType.IDENTIFIER, TokenType.STRING, TokenType.LBRACKET, TokenType.LBRACE):
                query_tok = self.advance()
                query_str = query_tok.value

        exprs = []
        exprs.append(self.parse_expression())
        while self.match(TokenType.COMMA):
            exprs.append(self.parse_expression())

        audience = None
        format_style = None

        # Allow 'for' and 'as' in any order
        for _ in range(2):
            if self.match(TokenType.FOR):
                aud_tok = self.current_token()
                if aud_tok.type in (TokenType.STRING, TokenType.IDENTIFIER):
                    audience = str(aud_tok.value).strip('"\'')
                    self.advance()
                else:
                    raise ParserError("Expected audience string or identifier after 'for'", aud_tok)

            elif self.match(TokenType.AS):
                fmt_tok = self.current_token()
                if fmt_tok.type in (TokenType.IDENTIFIER, TokenType.STRING):
                    format_style = str(fmt_tok.value).strip('"\'')
                    self.advance()
                else:
                    raise ParserError("Expected format style after 'as' (e.g. table, bar_chart, badge, sentiment, card, gauge, json, tree)", fmt_tok)

        self.match(TokenType.SEMICOLON)

        return PrintStatement(
            exprs=exprs,
            query=query_str,
            audience=audience,
            format_style=format_style,
            line=start_tok.line
        )

    def parse_block(self) -> Block:
        start_tok = self.expect(TokenType.LBRACE, "Expected '{' to start block")
        stmts: List[ASTNode] = []
        while self.current_token().type not in (TokenType.RBRACE, TokenType.EOF):
            if self.match(TokenType.SEMICOLON):
                continue
            stmts.append(self.parse_statement())
        self.expect(TokenType.RBRACE, "Expected '}' to close block")
        return Block(statements=stmts, line=start_tok.line)

    def parse_if_statement(self) -> IfStatement:
        start_tok = self.advance()  # consume 'if'
        if self.current_token().type == TokenType.LPAREN:
            self.advance()
            cond = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after if condition")
        else:
            cond = self.parse_expression()
        then_block = self.parse_block()

        elif_branches: List[Tuple[Expr, Block]] = []
        while self.current_token().type == TokenType.ELIF or (
            self.current_token().type == TokenType.ELSE and self.peek_token().type == TokenType.IF
        ):
            if self.current_token().type == TokenType.ELIF:
                self.advance()
            else:
                self.advance()  # consume 'else'
                self.advance()  # consume 'if'
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                e_cond = self.parse_expression()
                self.expect(TokenType.RPAREN, "Expected ')' after elif condition")
            else:
                e_cond = self.parse_expression()
            e_block = self.parse_block()
            elif_branches.append((e_cond, e_block))

        else_block = None
        if self.match(TokenType.ELSE):
            else_block = self.parse_block()

        return IfStatement(
            condition=cond,
            then_branch=then_block,
            elif_branches=elif_branches,
            else_branch=else_block,
            line=start_tok.line
        )

    def parse_for_statement(self) -> ForStatement:
        start_tok = self.advance()  # consume 'for'
        ident_tok = self.expect(TokenType.IDENTIFIER, "Expected loop variable name after 'for'")
        self.expect(TokenType.IN, "Expected 'in' after loop variable")
        iterable_expr = self.parse_expression()
        body = self.parse_block()
        return ForStatement(
            variable=ident_tok.value,
            iterable=iterable_expr,
            body=body,
            line=start_tok.line
        )

    def parse_while_statement(self) -> WhileStatement:
        start_tok = self.advance()  # consume 'while'
        if self.current_token().type == TokenType.LPAREN:
            self.advance()
            cond = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after while condition")
        else:
            cond = self.parse_expression()
        body = self.parse_block()
        return WhileStatement(
            condition=cond,
            body=body,
            line=start_tok.line
        )

    def parse_break_statement(self) -> BreakStatement:
        start_tok = self.advance()  # consume 'break'
        self.match(TokenType.SEMICOLON)
        return BreakStatement(line=start_tok.line)

    def parse_continue_statement(self) -> ContinueStatement:
        start_tok = self.advance()  # consume 'continue'
        self.match(TokenType.SEMICOLON)
        return ContinueStatement(line=start_tok.line)

    def parse_function_def(self) -> FunctionDef:
        start_tok = self.advance()  # consume 'fn'/'func'
        name_tok = self.expect(TokenType.IDENTIFIER, "Expected function name after 'fn'")
        self.expect(TokenType.LPAREN, "Expected '(' after function name")

        params: List[str] = []
        param_types = {}
        if self.current_token().type != TokenType.RPAREN:
            while True:
                p_tok = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
                p_name = p_tok.value
                params.append(p_name)
                p_type = None
                if self.match(TokenType.COLON):
                    p_type = self.parse_type_annotation()
                param_types[p_name] = p_type
                if self.match(TokenType.COMMA):
                    continue
                break
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")

        return_type = None
        if self.match(TokenType.ARROW):
            return_type = self.parse_type_annotation()

        body = self.parse_block()
        return FunctionDef(
            name=name_tok.value,
            params=params,
            param_types=param_types,
            body=body,
            return_type=return_type,
            line=start_tok.line
        )

    def parse_return_statement(self) -> ReturnStatement:
        start_tok = self.advance()  # consume 'return'
        val_expr = None
        if self.current_token().type not in (TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            val_expr = self.parse_expression()
        self.match(TokenType.SEMICOLON)
        return ReturnStatement(value_expr=val_expr, line=start_tok.line)

    # --------------------------------------------------------------------------
    # Expression Parsing (Precedence Hierarchy)
    # --------------------------------------------------------------------------

    def parse_expression(self) -> Expr:
        return self.parse_or()

    def parse_or(self) -> Expr:
        expr = self.parse_and()
        while self.match(TokenType.OR):
            right = self.parse_and()
            expr = BinaryOp(left=expr, op="or", right=right)
        return expr

    def parse_and(self) -> Expr:
        expr = self.parse_comparison()
        while self.match(TokenType.AND):
            right = self.parse_comparison()
            expr = BinaryOp(left=expr, op="and", right=right)
        return expr

    def parse_comparison(self) -> Expr:
        expr = self.parse_additive()
        comp_tokens = (
            TokenType.EQ, TokenType.NEQ, TokenType.LT,
            TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.TILDE
        )
        while self.current_token().type in comp_tokens:
            op_tok = self.advance()
            right = self.parse_additive()
            expr = BinaryOp(left=expr, op=op_tok.value, right=right)
        return expr

    def parse_additive(self) -> Expr:
        expr = self.parse_multiplicative()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self.advance()
            right = self.parse_multiplicative()
            expr = BinaryOp(left=expr, op=op_tok.value, right=right)
        return expr

    def parse_multiplicative(self) -> Expr:
        expr = self.parse_unary()
        while self.current_token().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_tok = self.advance()
            right = self.parse_unary()
            expr = BinaryOp(left=expr, op=op_tok.value, right=right)
        return expr

    def parse_unary(self) -> Expr:
        if self.match(TokenType.MINUS):
            operand = self.parse_unary()
            return UnaryOp(op="-", operand=operand)
        if self.match(TokenType.NOT):
            operand = self.parse_unary()
            return UnaryOp(op="not", operand=operand)
        return self.parse_postfix()

    def parse_postfix(self) -> Expr:
        expr = self.parse_primary()
        while True:
            if self.match(TokenType.DOT):
                member_tok = self.expect(TokenType.IDENTIFIER, "Expected field name after '.'")
                expr = MemberAccess(target=expr, member=member_tok.value)
            elif self.match(TokenType.LPAREN):
                args: List[Expr] = []
                if self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        if self.current_token().type == TokenType.RPAREN:
                            break
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN, "Expected ')' after function arguments")
                expr = FunctionCall(callee=expr, args=args)
            elif self.match(TokenType.LBRACKET):
                idx_expr = self.parse_expression()
                self.expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexAccess(target=expr, index=idx_expr)
            else:
                break
        return expr

    def parse_primary(self) -> Expr:
        tok = self.current_token()

        # Literals
        if tok.type == TokenType.NUMBER:
            self.advance()
            type_name = "float" if isinstance(tok.value, float) else "int"
            return Literal(value=tok.value, type_name=type_name)

        if tok.type == TokenType.STRING:
            self.advance()
            return Literal(value=tok.value, type_name="string")

        if tok.type in (TokenType.TRUE, TokenType.FALSE):
            self.advance()
            return Literal(value=tok.value, type_name="bool")

        if tok.type == TokenType.NULL:
            self.advance()
            return Literal(value=None, type_name="null")

        # Identifier
        if tok.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(name=tok.value)

        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        # List Literal [e1, e2, ...]
        if self.match(TokenType.LBRACKET):
            elements = []
            if self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    if self.current_token().type == TokenType.RBRACKET:
                        break
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET, "Expected ']' at end of list")
            return ListLiteral(elements=elements)

        # Dict Literal { k: v, ... }
        if self.match(TokenType.LBRACE):
            pairs = []
            if self.current_token().type != TokenType.RBRACE:
                k = self.parse_dict_key()
                self.expect(TokenType.COLON, "Expected ':' after key in dictionary")
                v = self.parse_expression()
                pairs.append((k, v))
                while self.match(TokenType.COMMA):
                    if self.current_token().type == TokenType.RBRACE:
                        break
                    k = self.parse_dict_key()
                    self.expect(TokenType.COLON, "Expected ':' after key in dictionary")
                    v = self.parse_expression()
                    pairs.append((k, v))
            self.expect(TokenType.RBRACE, "Expected '}' at end of dictionary")
            return DictLiteral(pairs=pairs)

        raise ParserError(f"Unexpected token in expression: {tok.type.name} ('{tok.value}')", tok)

    def parse_dict_key(self) -> Expr:
        tok = self.current_token()
        if tok.type == TokenType.STRING:
            self.advance()
            return Literal(value=tok.value, type_name="string")
        elif tok.type == TokenType.IDENTIFIER:
            self.advance()
            return Literal(value=tok.value, type_name="string")
        elif tok.type == TokenType.NUMBER:
            self.advance()
            return Literal(value=tok.value, type_name="int" if isinstance(tok.value, int) else "float")
        else:
            raise ParserError(f"Expected dictionary key (string, identifier, or number), got {tok.type.name}", tok)
