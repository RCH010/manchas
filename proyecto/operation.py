from utils import Relation_operators, Data_types

class Operation:
    
    def getType(symbol, type1, type2):
        sum_times_minus = [Relation_operators.SUM, Relation_operators.MINUS, Relation_operators.TIMES]
        comparisson_operators = [
            Relation_operators.LESSTHAN,
            Relation_operators.LESSEQUALTHAN,
            Relation_operators.GREATERTHAN,
            Relation_operators.GREATEREQUALTHAN,
            Relation_operators.EQUAL,
            Relation_operators.DIFFERENT,
        ]
        # int-int
        if(type1 == Data_types.INTEGER and type2 == Data_types.INTEGER):
            if(symbol == Relation_operators.DIVISION):
                return Data_types.FLOAT
            elif(symbol in sum_times_minus):
                return Data_types.INTEGER
            elif(symbol in comparisson_operators):
                return Data_types.BOOLEAN
            else:
                return 'Error'
        # int - float || floar - int || float - float
        if((type1 == Data_types.INTEGER or type1 == Data_types.FLOAT) 
            and (type2 == Data_types.INTEGER or type2 == Data_types.FLOAT)):
            if(symbol in sum_times_minus or symbol == Relation_operators.DIVISION):
                return Data_types.FLOAT
            elif(symbol in comparisson_operators):
                return Data_types.BOOLEAN
            else:
                return 'Error'
        # Check if we want to chars to be added or smth like that
        # int - int would reach this case
        # int - char || char - int || char - char
        if((type1 == Data_types.CHARACTER or type1 == Data_types.INTEGER) 
            and (type2 == Data_types.CHARACTER or type2 == Data_types.INTEGER)):
            if(symbol in sum_times_minus):
                return Data_types.INTEGER
            elif(symbol == Relation_operators.DIVISION):
                return Data_types.FLOAT
            elif(symbol in comparisson_operators):
                return Data_types.BOOLEAN
            else:
                return 'Error'

        # float - char || char - float
        if((type1 == Data_types.CHARACTER or type1 == Data_types.FLOAT) 
            and (type2 == Data_types.CHARACTER or type2 == Data_types.FLOAT)):
            if(symbol in sum_times_minus or symbol == Relation_operators.DIVISION):
                return Data_types.FLOAT
            elif(symbol in comparisson_operators):
                return Data_types.BOOLEAN
            else:
                return 'Error'
        # bool-bool
        if(type1 == Data_types.BOOLEAN and type2 == Data_types.BOOLEAN):
            if(symbol == Relation_operators.AND or symbol == Relation_operators.OR):
                return Data_types.BOOLEAN
            else:
                return 'Error'
        # any other is an invalid combination
        return 'Error'

