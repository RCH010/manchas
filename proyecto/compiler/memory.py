
'''
Memory address explanation:

global starts with      --> 1
local starts with       --> 2
temporals starts with   --> 3
constants starts with   --> 4

-Decenas de millar-
all int's are           --> 1
all float's are         --> 2
all char's are          --> 3
all bool's are          --> 4
'''
from compiler.utils import Data_types


class Memory():
    count_global_int = 110000
    count_global_float = 120000
    count_global_char = 130000
    count_global_bool = 140000

    count_local_int = 210000
    count_local_float = 220000
    count_local_char = 230000
    count_local_bool = 240000

    count_temp_int = 310000
    count_temp_float = 320000
    count_temp_char = 330000
    count_temp_bool = 340000

    count_const_int = 410000
    count_const_float = 420000
    count_const_char = 430000
    count_const_bool = 440000 #TODO preguntar a elda si deberia aqui ser diferente
    #                               ya que solo puede ser true o false
    
    def update_counter(self, counter_type, type, space_to_save = 1):
        print(space_to_save)
        if counter_type == 'global':
            if type == Data_types['INTEGER']:
                self.count_global_int = self.count_global_int + space_to_save
            elif type == Data_types['FLOAT']:
                self.count_global_float = self.count_global_float + space_to_save
            elif type == Data_types['CHARACTER']:
                self.count_global_char = self.count_global_char + space_to_save
            elif type == Data_types['BOOLEAN']:
                self.count_global_bool = self.count_global_bool + space_to_save
        elif counter_type == 'local':
            if type == Data_types['INTEGER']:
                self.count_local_int = self.count_local_int + space_to_save
            elif type == Data_types['FLOAT']:
                self.count_local_float = self.count_local_float + space_to_save
            elif type == Data_types['CHARACTER']:
                self.count_local_char = self.count_local_char + space_to_save
            elif type == Data_types['BOOLEAN']:
                self.count_local_bool = self.count_local_bool + space_to_save
        elif counter_type == 'temp':
            if type == Data_types['INTEGER']:
                self.count_temp_int = self.count_temp_int + space_to_save
            elif type == Data_types['FLOAT']:
                self.count_temp_float = self.count_temp_float + space_to_save
            elif type == Data_types['CHARACTER']:
                self.count_temp_char = self.count_temp_char + space_to_save
            elif type == Data_types['BOOLEAN']:
                self.count_temp_bool = self.count_temp_bool + space_to_save
        elif counter_type == 'const':
            if type == Data_types['INTEGER']:
                self.count_const_int = self.count_const_int + space_to_save
            elif type == Data_types['FLOAT']:
                self.count_const_float = self.count_const_float + space_to_save
            elif type == Data_types['CHARACTER']:
                self.count_const_char = self.count_const_char + space_to_save
            elif type == Data_types['BOOLEAN']:
                self.count_const_bool = self.count_const_bool + space_to_save
            
    def reset_local_counters(self):
        self.count_local_int = 210000
        self.count_local_float = 220000
        self.count_local_char = 230000
        self.count_local_bool = 240000
        
    def reset_temp_counters(self):
        self.count_temp_int = 310000
        self.count_temp_float = 320000
        self.count_temp_char = 330000
        self.count_temp_bool = 340000

