import config_manager


# Find similar setting of bits
def find_sim_bits(nbits):
    l_case_o1 = []
    for case in config["wanted_outputs"]:
        if config["wanted_outputs"][case] == 1:
            l_case_o1.append(case)
    print(l_case_o1)

    obj = l_case_o1[0]
    for i in range(0, len(obj)):
        counter = 0
        for case in l_case_o1[1:]:
            if obj[i] == case[i]:
                counter += 1
                print(case)
        print(i, "| ", obj[i], " : ", counter)


config = config_manager.ConfigManager("config_file_4_conversed.json").get_config()
find_sim_bits(config["inputs"])

