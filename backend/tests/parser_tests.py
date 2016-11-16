import unittest
from calculation import parser


class ParserTests(unittest.TestCase):
    
    def test_simple_parser(self):
        atoms = ['123', '3.14', 'derp', 'x', 'x2y']
        for atom in atoms:
            self.assertEqual(atom, parser.parse_string_to_tree(atom))
    
    def test_dumb_parens(self):
        atoms = ['123', '3.14', 'derp', 'x', 'x2y']
        
        for atom in atoms:
            complex = '(' + atom + ')'
            self.assertEqual([atom], parser.parse_string_to_tree(complex))

        for atom in atoms:
            complex = '((' + atom + '))'
            self.assertEqual([[atom]], parser.parse_string_to_tree(complex))
        
        # test nesting a crapload of parentheses around an expression
        # note this is a "worst case" scenario for the parser so it's also a speed test?
        for depth in range(0, 100):
            complex = '('*depth + atom + ')'*depth
            answer = atom
            for i in range(0, depth):
                answer = [answer]
            self.assertEqual(answer, parser.parse_string_to_tree(complex))
    
    def test_connectives(self):
        for connective in ['+', '*', '-', '/']:
            for x, y in [('1', '2'), ('3', '4'), ('x', 'y')]:
                to_parse = x + connective + y
                desired = [x, connective, y]
                self.assertEqual(desired, parser.parse_string_to_tree(to_parse))
    
    def test_complex(self):
        L = '1+(2*3)'
        R = '7*((8-9)+x)'
        big = '({0:s})*({1:s})'.format(L, R)
        
        self.assertEqual(
            [  # NB parse_tree does strip out the outermost layer of parens
                parser.parse_string_to_tree(L),
                '*',
                parser.parse_string_to_tree(R)
            ],
            parser.parse_string_to_tree(big)
        )
        
        self.assertEqual(
            [
                '1', '+', ['2', '*', '3']
            ],
            parser.parse_string_to_tree(L)
        )
        
        self.assertEqual(
            [
                '7',
                '*',
                [['8', '-', '9'], '+', 'x']
            ],
            parser.parse_string_to_tree(R)
        )

    def test_paren_problems(self):
        trouble = [
            'un(close(d)',
            '(dsj((kdns)())',
            'unope)ned',
            'and_ag()ain)',
            'wrong)(order',
            '((t)(b)((a)',
            '(()()((()()))()',
            '()',
            '' # empty strings are also bad
            ]
        
        for bad_input in trouble:
            with self.assertRaises(ValueError):
                parser.parse_string_to_tree(bad_input)
    

class ElevatorTests(unittest.TestCase):
    
    def test_string_atoms(self):
        # string atoms just get transformed to themselves ...
        good_atoms = [
            'x', 'y', 'fdj', 'fjdbfjkdsbfjkdnsb',
            'BNJnNBKJNBnnK', 'nabhKJHBnmn'
        ]
        
        for atom in good_atoms:
            parsed = parser.parse_string_to_tree(atom)
            ev = parser.parse_tree_to_evaluatable(parsed)
            self.assertEqual(atom, ev)
            
            self.assertEqual(
                (True, atom),
                parser.try_atom(atom)
            )
        
        trouble = [
            '1x', 'x1', '_X', 'Ymk_',
            '!', '.', '213.x'
        ]
        
        for atom in trouble:
            with self.assertRaises(ValueError):
                parser.try_atom(atom)
            
            parsed = parser.parse_string_to_tree(atom)
            with self.assertRaises(ValueError):
                parser.parse_tree_to_evaluatable(parsed)
    
    def test_spaces_are_bad(self):
        trouble = [
            'x y',
            ' ndjn dajknf afjksda',
            'nfdlj fdjlns anla    anlj  ',
            '  jfdnaf faddsfdsj   fabdjk fdsfd  ',
        ]
        for atom in trouble:
            tree = parser.parse_string_to_tree(atom)
            with self.assertRaises(ValueError):
                parser.parse_tree_to_evaluatable(tree)
        
        should_be_fine = [
            ' x',
            'y ',
            '   dnsajd\t',
        ]
        
        for atom in should_be_fine:
            tree = parser.parse_string_to_tree(atom)
            ev = parser.parse_tree_to_evaluatable(tree)
            
            self.assertEqual(
                ev,
                atom.strip()
            )
    
    def test_complex_example(self):
        # still gotta write some!
        self.assertTrue(False)
    
    def test_connectives_work(self):
        # still gotta write some tests!
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
