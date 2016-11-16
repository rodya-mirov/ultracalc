import string
from typing import Union, Iterable

from grammar.grammar import Grammar, Rule
from grammar.symbols import Nonterminal, Terminal

grammar = Grammar


def make_nonterminals(n: int) -> Union[Nonterminal, Iterable[Nonterminal]]:
    if n == 1:
        return grammar.make_nonterminal()
    else:
        return (grammar.make_nonterminal() for _ in range(0, n))


def make_or_get_terminals(*args: Iterable[str]) -> Union[Terminal, Iterable[Terminal]]:
    if len(args) == 1:
        return grammar.get_or_make_terminal(args[0])
    else:
        return (grammar.get_or_make_terminal(a) for a in args)


Start = make_nonterminals(1)
FullExpr, MultExpr, AddExpr, BottomExpr = make_nonterminals(3)
AddInfixFn, MultInfixFn = make_nonterminals(2)
MultUnaryFn = make_nonterminals(1)
Number, Variable = make_nonterminals(2)
Int, Float = make_nonterminals(2)
Digit = make_nonterminals(1)

L_Paren, R_Paren = make_or_get_terminals('(', ')')
Plus, Minus = make_or_get_terminals('+', '-')
Times, Divide = make_or_get_terminals('*', '/')
Period, Comma = make_or_get_terminals('.', ',')

grammar.set_start(FullExpr)

# Full Expressions moving downward in priority ...
grammar += Rule(FullExpr, [AddExpr])

# Additive Expression are made up of sums/differences of multiplicative expressions
# Note this guarantees unique readability: 1+2+3 must be read as (1+2)+3
grammar += Rule(AddExpr, [AddExpr, AddInfixFn, MultExpr])
grammar += Rule(AddExpr, [MultExpr])

# Multiplicative Expressions are made up of products/quotients of "bottom expressions"
# Again note unique readability, so 1/2/3 is (1/2)/3 (which is probably intended)
grammar += Rule(MultExpr, [MultExpr, MultInfixFn, BottomExpr])
grammar += Rule(MultUnaryFn, [BottomExpr])
grammar += Rule(MultExpr, [BottomExpr])

# Bottom expressions must be something simple - either a number, a variable, or
# contained in a parentheses pair
grammar += Rule(BottomExpr, [L_Paren, FullExpr, R_Paren])
grammar += Rule(BottomExpr, [Number])
grammar += Rule(BottomExpr, [Variable])

# Finally just define the various connectives
grammar += Rule(MultUnaryFn, [Minus])
grammar += Rule(MultInfixFn, [Times])
grammar += Rule(MultInfixFn, [Divide])
grammar += Rule(AddInfixFn, [Plus])
grammar += Rule(AddInfixFn, [Minus])

# This is how we build up numbers:
grammar += Rule(Number, [Int])
grammar += Rule(Number, [Float])

grammar += Rule(Int, [Digit])
grammar += Rule(Int, [Int, Digit])

grammar += Rule(Float, [Int, Period, Int])

# and of course we need to say what a digit is
for digit in string.digits:
    digit_terminal = grammar.get_terminal(digit)
    grammar += Rule(Digit, [digit_terminal])

# variables are just lowercase letters
for letter in string.ascii_lowercase:
    letter_terminal = grammar.get_terminal(letter)
    grammar += Rule(Variable, [letter_terminal])
