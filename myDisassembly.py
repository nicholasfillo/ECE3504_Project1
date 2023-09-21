##########################################################################################################################################################
#   ECE 3504 - Project 1                                                                                                                                 #
#   Nicky Fillo - nickf17                                                                                                                                #
#   Version 1                                                                                                                                            #
#   Date: 09/20/2023                                                                                                                                     #
#   Purpose: The purpose of this Python script is to act as a Mips Disassembler. The program will take in a .obj file containing Mips instructions in    #
#            hex format and write the disassembled mips instrucitno to a .s file                                                                         #
##########################################################################################################################################################

#Note: In order to run this code change the input_file to the .obj file being read in and the output_file_string to the .s file that is being written to
input_file = "test_case3.obj"
output_file_string = "test_case3.s"

#clears the output file
output_file = open(output_file_string, "w")
output_file.close()

with open(input_file) as infile:
    #Dictionaries made to easily switch between binary and the actually mips instruction
    bin_dict = {'00000': '$zero', '00001': '$at', '00010': '$v0', '00011': '$v1', '00100': '$a0', '00101': '$a1', '00110': '$a2', '00111': '$a3',
                '01000': '$t0', '01001': '$t1', '01010': '$t2', '01011': '$t3', '01100': '$t4', '01101': '$t5', '01110': '$t6', '01111': '$t7',
                '10000': '$s0', '10001': '$s1', '10010': '$s2', '10011': '$s3', '10100': '$s4', '10101': '$s5', '10110': '$s6', '10111': '$s7',
                '11000': '$t8', '11001': '$t9', '11010': '$k0', '11011': '$k1', '11100': '$gp', '11101': '$sp', '11110': '$s8', '11111': '$ra'}
    rtype_dict = {'100000': 'add', '100001': 'addu', '100100': 'and', '100111': 'nor', '100101': 'or', '101010': 'stl', '101011': 'sltu', '000000': 'sll',
                '000010': 'srl', '100010': 'sub', '100011': 'subu'}
    itype_dict = {'001000': 'addi', '001001': 'addiu', '001100': 'andi', '000100': 'beq', '000101': 'bne', '100100': 'lbu', '100101': 'lhu', '110000': 'll',
                '001111': 'lui', '100011': 'lw', '001101': 'ori', '001010': 'slti', '001011': 'sltiu', '101000': 'sb', '111000': 'sc', '101001': 'sh', '101011': 'sw'}
    hex_dict = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}
    
    #PC count
    count = 4

    #These two variables are used for implementing the beq and bne insructions
    address_location_array = []
    hex_address_location_array = []

    #if write_to_file is false then the program has run into an error in which it cannot disasemble the mips instruction and will not write to the output file
    write_to_file = True

    #Read in from the .obj file
    for hex_data in infile:
        binary_data = ''

        #Convert Hex Data to Binary Data
        for hex_digit in hex_data[0:8]:
            binary_data += hex_dict[hex_digit]

        #This if statement checks if there is an error and prints an error message corresponding to the hex instruction as well as the line number
        if (itype_dict.get(binary_data[0:6]) == None and binary_data[0:6] != '000000') or (rtype_dict.get(binary_data[26:32]) == None and binary_data[0:6] == '000000') or (binary_data.__len__() != 32):
            print("ERROR: Cannot Disassemble " + hex_data.rstrip("\n") + " at line " + str(int(count/4)))
            write_to_file = False
        else:
            #R type
            if binary_data[0:6] == '000000':
                #Not a shift
                if binary_data[21:26] == '00000':
                    mips_instruction = ("    " + rtype_dict[binary_data[26:32]] + " " + bin_dict[binary_data[16:21]] + ", " + bin_dict[binary_data[6:11]] + ", " + bin_dict[binary_data[11:16]])
                    output_file = open(output_file_string, "a")
                    output_file.write(mips_instruction + "\n")
                    output_file.close()
                #Is a shift
                else:
                    mips_instruction = ("    " + rtype_dict[binary_data[26:32]] + " " + bin_dict[binary_data[16:21]] + ", " + bin_dict[binary_data[11:16]] + ", " + str(int(binary_data[21:26], 2)))
                    output_file = open(output_file_string, "a")
                    output_file.write(mips_instruction + "\n")
                    output_file.close()
            #I type
            else:
                #Load or Store Instruction (signed)
                if itype_dict[binary_data[0:6]] == 'lw' or itype_dict[binary_data[0:6]] == 'sw' or itype_dict[binary_data[0:6]] == 'sb' or itype_dict[binary_data[0:6]] == 'sh' or itype_dict[binary_data[0:6]] == 'sc' or itype_dict[binary_data[0:6]] == 'll':
                    #The immediate values are signed so it is necessary to check the most signifigant bit of the immediate value
                    if binary_data[16] == '0':
                        mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[11:16]] + ", " + str(int(binary_data[16:32], 2)) + "(" + bin_dict[binary_data[6:11]] + ")")
                        output_file = open(output_file_string, "a")
                        output_file.write(mips_instruction + "\n")
                        output_file.close()
                    elif binary_data[16] == '1':
                        ones_complement = ''.join('1' if bit == '0' else '0' for bit in binary_data[16:32])
                        twos_complement_decimal = int(ones_complement, 2) + 1 
                        mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[11:16]] + ", -" + str(int(binary_data[16:32], 2)) + "(" + bin_dict[binary_data[6:11]] + ")")
                        output_file = open(output_file_string, "a")
                        output_file.write(mips_instruction + "\n")
                        output_file.close()
                #load instructions (unsigned)
                elif itype_dict[binary_data[0:6]] == 'lbu' or itype_dict[binary_data[0:6]] == 'lhu':
                    mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[11:16]] + ", " + str(int(binary_data[16:32], 2)) + "(" + bin_dict[binary_data[6:11]] + ")")
                    output_file = open(output_file_string, "a")
                    output_file.write(mips_instruction + "\n")
                    output_file.close()
                #BEQ or BNE instructon
                elif itype_dict[binary_data[0:6]] == 'beq' or itype_dict[binary_data[0:6]] == 'bne':
                    if binary_data[16] == '0':
                        branch = int(binary_data[16:32], 2) * 4
                        branch = branch + count
                        address_location_array.append(int(branch/4))
                        hex_branch = hex(branch)
                        if len(hex_branch) == 3:
                            address = str("Addr_000" + hex_branch[2:])
                        elif len(hex_branch) == 4:
                            address = str("Addr_00" + hex_branch[2:])
                        elif len(hex_branch) == 5:
                            address = str("Addr_0" + hex_branch[2:])
                        elif len(hex_branch) == 6:
                            address = str("Addr_" + hex_branch[2:])

                        #Store the address in an array
                        hex_address_location_array.append(address + ':\n')
                        mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[6:11]] + ", " + bin_dict[binary_data[11:16]] + ", " + address)
                        output_file = open(output_file_string, "a")
                        output_file.write(mips_instruction + "\n")
                        output_file.close()
                    elif binary_data[16] == '1':
                        ones_complement = ''.join('1' if bit == '0' else '0' for bit in binary_data[16:32])
                        ones_complement_decimal = int(ones_complement, 2) + 1 
                        ones_complement_decimal *= -4
                        twos_complement = ones_complement_decimal + count
                        address_location_array.append(int(twos_complement/4))
                        twos_complement_hex = hex(twos_complement)
                        if len(twos_complement_hex) == 3:
                            address = str("Addr_000" + twos_complement_hex[2:])
                        if len(twos_complement_hex) == 4:
                            address = str("Addr_00" + twos_complement_hex[2:])
                        elif len(hex_branch) == 5:
                            address = str("Addr_0" + twos_complement_hex[2:])
                        elif len(hex_branch) == 6:
                            address = str("Addr_" + twos_complement_hex[2:])
                        hex_address_location_array.append(address + ':\n')
                        mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[6:11]] + ", " + bin_dict[binary_data[11:16]] + ", " + address)
                        output_file = open(output_file_string, "a")
                        output_file.write(mips_instruction + "\n")
                        output_file.close()
                #LUI instruction
                elif itype_dict[binary_data[0:6]] == 'lui':
                    mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + str(int(binary_data[16:32], 2))) 
                    output_file = open(output_file_string, "a")
                    output_file.write(mips_instruction + "\n")
                    output_file.close()
                elif (itype_dict[binary_data[0:6]] == 'addi' or itype_dict[binary_data[0:6]] == 'slti') and binary_data[16] == '1':
                    ones_complement = ''.join('1' if bit == '0' else '0' for bit in binary_data[16:32])
                    twos_complement_decimal = int(ones_complement, 2) + 1 
                    mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[6:11]] + ", " + bin_dict[binary_data[11:16]] + ", -" + str(twos_complement_decimal))
                    output_file = open(output_file_string, "a")
                    output_file.write(mips_instruction + "\n")
                    output_file.close()
                else:
                    mips_instruction = ("    " + itype_dict[binary_data[0:6]] + " " + bin_dict[binary_data[11:16]] + ", " + bin_dict[binary_data[6:11]] + ", " + str(int(binary_data[16:32], 2)))
                    output_file = open(output_file_string, "a")
                    output_file.write(mips_instruction + "\n")
                    output_file.close()
        count += 4

#sort and reverse both arrays so that the largest value is first
unique_address_location_array = list(set(address_location_array))
unique_address_location_array.sort()
unique_address_location_array.reverse()

unique_hex_address_location_array = list(set(hex_address_location_array))
unique_hex_address_location_array.sort()
unique_hex_address_location_array.reverse()

#read all contents of the output file and store in an array
outfile_arr = open(output_file_string, 'r')
lines = outfile_arr.readlines()
outfile_arr.close()

#Add in the Addr_xxxx of the BEQ or BNE instructons into the array
address_count = 0
for i in unique_address_location_array:
    lines.insert(i, unique_hex_address_location_array[address_count])
    address_count += 1

#Using the array, write to the output file with the newly added Addr_xxx of the BEQ or BNE instruction
output_file = open(output_file_string, 'w')
output_file.writelines(lines)
output_file.close()

#If there was an error that occured, clear the output file
if write_to_file == False:
    output_file = open(output_file_string, "w")
    output_file.close()