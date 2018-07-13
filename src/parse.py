import math
import os.path


def missing_numbers(num_list):
    original_list = [x for x in range(num_list[0], num_list[-1] + 1)]
    num_list = set(num_list)
    return (list(num_list ^ set(original_list)))


class Parse(object):
    # == Parameters == #
    N_MUX = 1		# number of selection lines for the mux per io
    N_IO = 0
    N_MUX_IO = 0
    Addressing = 'WORD'
    ADDR_WIDTH = 32
    DATA_WIDTH = 32
    # ================ #

    # Generating the number of bits for memory map #
    lower_offset = 0
    if Addressing == 'BYTE':
        lower_offset = 0
    elif Addressing == 'HWORD':
        lower_offset = 1
    elif Addressing == 'WORD':
        lower_offset = 2
    elif Addressing == 'DWORD':
        lower_offset = 3
    else:
        print('ERROR: Addressing should be one of: BYTE, HWORD, WORD, DWORD')
        exit(1)

    def __init__(self, pth=None, verify=True):

        max_io = 0
        self.muxed_cells = []
        self.dedicated_cells = []
        self.pinnumbers = []

        # == capture the number of IO cells required == #
        fname = 'pinmap.txt'
        if pth:
            fname = os.path.join(pth, fname)
        with open(fname) as pinmapfile:
            for lineno, line in enumerate(pinmapfile):
                line1 = line[:-1].split('\t')
                if len(line1) <= 1:
                    continue
                self.pinnumbers.append(int(line1[0]))
                if len(line1) == 2:  # dedicated
                    self.dedicated_cells.append(line1)
                else:
                    self.muxed_cells.append(line1)

        self.pinnumbers = sorted(self.pinnumbers)
        self.upper_offset = self.lower_offset + \
            int(math.log(len(self.muxed_cells), 2))

        if verify:
            self.do_checks()

        self.cell_bitwidth = self.get_cell_bit_width()

        # == user info after parsing ================= #
        self.N_IO = len(self.dedicated_cells) + len(self.muxed_cells)
        print("Max number of IO: " + str(self.N_IO))
        print("Muxer bit width: " + str(self.cell_bitwidth))
        print("Muxed IOs: " + str(len(self.muxed_cells)))
        print("Dedicated IOs: " + str(len(self.dedicated_cells)))

    def do_checks(self):
        """ Multiple checks to see if the user has not screwed up
        """
        missing_pins = missing_numbers(self.pinnumbers)

        # Check-1: ensure no pin is present in both muxed and dedicated pins
        for muxcell in self.muxed_cells:
            for dedcel in self.dedicated_cells:
                if dedcel[1] in muxcell:
                    print("ERROR: " + str(dedcel[1]) + " present \
                                          in dedicated & muxed lists")
                    exit(1)

        # Check-2: if pin numbering is consistent:
        if missing_pins:
            print("ERROR: Following pins have no assignment: " +
                  str(missing_numbers(self.pinnumbers)))
            exit(1)
        unique = set(self.pinnumbers)
        duplicate = False
        for each in unique:
            count = self.pinnumbers.count(each)
            if count > 1:
                print("ERROR: Multiple assignment for pin: " + str(each))
                duplicate = True
        if duplicate:
            exit(1)

        # Check-3: confirm if N_* matches the instances in the pinmap
        # ============================================================== #

        # TODO

    def get_cell_bit_width(self):
        max_num_cells = 0
        for cell in self.muxed_cells:
            max_num_cells = max(len(cell) - 1, max_num_cells)
        return int(math.log(max_num_cells + 1, 2))


if __name__ == '__main__':
    p = Parse()
    print (p.N_IO)
