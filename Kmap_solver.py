import math


def print_color(in_str, color):
    print(color, in_str, "\033[0m")


def log2(x):
    if x == 0:
        return False
    return math.log10(x)/math.log10(2)


def is_square(num):
    return math.ceil(log2(num)) == math.floor(log2(num))


class KMapLoader:
    dict_map = {}
    dict_com = {}
    applied_con = []
    config = {}
    logic_groups = []
    kmap_index_dict = {}
    input_char_list = []
    no_inputs = 0

    def __init__(self, config, report_file_name):
        print("K-Map Loader")
        self.config = config
        self.no_inputs = self.config["inputs"]
        self.no_bits_rows = int(self.no_inputs / 2)
        self.no_bits_cols = self.no_inputs - self.no_bits_rows
        self.kmap_index_dict = self.gen_kmap_index(self.no_inputs)
        self.input_char_list = config["input_chars"]
        self.file = open(report_file_name, "w", encoding='utf8')

    def gen_kmap_index(self, no_inputs):
        l_header =[
            [],
            [0b0, 0b1],
            [0b00, 0b01, 0b11, 0b10],
            [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100],
            [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100, 0b1100, 0b1101, 0b1111, 0b1110, 0b1010, 0b1011, 0b1001, 0b1000],
            [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100,
                  0b1100, 0b1101, 0b1111, 0b1110, 0b1010, 0b1011, 0b1001, 0b1000,
                  0b11000, 0b11001, 0b11011, 0b11010, 0b11110, 0b11111, 0b11101, 0b11100,
                  0b10100, 0b10101, 0b10111, 0b10110, 0b10010, 0b10011, 0b10001, 0b10000]]
        no_bits_col = self.no_bits_cols
        no_bits_row = self.no_bits_rows
        print(no_bits_row, no_bits_col)

        new_row_list = l_header[no_bits_row].copy()
        new_col_list = l_header[no_bits_col].copy()

        # for n_col in range(2, no_bits_col):
        # n_col = 2
        # while n_col < no_bits_col:
        #     temp_col_list = new_col_list.copy()
        #     # print(n_col)
        #     for num in temp_col_list:
        #         num += 2 ** n_col
        #         new_col_list.append(num)
        #     n_col += 1
        #
        # n_row = 2
        # while n_row < no_bits_row:
        #     temp_row_list = new_row_list.copy()
        #     for num in temp_row_list:
        #         num += 2 ** n_row
        #         new_row_list.append(num)
        #     n_row += 1

        kmp_dict = {}
        i = 0
        for row in new_row_list:
            for col in new_col_list:
                kmp_dict[i] = row << no_bits_col | col
                print("%2d - %2d" % (i,kmp_dict[i]), "|", end='')
                i += 1
            print("")

        return kmp_dict

    def map_allocate(self):
        c = 0
        for out in self.config["wanted_outputs"]:
            w_output = self.config["wanted_outputs"][str(self.kmap_index_dict[c])]
            self.dict_map[c] = {"cell_name": self.kmap_index_dict[c], "output": w_output}
            print("out ", out, " ", c, " km ", self.kmap_index_dict[c], "output ", w_output)
            c = c + 1
        print(self.dict_map)
        no_bits_col = self.no_bits_cols
        no_bits_row = self.no_bits_rows
        c = 0
        print(no_bits_col, " ", no_bits_row)
        print("------------- K MAP ------------")
        self.file.writelines("------------- K MAP ------------\n")

        # Print Tittle
        print_tittle = 0
        print("\033[95m", end='')
        for t_col in range(2 ** no_bits_col):
            cell = self.dict_map[print_tittle]["cell_name"]
            bin_string = format(cell & (2 ** no_bits_col - 1),
                                '{fill}{width}b'.format(width=no_bits_col, fill=0))
            if t_col == 0:
                for i in range(len(self.config["input_chars"])):
                    if i != self.no_bits_rows:
                        print(self.config["input_chars"][i], end='')
                    elif i == self.no_bits_rows:
                        print('\\', self.config["input_chars"][i], end='')
                print("")
                print(bin_string.center(8), "|", end='')
                self.file.write(bin_string.center(8) + "|")
            print(bin_string.center(8), "|", end='')
            self.file.write(bin_string.center(8) + "|")
            print_tittle += 1
        print("\033[1;30;0m")
        self.file.write("\n")

        for row in range(0, 2 ** no_bits_row):
            for col in range(0, 2 ** no_bits_col):
                cell = self.dict_map[c]["cell_name"]
                if col == 0:
                    copy_cell = cell
                    bin_string = format((copy_cell >> no_bits_col) & (2 ** no_bits_row - 1),
                                        '{fill}{width}b'.format(width=no_bits_row, fill=0))
                    print("\033[95m", end='')
                    print(bin_string.center(8), "|", end='')
                    self.file.write(bin_string.center(8) + "|")
                    print("\033[0m", end='')

                cell_string = "%2d (%1d)" % (cell, self.dict_map[cell]["output"])
                # cell_string = "%2d - %2d (%1d)" % (cell, c, self.dict_map[c]["output"])
                if self.dict_map[c]["output"] == 1:
                    print("\033[92m", end='')
                    print(cell_string.center(8), "|", end='')
                    self.file.write(cell_string.center(8) + "|")
                    print("\033[0m", end='')
                else:
                    print(cell_string.center(8), "|", end='')
                    self.file.write(cell_string.center(8) + "|")
                c += 1
            print("")
            self.file.write("\n")

    def gen_index_con2(self, no_rows, no_cols, row_off, col_off, max_col, max_row):
        index_list = []
        r_row = no_rows

        row = row_off
        while r_row > 0:
            r_col = no_cols
            col = col_off
            while r_col > 0:
                # print(row * max_col + col)
                index_list.append(self.dict_map[row * max_col + col]['cell_name'])
                r_col = r_col - 1
                col = col + 1
                if col >= max_col:
                    # if self.no_inputs <= 4:
                    #     col = 0
                    # else:
                    break

            r_row = r_row - 1
            row = row + 1
            if row >= max_row:
                # if self.no_inputs <= 4:
                #     col = 0
                # else:
                break

        index_list.sort()
        return {"key": "{0}".format(index_list), "index_list": index_list}

    total_logic_groups = []

    def find_adjacent_groups(self, is_validity, o_cell, s_cell, group_len, logic_group):
        # print(is_validity)
        # Find all adjacent cells
        l_adjacent = []
        for b in range(0, self.no_inputs):
            n_cell = s_cell | 2 ** b
            if n_cell not in l_adjacent:
                l_adjacent.append(n_cell)

            n_cell = s_cell & ~(2 ** b)
            if n_cell not in l_adjacent:
                l_adjacent.append(n_cell)
        # Check for cell output and duplication
        is_validity &= s_cell
        if self.dict_map[s_cell]["output"] == 1 \
                and s_cell not in logic_group and is_validity != 0:
            # print(s_cell, end=" ")
            logic_group.append(s_cell)
            # Exit condition of the recursive calls
            if group_len == 1:
                # Check validity of the groups
                # x_result = 2**self.no_inputs-1
                # for c in logic_group:
                #     x_result &= c
                # print(logic_group, "-", x_result)
                if o_cell in l_adjacent:
                    print(logic_group, " - ", is_validity)
                    logic_group.sort()
                # if x_result != 0 and logic_group not in self.total_logic_groups:
                if logic_group not in self.total_logic_groups and o_cell in l_adjacent:
                    self.total_logic_groups.append(logic_group)
                return 1
            for cell in l_adjacent:
                if cell not in logic_group:
                    self.find_adjacent_groups(is_validity, o_cell, cell, group_len-1, logic_group.copy())
        else:
            return 0

    def find_all_groups(self):
        list_output_1 = []
        choosen_group = []
        for i in self.dict_map:
            if self.dict_map[i]["output"] == 1:
                list_output_1.append(i)
        print("-----------------------Cover cells-----------------")
        print(list_output_1)

        group_size = []
        for b in range(self.no_inputs-1, 0, -1):
            group_size.append(2**b)
        print("group_size ", group_size)
        covered_cells = []
        for cell in list_output_1:
            print("Cell: ", cell)
            if len(covered_cells) == len(list_output_1):
                print("choosen_group")
                print(choosen_group)
                self.logic_groups = choosen_group
                return choosen_group
            if cell in covered_cells:
                continue
            for group in group_size:
                logic_groups = []
                self.total_logic_groups = []
                self.find_adjacent_groups(2**self.no_inputs-1, cell, cell, group, logic_groups)
                # Choose groups which have maximum number of cell
                print(self.total_logic_groups, "group size: ", group)
                if len(self.total_logic_groups) != 0:
                    choosen_group.append(self.total_logic_groups[0])
                    print(self.total_logic_groups[0])
                    for e_cell in self.total_logic_groups[0]:
                        if e_cell not in covered_cells:
                            covered_cells.append(e_cell)
                    break

    def gen_filter(self, index, group_size):
        print("")

    def gen_possible_index(self):
        # large group
        no_inputs = self.no_inputs
        max_cols = self.no_bits_cols
        max_rows = self.no_bits_rows
        total_cols = 2 ** max_cols
        total_rows = 2 ** max_rows
        # print(max_cols, max_rows)
        c_row = max_rows
        while c_row >= 0:
            c_no_rows = 2 ** c_row
            c_col = max_cols
            while c_col >= 0:
                c_no_cols = 2 ** c_col
                # print("----", c_no_rows, c_no_cols, "----")
                for row_off in range(total_rows):
                    for col_off in range(total_cols):
                        if self.dict_map[row_off * total_cols + col_off]["output"] == 1:
                            # print((row_off * total_cols + col_off)," ",self.dict_map[row_off * total_cols + col_off])
                            com = self.gen_index_con2(c_no_rows, c_no_cols, row_off, col_off, total_cols, total_rows)
                            if is_square(len(com)):
                                self.dict_com[com["key"]] = com["index_list"]
                                l_comb_need_mirror = [com["index_list"]]
                                while len(l_comb_need_mirror) > 0:
                                    # print("l_comb_need_mirror :", l_comb_need_mirror)
                                    mirror_comb_seq = self.mirror_combs_seq(l_comb_need_mirror[0])
                                    # print(mirror_comb_seq)
                                    # print("------------mirror-seq-------------------")
                                    # print("Passing indexes: ", l_comb_need_mirror[0])
                                    del l_comb_need_mirror[0]
                                    for c in mirror_comb_seq:
                                        if c and is_square(len(c)):
                                            # print(c)
                                            self.dict_com["{0}".format(c)] = c
                                            if c not in l_comb_need_mirror:
                                                l_comb_need_mirror.append(c)

                            # # print("------------mirror-cas-------------------")
                            # mirror_comb_cas = self.mirror_combs_cas(com["index_list"])
                            # if mirror_comb_cas:
                            #     for c in mirror_comb_cas:
                            #         if c and is_square(len(c)):
                            #             # print(c)
                            #             self.dict_com["{0}".format(c)] = c
                c_col -= 1
            c_row -= 1

    def test(self):
        com = self.gen_index_con2(4, 2, 3, 4, 2**3, 2**3)
        self.dict_com[com["key"]] = com["index_list"]
        l_comb_need_mirror = [com["index_list"]]
        while len(l_comb_need_mirror) > 0:
            mirror_comb_seq = self.mirror_combs_seq(l_comb_need_mirror[0])
            # print(mirror_comb_seq)
            print("------------mirror-seq-------------------")
            print("Passing indexes: ", l_comb_need_mirror[0])
            del l_comb_need_mirror[0]
            print("l_comb_need_mirror :", l_comb_need_mirror)
            for c in mirror_comb_seq:
                if c and is_square(len(c)):
                    print(c)
                    self.dict_com["{0}".format(c)] = c
                    if c not in l_comb_need_mirror:
                        l_comb_need_mirror.append(c)

    def mirror_combs_seq(self, comb):
        if self.no_inputs <= 4:
            return
        d_mirror_combs = {}
        max_index = 2**self.no_inputs
        # 4 mirror
        mirror_index_list = []
        l_mirrors = []
        for i in range(2, self.no_inputs):
            l_mirrors.append(i)

        for mirror in l_mirrors:
            partial_index_list = []
            for num in comb:
                c_index = (num | 2**mirror)
                if c_index >= max_index or c_index in comb:
                    break
                partial_index_list.append(num)
                partial_index_list.append(c_index)
            if len(partial_index_list) > max_index:
                break
            if is_square(len(partial_index_list)):
                partial_index_list.sort()
                mirror_index_list.append(partial_index_list)
        return mirror_index_list

    def mirror_combs_cas(self, comb):
        if self.no_inputs <= 5:
            return
        max_index = 2**self.no_inputs
        # 4 mirror
        mirror_index_list = []
        l_mirrors = []
        for i in range(2, self.no_inputs):
            l_mirrors.append(i)

        comb_copy = comb.copy()
        partial_index_list = comb.copy()
        for mirror in l_mirrors:
            # print("comb len",  len(comb_copy), " ", mirror)
            for num in range(len(comb_copy)):
                c_index = comb_copy[num] | 2**mirror
                # print(c_index, end=" ")
                # if c_index >= max_index or c_index in comp_copy:
                if c_index >= max_index:
                    break
                if c_index not in comb_copy:
                    partial_index_list.append(c_index)
            # print("")
            if len(partial_index_list) > max_index:
                return mirror_index_list

            partial_index_list.sort()
            if partial_index_list not in mirror_index_list:
                mirror_index_list.append(partial_index_list.copy())
            # print(partial_index_list)
            comb_copy = partial_index_list.copy()
        # print(mirror_index_list)
        return mirror_index_list

    def dump_combs(self):
        for com in self.dict_com:
            print(com)

    def con_apply(self, index_list):
        if not is_square(len(index_list)):
            return 0
        for index in index_list:
            for e in self.dict_map:
                if self.dict_map[e]["cell_name"] == index:
                    # print(index)
                    # print(self.dict_map.get(index))
                    if self.dict_map[e]["output"] == 0:
                        return 0
        return 1

    def sort_logic(self, val):
        return len(val)

    def cal_con(self):
        # print("-------------------- BIG----------------------")
        for com in sorted(self.dict_com, key=self.sort_logic, reverse=True):
            # print(self.dict_com[com])
            if self.con_apply(self.dict_com[com]):
                self.applied_con.append(self.dict_com[com])
            self.applied_con.sort(key=self.sort_logic, reverse=True)
        # print("-------------cal_con--------------")
        # for c in self.applied_con:
        #     print(c, "size: ", len(c))

    def check_chosen_groups(self, index, chosen_groups):
        for group in chosen_groups:
            if index in group:
                return 0
        return 1

    def find_groups(self):
        # Find all the outputs 1
        chosen_groups = []
        list_output_1 = []
        for i in self.dict_map:
            if self.dict_map[i]["output"] == 1:
                list_output_1.append(self.dict_map[i]["cell_name"])
        # Apply convolution and register largest groups

        for i in list_output_1:
            if self.check_chosen_groups(i, chosen_groups) == 0:
                # print("Skip ", i)
                continue
            else:
                for li in self.applied_con:
                    if i in li:
                        chosen_groups.append(li)
                        break
                        # self.applied_con.remove(li)
        print("------------- Cover Cell ------------")
        self.file.writelines("------------- Cover Cell ------------\n")
        print(list_output_1)
        self.file.writelines(str(list_output_1) + "\n")
        print("-------------Groups--------------")
        self.file.writelines("-------------Groups--------------\n")
        num = 1
        for group in chosen_groups:
            print(num, ". ", group, "size: ", len(group))
            self.file.writelines(str(num) + ". " + str(group) + "\n")
            num += 1
        # self.file.writelines(str(chosen_groups) + "\n")

        self.logic_groups = chosen_groups

    def output_logic(self):
        logic_string = 'F = '
        is_first_group = True
        for group in self.logic_groups:
            # get logic of the first num in group
            logic_result = []
            if not is_first_group:
                logic_string += " + "
            for i in range(self.no_inputs):
                logic_result.append((group[0] & (1 << i)))
            for num in group:
                for i in range(self.no_inputs):
                    if logic_result[i] == -1:
                        continue
                    if num & (1 << i) != logic_result[i]:
                        logic_result[i] = -1
            print(logic_result)
            for i in range(len(logic_result)):
                if logic_result[len(logic_result)-1-i] == -1:
                    continue
                elif logic_result[len(logic_result)-1-i] == 0:
                    char_bar = self.input_char_list[i] + "\u0304"
                    logic_string += char_bar  # input_string_not[i]
                else:
                    logic_string += self.input_char_list[i]
            if is_first_group:
                is_first_group = False
        print("----------Logic-------------")
        self.file.writelines("----------Logic-------------\n")
        print_color(logic_string, '\033[1;0;34m')
        self.file.write(logic_string)
        self.file.close()


