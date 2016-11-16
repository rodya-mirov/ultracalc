from typing import Iterable, Dict, Callable, List

from grammar.symbols import Nonterminal, Symbol, Terminal, SymbolList


class Rule:
    def __init__(self, lhs: Nonterminal, rhs: Iterable[Symbol], fn: Callable):
        self.lhs = lhs
        self.rhs = list(rhs)
        self.fn = fn
    
    def get_fn(self) -> Callable:
        return self.fn
    
    def get_lhs(self) -> Nonterminal:
        return self.lhs
    
    def get_rhs(self) -> Iterable[Symbol]:
        return self.rhs
    
    def __add__(self, other: 'Rule') -> Grammar:
        out = Grammar()
        out.add_rule(self)
        out.add_rule(other)
        return out


class Grammar:
    def __init__(self, rules: Dict[Nonterminal, List[Rule]] = None):
        self.rules = dict()
        self.symbol_list = SymbolList()
        self.start = None
        if rules:
            for key in rules:
                self.rules[key] = [rule for rule in rules[key]]
    
    def set_start(self, start: Nonterminal) -> None:
        self.start = start
    
    def make_nonterminal(self) -> Nonterminal:
        return self.symbol_list.make_nonterminal()
    
    def get_terminal(self, character: str) -> Terminal:
        return self.symbol_list.get_or_make_terminal(character)
    
    def add_rule(self, rule: Rule) -> None:
        lhs = rule.get_lhs()
        if lhs not in self.rules:
            self.rules[lhs] = []
        
        self.rules[lhs].add(rule)
    
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
    
    def is_connected(self) -> (bool, Iterable[Rule]):
        """
        Determines if all of its rules can possibly be applied, on some string, somewhere.
        It is possible that a grammar could be logically "connected" but some rules never apply,
        for whatever reason; but if is_connected is False, you're definitely missing something.
        :return: (success, missed_rules) where success is a bool (true if connected, false if not)
        and where missed_rules is the collection of all rules which are NOT accessible.
        """
        needed = set(self.rules.keys())
        processed = set()
        to_process = [self.start]
        while to_process:
            processing = to_process.pop()
            
            # we checked this before adding, but it's still possible for it to slip through
            # if (e.g.) it's added twice before it's processed the first time
            if processing in processed:
                continue
            
            processed.add(processing)
            
            for rule in self.rules[processing]:
                for symbol in rule.get_rhs():
                    if symbol in needed:
                        to_process.append(symbol)
        
        leftover_keys = needed.difference(processed)
        if leftover_keys:
            unused_rules = []
            for key in leftover_keys:
                unused_rules.extend(self.rules[key])
            return False, unused_rules
        else:
            return True, list()
