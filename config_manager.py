import json


class ConfigManager:
    config_dict = {}
    x_cases = []

    def __init__(self, filename):
        print("ConfigGenerator")
        # self.load_config(filename)

    def generate(self, no_inputs, file_name):
        dict_cases = {}
        char_list = []
        char = 'A'
        for i in range(no_inputs):
            char_list.append(char)
            char = chr(ord(char) + 1)

        for i in range(2 ** no_inputs):
            # bin_string = "{0:b}".format(i)
            # bin_string = format(i, '{fill}{width}b'.format(width=no_inputs, fill=0))
            dict_cases[i] = 0
        json_obj = {"inputs": no_inputs, "input_chars": char_list, "wanted_outputs": dict_cases}
        # print(json.dumps(json_obj))
        # save configure file
        with open(file_name, 'w') as json_file:
            json.dump(json_obj, json_file, indent=4, sort_keys=True)

    def load_config(self, filename):
        try:
            with open(filename) as f:
                self.config_dict = json.load(f)
                print(self.config_dict)
        except OSError:
            print("Cannot read config file")

    def parse_num_logic(self, filename, output_filename):
        try:
            with open(filename) as f:
                config = json.load(f)
                print(self.config_dict)
        except OSError:
            print("Cannot read config file")
        # Generate dic cases
        dict_cases = {}
        no_inputs = config["inputs"]
        for i in range(2 ** no_inputs):
            # bin_string = format(i, '{fill}{width}b'.format(width=no_inputs, fill=0))
            if i in config["cases"]:
                dict_cases[i] = 1
            else:
                dict_cases[i] = 0
        # Generate Char list
        char_list = []
        char = 'A'
        for i in range(no_inputs):
            char_list.append(char)
            char = chr(ord(char) + 1)
        json_obj = {"inputs": no_inputs, "input_chars": char_list, "wanted_outputs": dict_cases}
        # print(json.dumps(json_obj))
        # save configure file
        save_filename = output_filename + "_{0}_conversed.json".format(no_inputs)
        with open(save_filename, 'w') as json_file:
            json.dump(json_obj, json_file, indent=4, sort_keys=True)

    def parse_x_logic(self, filename, output_filename):
        try:
            with open(filename) as f:
                config_x_logic = json.load(f)
                print(self.config_dict)
        except OSError:
            print("Cannot read config file")
        # Generate dic cases
        dict_cases = {}
        no_inputs = config_x_logic["inputs"]
        for i in range(2 ** no_inputs):
            bin_string = format(i, '{fill}{width}b'.format(width=no_inputs, fill=0))
            dict_cases[bin_string] = 0
        # Generate x logic cases
        for i in range(len(config_x_logic["logic"])):
            case = config_x_logic["logic"][i]
            converse_case = []
            self.find_bit_combination(case, '', 0, converse_case)
            print("------------", i, "------------")
            print(case)
            for com in converse_case:
                print(com, ":", config_x_logic["output"][i])
                dict_cases[com] = config_x_logic["output"][i]

        # Generate Char list
        char_list = []
        char = 'A'
        for i in range(no_inputs):
            char_list.append(char)
            char = chr(ord(char) + 1)
        # Hot fix convert bin to num
        d_num_cases = {}
        i = 0
        for case in dict_cases:
            d_num_cases[i] = dict_cases[case]
            i += 1
        json_obj = {"inputs": no_inputs, "input_chars": char_list, "wanted_outputs": d_num_cases}
        # print(json.dumps(json_obj))
        # save configure file
        save_filename = output_filename+"_{0}_conversed.json".format(no_inputs)
        with open(save_filename, 'w') as json_file:
            json.dump(json_obj, json_file, indent=4, sort_keys=True)

    def find_bit_combination(self, case, c_string, index, result):
        if len(case) == index:
            # print(c_string)
            result.append(c_string)
            return
        ch = case[index]
        # print(ch)
        if ch == '1':
            c_string += '1'
            self.find_bit_combination(case, c_string, index + 1, result)
        elif ch == '0':
            c_string += '0'
            self.find_bit_combination(case, c_string, index + 1, result)
        else:
            c_string += "1"
            self.find_bit_combination(case, c_string, index + 1, result)
            c_string = c_string[:-1]

            c_string += "0"
            self.find_bit_combination(case, c_string, index + 1, result)

    def get_config(self):
        return self.config_dict
