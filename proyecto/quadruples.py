'''
Quadruples class is used to save an operation
'''
class Quadruple():
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def getQuadruple(self):
        return [self.operator, self.left_operand, self.right_operand, self.result]

    def getOperator(self):
        return self.operator

    def getLeftOperand(self):
        return self.left_operand

    def getRightOperand(self):
        return self.right_operand

    def getResult(self):
        return self.result

    def print(self):
        print('\t', self.operator, '\t', self.left_operand, '\t', self.right_operand, '\t', self.result)
