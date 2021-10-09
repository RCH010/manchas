from operation import Operation
from utils import Data_types
from directories.scopes import Scopes_directory
from directories.vars import Vars

def test_operations():
    assert (Operation.getType('+', Data_types.INTEGER, Data_types.INTEGER) == Data_types.INTEGER)
    assert (Operation.getType('*', Data_types.INTEGER, Data_types.INTEGER) == Data_types.INTEGER)
    assert (Operation.getType('-', Data_types.INTEGER, Data_types.INTEGER) == Data_types.INTEGER)
    assert (Operation.getType('/', Data_types.INTEGER, Data_types.INTEGER) == Data_types.FLOAT)
    assert (Operation.getType('+', Data_types.BOOLEAN, Data_types.INTEGER) == 'Error')
    assert (Operation.getType('-', Data_types.FLOAT, Data_types.INTEGER) == Data_types.FLOAT)
    assert (Operation.getType('*', Data_types.FLOAT, Data_types.FLOAT) == Data_types.FLOAT)
    assert (Operation.getType('/', Data_types.INTEGER, Data_types.FLOAT) == Data_types.FLOAT)
    assert (Operation.getType('+', Data_types.INTEGER, Data_types.FLOAT) == Data_types.FLOAT)
    assert (Operation.getType('+', Data_types.CHARACTER, Data_types.FLOAT) == Data_types.FLOAT)
    assert (Operation.getType('+', Data_types.CHARACTER, Data_types.CHARACTER) == Data_types.INTEGER)
    assert (Operation.getType('+', Data_types.INTEGER, Data_types.CHARACTER) == Data_types.INTEGER)
    assert (Operation.getType('*', Data_types.INTEGER, Data_types.CHARACTER) == Data_types.INTEGER)
    assert (Operation.getType('-', Data_types.INTEGER, Data_types.CHARACTER) == Data_types.INTEGER)
    assert (Operation.getType('-', Data_types.CHARACTER, Data_types.CHARACTER) == Data_types.INTEGER)
    assert (Operation.getType('noOP', Data_types.INTEGER, Data_types.INTEGER) == 'Error')
    assert (Operation.getType('<', Data_types.CHARACTER, Data_types.INTEGER) == Data_types.BOOLEAN)
    assert (Operation.getType('>', Data_types.CHARACTER, Data_types.INTEGER) == Data_types.BOOLEAN)
    assert (Operation.getType('<=', Data_types.INTEGER, Data_types.INTEGER) == Data_types.BOOLEAN)
    assert (Operation.getType('>=', Data_types.INTEGER, Data_types.FLOAT) == Data_types.BOOLEAN)
    assert (Operation.getType('==', Data_types.INTEGER, Data_types.INTEGER) == Data_types.BOOLEAN)
    assert (Operation.getType('!=', Data_types.CHARACTER, Data_types.INTEGER) == Data_types.BOOLEAN)
    assert (Operation.getType('!=', Data_types.BOOLEAN, Data_types.INTEGER) == 'Error')
    assert (Operation.getType('&&', Data_types.BOOLEAN, Data_types.INTEGER) == 'Error')
    assert (Operation.getType('&&', Data_types.BOOLEAN, Data_types.BOOLEAN) == Data_types.BOOLEAN)
    assert (Operation.getType('||', Data_types.BOOLEAN, Data_types.BOOLEAN) == Data_types.BOOLEAN)
    return 'Tests types of operations were succesful!'

print(test_operations())

my_scope = Scopes_directory()
my_vars_table = Vars()
my_scope.add_new_scope('test', 'VOIDs', my_vars_table)