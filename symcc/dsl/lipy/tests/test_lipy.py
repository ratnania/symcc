from os.path import join, dirname
from textx.metamodel import metamodel_from_str
from textx.export import metamodel_export, model_export

f = open("../grammar.tx")
grammar = f.read().replace("\n", "")
f.close()

# Global variable namespace
namespace = {}

mm = metamodel_from_str(grammar)

def test_for_1():

    input_expr = '''
    for i=1,5 do
    end
    '''

    model = mm.model_from_str(input_expr)
    return model

if __name__ == '__main__':
    test_for_1()
