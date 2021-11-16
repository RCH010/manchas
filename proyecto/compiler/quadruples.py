'''
Quadruples class is used to save an operation
'''
class Quadruple():
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def get_quadruple(self):
        return [self.operator, self.left_operand, self.right_operand, self.result]

    def get_operator(self):
        return self.operator

    def get_left_operand(self):
        return self.left_operand

    def get_right_operand(self):
        return self.right_operand

    def get_result(self):
        return self.result

    def set_result(self, new_result):
        self.result = new_result

    def print(self):
        print('\t', self.operator, '\t', self.left_operand, '\t', self.right_operand, '\t', self.result)
