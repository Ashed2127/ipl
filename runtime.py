"""
Runtime Environment, IValue representation, and Interpreter for IPL (Intelligent Programming Language / Aether).
"""
from typing import Any, Dict, List, Optional, Tuple
from rich.console import Console
from rich.text import Text

from ast_nodes import (
    Program, ASTNode, LetStatement, AssignStatement, PrintStatement, TypeAnnotation,
    Expr, Literal, Identifier, BinaryOp, UnaryOp, ListLiteral, DictLiteral, MemberAccess
)
from semantic_engine import SemanticEngine
from formatter import IntelligentFormatter
from security_engine import SecurityEngine


class IValue:
    """
    Intelligent Value representation.
    Wraps raw runtime data with type tags, Bayesian/neural confidence scores,
    provenance, refinement metadata, and mutability flags.
    """
    def __init__(
        self,
        raw_value: Any,
        type_name: str = "Any",
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
        invariant_violation: Optional[str] = None,
        is_mutable: bool = False
    ):
        self.raw_value = raw_value
        self.type_name = type_name
        self.confidence = max(0.0, min(1.0, float(confidence)))
        self.metadata = metadata or {}
        self.invariant_violation = invariant_violation
        self.is_mutable = is_mutable

    def get_display_value(self) -> Any:
        if isinstance(self.raw_value, dict):
            if "formatted" in self.raw_value:
                return self.raw_value["formatted"]
            if "summary" in self.raw_value:
                return self.raw_value["summary"]
        return self.raw_value

    def __repr__(self) -> str:
        conf_pct = int(self.confidence * 100)
        mut_str = "var" if self.is_mutable else "let"
        return f"IValue({mut_str} {self.type_name}: {repr(self.raw_value)}, conf={conf_pct}%)"

    def get_numeric(self) -> float:
        if isinstance(self.raw_value, (int, float)):
            return float(self.raw_value)
        if isinstance(self.raw_value, dict):
            if "amount" in self.raw_value:
                return float(self.raw_value["amount"])
            if "value" in self.raw_value:
                return float(self.raw_value["value"])
            if "score" in self.raw_value:
                return float(self.raw_value["score"])
        try:
            return float(str(self.raw_value))
        except ValueError:
            return 0.0


class Environment:
    def __init__(self, parent=None, console: Optional[Console] = None):
        self.bindings: Dict[str, IValue] = {}
        self.parent = parent
        self.console = console or Console()

    def set(self, name: str, value: IValue, is_reassignment: bool = False):
        if is_reassignment:
            # Check if variable exists and is mutable
            if name in self.bindings:
                existing = self.bindings[name]
                if not existing.is_mutable:
                    raise TypeError(
                        f"Cannot reassign immutable binding '{name}' declared with 'let'. "
                        f"Declare with 'var' to enable mutation."
                    )
                value.is_mutable = True
                self.bindings[name] = value
                return
            if self.parent:
                self.parent.set(name, value, is_reassignment=True)
                return
            raise NameError(f"Cannot reassign undeclared variable '{name}'")

        self.bindings[name] = value

    def get(self, name: str) -> IValue:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.get(name)

        # Neuro-Symbolic Self-Healing symbol resolution
        healing_match = SemanticEngine.find_self_healing_variable(name, self.all_symbols())
        if healing_match:
            matched_name, conf = healing_match
            self.console.print(
                f"[bold magenta]✨ [Self-Healing][/bold magenta] "
                f"Resolved undefined identifier [bold yellow]'{name}'[/bold yellow] -> "
                f"[bold green]'{matched_name}'[/bold green] (Confidence: {int(conf*100)}%)"
            )
            return self.get_exact(matched_name)

        available = list(self.all_symbols().keys())
        raise NameError(f"Undefined variable '{name}'. Did you mean one of: {available}?")

    def get_exact(self, name: str) -> IValue:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent:
            return self.parent.get_exact(name)
        raise NameError(f"Variable '{name}' not found")

    def all_symbols(self) -> Dict[str, IValue]:
        symbols = {}
        if self.parent:
            symbols.update(self.parent.all_symbols())
        symbols.update(self.bindings)
        return symbols


class Interpreter:
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.formatter = IntelligentFormatter(self.console)
        self.global_env = Environment(console=self.console)
        self.security_engine = SecurityEngine()

    def run(self, program: Program, source_code: str = ""):
        # Security check before execution
        if source_code:
            security_analysis = self.security_engine.analyze_code(source_code)
            if security_analysis["is_malicious"]:
                self.console.print(
                    f"[bold red]🚨 SECURITY ALERT: {security_analysis['threat_level'].upper()} THREAT DETECTED[/bold red]"
                )
                self.console.print(f"[red]Threat Score: {security_analysis['threat_level']}[/red]")
                
                if security_analysis["detected_threats"]:
                    self.console.print("[bold red]Detected Threats:[/bold red]")
                    for threat in security_analysis["detected_threats"]:
                        self.console.print(f"  • [yellow]{threat['type']}[/yellow]: {threat['match']}")
                
                if security_analysis["dangerous_keywords"]:
                    self.console.print("[bold red]Dangerous Keywords:[/bold red]")
                    for kw in security_analysis["dangerous_keywords"]:
                        self.console.print(f"  • [yellow]{kw['keyword']}[/yellow]: {kw['description']}")
                
                self.console.print("[bold red]Execution blocked for security reasons.[/bold red]")
                return
            
            # Check execution safety
            is_safe, warnings = self.security_engine.check_execution_safety(source_code)
            if not is_safe:
                self.console.print("[bold yellow]⚠️ SECURITY WARNINGS:[/bold yellow]")
                for warning in warnings:
                    self.console.print(f"  • {warning}")
                self.console.print("[yellow]Proceeding with caution...[/yellow]\n")
        
        for stmt in program.statements:
            self.execute_statement(stmt, self.global_env)

    def execute_statement(self, stmt: ASTNode, env: Environment):
        if isinstance(stmt, LetStatement):
            self.execute_let(stmt, env)
        elif isinstance(stmt, AssignStatement):
            self.execute_assign(stmt, env)
        elif isinstance(stmt, PrintStatement):
            self.execute_print(stmt, env)
        else:
            raise NotImplementedError(f"Statement {type(stmt).__name__} not implemented")

    def execute_let(self, stmt: LetStatement, env: Environment):
        # 1. Evaluate right-hand side expression
        evaluated = self.evaluate_expr(stmt.value_expr, env)

        # 2. If trusted, skip security checks
        if stmt.is_trusted:
            self.console.print(f"[green]🔒 Trusted variable '{stmt.name}' - security checks bypassed[/green]")
        else:
            # Security check on raw string data
            if isinstance(evaluated.raw_value, str):
                data_security = self.security_engine.analyze_data(evaluated.raw_value)
                if data_security["is_malicious"]:
                    self.console.print(
                        f"[bold red]🚨 DATA SECURITY ALERT: {data_security['risk_level'].upper()} RISK DETECTED[/bold red]"
                    )
                    if data_security["detected_risks"]:
                        self.console.print("[red]Detected Risks:[/red]")
                        for risk in data_security["detected_risks"]:
                            self.console.print(f"  • [yellow]{risk['type']}[/yellow]: {risk['match']}")
                    
                    # Sanitize the data
                    sanitized = self.security_engine.sanitize_string(evaluated.raw_value)
                    self.console.print(f"[yellow]Data sanitized for security. Original length: {len(evaluated.raw_value)}, Sanitized: {len(sanitized)}[/yellow]")
                    evaluated = IValue(raw_value=sanitized, type_name=evaluated.type_name, confidence=evaluated.confidence)

        # 3. Semantic Extraction & Type Coercion based on TypeAnnotation
        ivalue = self.apply_type_annotation(evaluated, stmt.type_annotation, stmt.name, skip_security=stmt.is_trusted)
        ivalue.is_mutable = stmt.is_mutable

        # 3. Refinement / Invariant Validation
        if stmt.refinement_expr is not None:
            ref_env = Environment(parent=env, console=self.console)
            val_to_bind = ivalue.raw_value
            if isinstance(val_to_bind, dict) and "amount" in val_to_bind:
                val_to_bind = val_to_bind["amount"]
            elif isinstance(val_to_bind, dict) and "value" in val_to_bind:
                val_to_bind = val_to_bind["value"]

            ref_env.set("v", IValue(raw_value=val_to_bind, type_name="RefinementTarget", confidence=ivalue.confidence))
            ref_env.set("confidence", IValue(raw_value=ivalue.confidence, type_name="Float"))

            # Expose raw dict fields directly if dict
            if isinstance(ivalue.raw_value, dict):
                for k, v in ivalue.raw_value.items():
                    ref_env.set(str(k), IValue(raw_value=v, type_name="RefinementProperty"))

            ref_result = self.evaluate_expr(stmt.refinement_expr, ref_env)
            is_valid = bool(ref_result.raw_value)

            if not is_valid:
                violation_msg = (
                    f"Invariant breach on '{stmt.name}': value {val_to_bind} "
                    f"failed condition."
                )
                self.console.print(
                    f"[bold red]⚠️ [Invariant Breach][/bold red] "
                    f"[yellow]{violation_msg}[/yellow] "
                    f"[dim](Self-healing guardrails engaged)[/dim]"
                )
                ivalue.invariant_violation = violation_msg

        # 4. Bind into environment
        env.set(stmt.name, ivalue)

    def execute_assign(self, stmt: AssignStatement, env: Environment):
        evaluated = self.evaluate_expr(stmt.value_expr, env)
        env.set(stmt.name, evaluated, is_reassignment=True)

    def apply_type_annotation(self, ivalue: IValue, type_ann: Optional[TypeAnnotation], var_name: str = "", skip_security: bool = False) -> IValue:
        if type_ann is None:
            return ivalue

        tname = type_ann.name
        raw = ivalue.raw_value

        # Security check for string data (skip if trusted)
        if isinstance(raw, str) and not skip_security:
            data_security = self.security_engine.analyze_data(raw)
            if data_security["is_malicious"]:
                self.console.print(
                    f"[bold red]🚨 DATA SECURITY ALERT: {data_security['risk_level'].upper()} RISK DETECTED[/bold red]"
                )
                if data_security["detected_risks"]:
                    self.console.print("[red]Detected Risks:[/red]")
                    for risk in data_security["detected_risks"]:
                        self.console.print(f"  • [yellow]{risk['type']}[/yellow]: {risk['match']}")
                
                # Sanitize the data
                sanitized = self.security_engine.sanitize_string(raw)
                self.console.print(f"[yellow]Data sanitized for security. Original length: {len(raw)}, Sanitized: {len(sanitized)}[/yellow]")
                raw = sanitized

        # Semantic extraction from strings
        if isinstance(raw, str):
            if tname == "Currency":
                data = SemanticEngine.extract_currency(raw)
                return IValue(
                    raw_value=data,
                    type_name="Currency",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname == "Sentiment":
                data = SemanticEngine.extract_sentiment(raw)
                return IValue(
                    raw_value=data,
                    type_name="Sentiment",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname == "Date":
                data = SemanticEngine.extract_date(raw)
                return IValue(
                    raw_value=data,
                    type_name="Date",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname == "Quantity":
                data = SemanticEngine.extract_quantity(raw)
                return IValue(
                    raw_value=data,
                    type_name="Quantity",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname == "Intent":
                candidates = type_ann.generic_args if type_ann.generic_args else None
                data = SemanticEngine.extract_intent(raw, candidates)
                return IValue(
                    raw_value=data,
                    type_name="Intent",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname in ("Int", "Integer"):
                data = SemanticEngine.extract_number(raw, as_float=False)
                return IValue(
                    raw_value=data["value"],
                    type_name="Int",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname == "Float":
                data = SemanticEngine.extract_number(raw, as_float=True)
                return IValue(
                    raw_value=data["value"],
                    type_name="Float",
                    confidence=data["confidence"],
                    metadata={"origin_text": raw}
                )
            elif tname == "Percentage":
                qdata = SemanticEngine.extract_quantity(raw)
                return IValue(
                    raw_value=qdata["value"],
                    type_name="Percentage",
                    confidence=qdata["confidence"],
                    metadata={"unit": "%", "origin_text": raw}
                )

        # Probabilistic wrapper: Prob<T> or Prob<T, min_conf>
        if tname == "Prob":
            inner_type = type_ann.generic_arg
            if inner_type:
                dummy_ann = TypeAnnotation(name=inner_type)
                inner_ivalue = self.apply_type_annotation(ivalue, dummy_ann, var_name)
                result_val = IValue(
                    raw_value=inner_ivalue.raw_value,
                    type_name=f"Prob<{inner_type}>",
                    confidence=inner_ivalue.confidence,
                    metadata=inner_ivalue.metadata
                )
            else:
                result_val = IValue(
                    raw_value=ivalue.raw_value,
                    type_name="Prob",
                    confidence=ivalue.confidence,
                    metadata=ivalue.metadata
                )

            # Check min_confidence threshold
            if type_ann.min_confidence > 0.0 and result_val.confidence < type_ann.min_confidence:
                self.console.print(
                    f"[bold yellow]⚠️ [Uncertainty Guardrail][/bold yellow] "
                    f"Variable [bold cyan]'{var_name}'[/bold cyan] confidence ({int(result_val.confidence*100)}%) "
                    f"is below declared threshold ({int(type_ann.min_confidence*100)}%)."
                )
            return result_val

        # Direct casts
        if tname in ("Int", "Integer") and isinstance(raw, (int, float)):
            return IValue(int(raw), "Int", ivalue.confidence)
        if tname == "Float" and isinstance(raw, (int, float)):
            return IValue(float(raw), "Float", ivalue.confidence)
        if tname == "String":
            return IValue(str(raw), "String", ivalue.confidence)

        return IValue(raw, tname, ivalue.confidence, ivalue.metadata)

    def execute_print(self, stmt: PrintStatement, env: Environment):
        # 1. Evaluate printed expressions
        evaluated_values: List[IValue] = [self.evaluate_expr(e, env) for e in stmt.exprs]

        primary_val = evaluated_values[0] if len(evaluated_values) == 1 else evaluated_values
        raw_target = primary_val.raw_value if isinstance(primary_val, IValue) else [v.raw_value for v in evaluated_values]

        # Case A: Semantic Query (e.g. print "summary of" x)
        if stmt.query is not None:
            query_answer = SemanticEngine.evaluate_semantic_query(stmt.query, raw_target)
            if stmt.audience:
                query_answer = SemanticEngine.adapt_for_audience(query_answer, stmt.audience)

            self.console.print(f"[bold cyan]🔍 Query Intent: \"{stmt.query}\"[/bold cyan]")
            if stmt.format_style:
                self.formatter.render_format(query_answer, stmt.format_style, primary_val if isinstance(primary_val, IValue) else None)
            else:
                self.console.print(query_answer)
            return

        # Case B: Audience Adaptation + Presentation Formatter
        if stmt.audience is not None:
            adapted = SemanticEngine.adapt_for_audience(raw_target, stmt.audience)
            if stmt.format_style:
                self.formatter.render_format(
                    adapted,
                    stmt.format_style,
                    primary_val if isinstance(primary_val, IValue) else None,
                    title_override=f"💼 {stmt.audience.upper()} ADAPTIVE VIEW"
                )
            else:
                self.console.print(adapted)
            return

        # Case C: Presentation Style
        if stmt.format_style is not None:
            self.formatter.render_format(
                value=raw_target,
                format_style=stmt.format_style,
                raw_ivalue=primary_val if isinstance(primary_val, IValue) else None
            )
            return

        # Case D: Default Intelligent Contextual Print
        rendered_parts = []
        for v in evaluated_values:
            rendered_parts.append(self.format_ivalue_for_display(v))
        self.console.print(" ".join(rendered_parts))

    def format_ivalue_for_display(self, ivalue: IValue) -> str:
        raw = ivalue.raw_value

        # If Invariant breached
        violation_suffix = ""
        if ivalue.invariant_violation:
            violation_suffix = " [bold red]⚠️ [INVARIANT BREACH][/bold red]"

        # If Currency
        if ivalue.type_name == "Currency" and isinstance(raw, dict):
            conf_str = f"[dim]({int(ivalue.confidence*100)}% conf)[/dim]"
            return f"[bold green]{raw.get('formatted', '')}[/bold green] {conf_str}{violation_suffix}"

        # If Sentiment
        if ivalue.type_name == "Sentiment" and isinstance(raw, dict):
            color = "green" if raw.get("score", 0) > 0.1 else ("red" if raw.get("score", 0) < -0.1 else "yellow")
            return f"[{color}]{raw.get('summary', '')}[/{color}] [dim]({int(ivalue.confidence*100)}% conf)[/dim]{violation_suffix}"

        # If Date
        if ivalue.type_name == "Date" and isinstance(raw, dict):
            return f"[bold cyan]📅 {raw.get('readable', '')}[/bold cyan] [dim](ISO: {raw.get('iso', '')})[/dim]{violation_suffix}"

        # If Quantity
        if ivalue.type_name == "Quantity" and isinstance(raw, dict):
            return f"[bold blue]📏 {raw.get('formatted', '')}[/bold blue] [dim]({int(ivalue.confidence*100)}% conf)[/dim]{violation_suffix}"

        # If Intent
        if ivalue.type_name == "Intent" and isinstance(raw, dict):
            return f"[bold magenta]🎯 {raw.get('summary', '')}[/bold magenta]{violation_suffix}"

        # If Prob
        if ivalue.type_name.startswith("Prob"):
            meter = "■" * int(ivalue.confidence * 10) + "□" * (10 - int(ivalue.confidence * 10))
            return f"[italic]{raw}[/italic] [bold yellow][{int(ivalue.confidence*100)}% {meter}][/bold yellow]{violation_suffix}"

        # If dictionary
        if isinstance(raw, dict):
            items = [f"[cyan]{k}[/cyan]: {v}" for k, v in raw.items()]
            return "{" + ", ".join(items) + "}" + violation_suffix

        # If list
        if isinstance(raw, list):
            items = [str(item) for item in raw]
            return "[" + ", ".join(items) + "]" + violation_suffix

        # If plain string or number
        if isinstance(raw, str):
            return raw + violation_suffix
        return str(raw) + violation_suffix

    # --------------------------------------------------------------------------
    # Expression Evaluation
    # --------------------------------------------------------------------------

    def evaluate_expr(self, expr: Expr, env: Environment) -> IValue:
        if isinstance(expr, Literal):
            return IValue(raw_value=expr.value, type_name=expr.type_name.capitalize())

        if isinstance(expr, Identifier):
            return env.get(expr.name)

        if isinstance(expr, ListLiteral):
            eval_elems = [self.evaluate_expr(e, env).raw_value for e in expr.elements]
            return IValue(raw_value=eval_elems, type_name="List")

        if isinstance(expr, DictLiteral):
            eval_dict = {}
            for k_expr, v_expr in expr.pairs:
                k_val = self.evaluate_expr(k_expr, env).raw_value
                v_val = self.evaluate_expr(v_expr, env).raw_value
                eval_dict[k_val] = v_val
            return IValue(raw_value=eval_dict, type_name="Dict")

        if isinstance(expr, MemberAccess):
            target_val = self.evaluate_expr(expr.target, env)
            raw = target_val.raw_value
            member = expr.member

            # Built-in properties on IValue
            if member == "confidence":
                return IValue(raw_value=target_val.confidence, type_name="Float")
            if member == "type":
                return IValue(raw_value=target_val.type_name, type_name="String")
            if member == "raw":
                return IValue(raw_value=target_val.raw_value, type_name="Any", confidence=target_val.confidence)

            # Field on dict
            if isinstance(raw, dict) and member in raw:
                return IValue(raw_value=raw[member], type_name="Any", confidence=target_val.confidence)

            # Field on object
            if hasattr(raw, member):
                return IValue(raw_value=getattr(raw, member), type_name="Any", confidence=target_val.confidence)

            raise AttributeError(f"Member '{member}' not found on {target_val}")

        if isinstance(expr, UnaryOp):
            val = self.evaluate_expr(expr.operand, env)
            if expr.op == "-":
                return IValue(raw_value=-val.get_numeric(), type_name="Number", confidence=val.confidence)
            if expr.op == "not":
                return IValue(raw_value=not bool(val.raw_value), type_name="Bool", confidence=val.confidence)

        if isinstance(expr, BinaryOp):
            return self.evaluate_binary_op(expr, env)

        raise NotImplementedError(f"Expression {type(expr).__name__} not supported")

    def evaluate_binary_op(self, expr: BinaryOp, env: Environment) -> IValue:
        left = self.evaluate_expr(expr.left, env)
        right = self.evaluate_expr(expr.right, env)

        op = expr.op
        min_conf = min(left.confidence, right.confidence)

        # Logical operators
        if op == "and":
            res = bool(left.raw_value) and bool(right.raw_value)
            return IValue(raw_value=res, type_name="Bool", confidence=min_conf)
        if op == "or":
            res = bool(left.raw_value) or bool(right.raw_value)
            return IValue(raw_value=res, type_name="Bool", confidence=min_conf)

        # Arithmetic operators
        if op in ("+", "-", "*", "/", "%"):
            # 1. Currency arithmetic
            if left.type_name == "Currency" or right.type_name == "Currency":
                l_amt = left.get_numeric()
                r_amt = right.get_numeric()
                curr = "USD"
                if isinstance(left.raw_value, dict):
                    curr = left.raw_value.get("currency", "USD")
                elif isinstance(right.raw_value, dict):
                    curr = right.raw_value.get("currency", "USD")

                if op == "+":
                    tot = l_amt + r_amt
                elif op == "-":
                    tot = l_amt - r_amt
                elif op == "*":
                    tot = l_amt * r_amt
                elif op == "/":
                    tot = l_amt / (r_amt if r_amt != 0 else 1)
                else:
                    tot = l_amt % r_amt

                tot = round(tot, 2)
                return IValue(
                    raw_value={"amount": tot, "currency": curr, "confidence": min_conf, "formatted": f"{tot:.2f} {curr}"},
                    type_name="Currency",
                    confidence=min_conf
                )

            # 2. Quantity arithmetic
            if left.type_name == "Quantity" and right.type_name == "Quantity":
                l_dict = left.raw_value if isinstance(left.raw_value, dict) else {}
                r_dict = right.raw_value if isinstance(right.raw_value, dict) else {}
                unit = l_dict.get("unit", "units")
                l_val = l_dict.get("value", left.get_numeric())
                r_val = r_dict.get("value", right.get_numeric())

                if op == "+":
                    tot = l_val + r_val
                elif op == "-":
                    tot = l_val - r_val
                elif op == "*":
                    tot = l_val * r_val
                else:
                    tot = l_val / (r_val if r_val != 0 else 1)

                return IValue(
                    raw_value={"value": tot, "unit": unit, "formatted": f"{tot:g} {unit}", "confidence": min_conf},
                    type_name="Quantity",
                    confidence=min_conf
                )

            # 3. String concatenation
            if op == "+" and (isinstance(left.raw_value, str) or isinstance(right.raw_value, str)):
                return IValue(
                    raw_value=str(left.get_display_value()) + str(right.get_display_value()),
                    type_name="String",
                    confidence=min_conf
                )

            # 4. Numeric arithmetic
            l_num = left.get_numeric()
            r_num = right.get_numeric()
            if op == "+":
                res = l_num + r_num
            elif op == "-":
                res = l_num - r_num
            elif op == "*":
                res = l_num * r_num
            elif op == "/":
                res = l_num / r_num if r_num != 0 else 0.0
            elif op == "%":
                res = l_num % r_num if r_num != 0 else 0.0
            return IValue(raw_value=res, type_name="Number", confidence=min_conf)

        # Comparison operators
        l_val = left.raw_value
        r_val = right.raw_value

        if isinstance(l_val, dict) and "amount" in l_val:
            l_val = l_val["amount"]
        elif isinstance(l_val, dict) and "value" in l_val:
            l_val = l_val["value"]

        if isinstance(r_val, dict) and "amount" in r_val:
            r_val = r_val["amount"]
        elif isinstance(r_val, dict) and "value" in r_val:
            r_val = r_val["value"]

        if op == "==":
            return IValue(raw_value=(l_val == r_val), type_name="Bool", confidence=min_conf)
        if op == "!=":
            return IValue(raw_value=(l_val != r_val), type_name="Bool", confidence=min_conf)
        if op == "<":
            return IValue(raw_value=(l_val < r_val), type_name="Bool", confidence=min_conf)
        if op == "<=":
            return IValue(raw_value=(l_val <= r_val), type_name="Bool", confidence=min_conf)
        if op == ">":
            return IValue(raw_value=(l_val > r_val), type_name="Bool", confidence=min_conf)
        if op == ">=":
            return IValue(raw_value=(l_val >= r_val), type_name="Bool", confidence=min_conf)
        if op == "~":
            # Fuzzy / Semantic match
            similarity = SemanticEngine.levenshtein_distance(str(l_val).lower(), str(r_val).lower())
            max_len = max(len(str(l_val)), len(str(r_val)), 1)
            score = 1.0 - (similarity / max_len)
            return IValue(raw_value=(score >= 0.70), type_name="Bool", confidence=score)

        raise NotImplementedError(f"Binary operator '{op}' not supported")
