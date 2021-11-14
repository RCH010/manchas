import sys
from utils import Relation_operators, Data_types
class Operation:
    
    def getType(symbol, type1, type2):
        # print('checking', symbol, type1, type2)
        sum_times_minus = [Relation_operators.SUM, Relation_operators.MINUS, Relation_operators.TIMES]
        comparisson_operators = [
            Relation_operators.LESSTHAN,
            Relation_operators.LESSEQUALTHAN,
            Relation_operators.GREATERTHAN,
            Relation_operators.GREATEREQUALTHAN,
            Relation_operators.EQUAL,
            Relation_operators.DIFFERENT,
        ]
        if(symbol == Relation_operators.EQUALS):
            return type1 == type2

        # int-int
        if(type1 == Data_types['INTEGER'] and type2 == Data_types['INTEGER']):
            if(symbol == Relation_operators.DIVISION):
                return Data_types['FLOAT']
            elif(symbol in sum_times_minus):
                return Data_types['INTEGER']
            elif(symbol in comparisson_operators):
                return Data_types['BOOLEAN']
            else:
                print('1- Invalid operation', type1, symbol, type2)
                sys.exit()
        # int - float || floar - int || float - float
        if((type1 == Data_types['INTEGER'] or type1 == Data_types['FLOAT']) 
            and (type2 == Data_types['INTEGER'] or type2 == Data_types['FLOAT'])):
            if(symbol in sum_times_minus or symbol == Relation_operators.DIVISION):
                return Data_types['FLOAT']
            elif(symbol in comparisson_operators):
                return Data_types['BOOLEAN']
            else:
                print('2 - Invalid operation', type1, symbol, type2)
                sys.exit()
        # Check if we want to chars to be added or smth like that
        # int - int would reach this case
        # int - char || char - int || char - char
        if((type1 == Data_types['CHARACTER'] or type1 == Data_types['INTEGER']) 
            and (type2 == Data_types['CHARACTER'] or type2 == Data_types['INTEGER'])):
            if(symbol in sum_times_minus):
                return Data_types['INTEGER']
            elif(symbol == Relation_operators.DIVISION):
                return Data_types['FLOAT']
            elif(symbol in comparisson_operators):
                return Data_types['BOOLEAN']
            else:
                print('3 - Invalid operation', type1, symbol, type2)
                sys.exit()

        # float - char || char - float
        if((type1 == Data_types['CHARACTER'] or type1 == Data_types['FLOAT']) 
            and (type2 == Data_types['CHARACTER'] or type2 == Data_types['FLOAT'])):
            if(symbol in sum_times_minus or symbol == Relation_operators.DIVISION):
                return Data_types['FLOAT']
            elif(symbol in comparisson_operators):
                return Data_types['BOOLEAN']
            else:
                print('4 - Invalid operation', type1, symbol, type2)
                sys.exit()
        # bool-bool
        if(type1 == Data_types['BOOLEAN'] and type2 == Data_types['BOOLEAN']):
            if(symbol == Relation_operators.AND or 
                symbol == Relation_operators.OR or 
                symbol in comparisson_operators):
                return Data_types['BOOLEAN']
            else:
                print('5 - Invalid operation', type1, symbol, type2)
                sys.exit()
        # any other is an invalid combination
        print('6 - Invalid operation', type1, symbol, type2)
        sys.exit()

