import config_manager
from Kmap_solver import *
# Main program here


DEBUG = False

test = config_manager.ConfigManager("config_file_5_conversed.json")
# test.parse_num_logic("num_config.json", "config_file_num")
if DEBUG:
    test.generate(5, "config_file_5.json")
else:
    test.load_config("G0_9_conversed.json")
    # test.load_config("config_file_num_7_conversed.json")
    km = KMapLoader(test.get_config(), "G0_9.txt")
    km.map_allocate()
    # km.test()
    km.gen_possible_index()
    # km.dump_combs()
    km.cal_con()
    km.find_groups()
    km.output_logic()

    # logic_group = []
    # km.find_adjacent_groups(2**km.no_inputs-1, 1, 1, 8, logic_group)
    # print(km.total_logic_groups)
    # km.find_all_groups()
    # km.output_logic()

# print(is_square(16))

