from _thread import RLock
from typing import Iterable


class Symbol:
    def is_terminal(self) -> bool:
        raise NotImplementedError()


class Nonterminal(Symbol):
    def is_terminal(self) -> bool:
        return False


class Terminal(Symbol):
    def __init__(self, character: str) -> None:
        super().__init__()
        
        self.character = character
    
    def is_terminal(self) -> bool:
        return True
    
    def __str__(self) -> str:
        return self.character


class SymbolList:
    def __init__(self):
        self.terminals = dict()
        self.terminals_lock = RLock()
        self.nonterminals = set()
    
    def make_nonterminal(self) -> Nonterminal:
        out = Nonterminal()
        self.nonterminals.add(out)
        return out
    
    def get_or_make_terminal(self, character: str) -> Terminal:
        if len(character) != 1:
            raise ValueError("Terminals must have a string representation of length 1")
        
        out = self.terminals.get(character, None)
        if out:
            return out
        else:
            return self.make_terminal(character)
    
    def make_terminal(self, character: str) -> Terminal:
        """
        Constructs a new Terminal with specified character. The process fails if a Terminal was already registered with
        the supplied character, or if the supplied character does not have length exactly one (that is, it should be a
        character, not just a string). Also registers the new Terminal internally, indexed by the character.
        
        :param character: The character to represent the new Terminal symbol.
        :return: terminal -- the new Terminal created, or None if the creation failed.
        """
        if len(character) != 1:
            raise ValueError("Terminals must have a string representation of length 1")

        self.terminals_lock.acquire(True)
        if character in self.terminals:
            t = None
        else:
            t = Terminal(character)
            self.terminals[character] = t
        self.terminals_lock.release()
        return t
    
    def __getitem__(self, item: str) -> Terminal:
        return self.terminals[item]
    
    def __contains__(self, item: str) -> bool:
        return item in self.terminals

