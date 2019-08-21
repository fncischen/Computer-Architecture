"""CPU functionality."""

import sys
print(sys.argv[1])
LDI = 0b10000010
PRN = 0b01000111
EXIT = 0b00000001
NOTHING = 0b00000000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

print("LDI", LDI)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.x = [0] * 25 
        # general purpose visitors
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        # self.ir = ""
        # self.mar = ""
        # self.mdr = ""
        # self.fl = []

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # these are our instructions we want to implement on this address
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        program = []

        if sys.argv[1]:
            filepath = sys.argv[1]
            with open(filepath) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()

                    if num == "":
                        continue
                    
                    x = int(num,2)
                    program.append(x)
        
            print("What our ram is now", self.ram)
        else:
            program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
            ] 

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MULT": 
            print("multiply")
            self.reg[reg_a] *= self.reg[reg_b]
            print(self.reg)
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
        return value 

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True
        sysStartingPoint = self.reg[7]
        sysStackPointer = self.reg[7]
        print("sys stack pointer", sysStackPointer)
        while running:
            command = self.ram_read(self.pc)

            operandA = self.ram_read(self.pc+1)
            operandB = self.ram_read(self.pc+2)

            # check all possible commands
            if command == LDI:
                self.reg[operandA] = operandB
                self.pc += 3
            elif command == PRN:
                print("print register value at", self.reg[operandA])
                self.pc += 2
            elif command == EXIT:
                print("exiting system!")
                sys.exit(1)
            elif command == NOTHING:
                print("Do nothing")
                self.pc += 1
            elif command == MUL:
                self.alu("MULT", operandA,operandB)
                self.pc += 3
            elif command == PUSH:
                if sysStackPointer < len(self.ram):
                    print("writing")
                    self.ram_write(sysStackPointer, operandA)
                    print(self.ram[sysStackPointer], "at", sysStackPointer)
                    sysStackPointer -= 1
                    self.pc += 2
                else:
                    print("System Stack full")
                    self.pc += 1
                print(self.ram)
            elif command == POP:
                if sysStackPointer < len(self.ram):
                    self.ram_write(sysStackPointer, 0)
                    sysStackPointer += 1
                    self.pc += 2
                else:
                    print("there is nothing else to pop")
                    self.pc += 1
                print(self.ram)


            else:
                "Go to next step"
                self.pc += 1
                pass

    
        
