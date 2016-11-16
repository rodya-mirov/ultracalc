from typing import Iterable, Dict, Callable

from grammar.symbols import Nonterminal, Symbol, Terminal, SymbolList


class Rule:
    def __init__(self, lhs: Nonterminal, rhs: Iterable[Symbol]):
        self.lhs = lhs
        self.rhs = list(rhs)
    
    def lhs(self) -> Nonterminal:
        return self.lhs
    
    def rhs(self) -> Iterable[Symbol]:
        return self.rhs
    
    def __add__(self, other: 'Rule') -> Grammar:
        out = Grammar()
        out.add_rule(self)
        out.add_rule(other)
        return out


class Grammar:
    def __init__(self, rules: Dict[Nonterminal, Rule] = None):
        self.rules = dict()
        self.symbol_list = SymbolList()
        self.start = None
        if rules:
            for key in rules:
                self.rules[key] = rules[key]
    
    def set_start(self, start: Nonterminal) -> None:
        self.start = start
    
    def make_nonterminal(self) -> Nonterminal:
        return self.symbol_list.make_nonterminal()
    
    def get_terminal(self, character: str) -> Terminal:
        return self.symbol_list.get_or_make_terminal(character)
    
    def add_rule(self, rule: Rule) -> None:
        self.rules[rule.lhs] = rule.rhs
    
    def __iadd__(self, other: Rule) -> 'Grammar':
        """Add the Rule to this Grammar"""
        self.add_rule(other)
        return self
    
    def __add__(self, other: Rule) -> 'Grammar':
        """Create a new Grammar containing the other Rule"""
        out = Grammar(self.rules)
        out.add_rule(other)
        return out
    
    def __radd__(self, other: Rule) -> 'Grammar':
        return self + other
