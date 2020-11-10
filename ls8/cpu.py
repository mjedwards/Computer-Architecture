"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  
        self.reg = [0] * 8 
        self.pc = 0
        self.fl = 0b00000000

        self.SP = 7
        

    def load(self):
        """Load a program into memory."""
        program = []
        address = 0
        with open(sys.argv[1]) as lines:
            for line in lines:
                clean_line = line.split('#')[0].strip()
                if clean_line == '':
                    continue
                value = int(clean_line, 2)

                program.append(value)

        
                
                    
            

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 set value
        #     0b00000000, #NOP do nothing
        #     0b00001000, 
        #     0b01000111, # PRN R0 print
        #     0b00000000, #NOP do nothing
        #     0b00000001, # HLT halt
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3

        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            else:
                self.fl = 0b00000000

            self.pc += 3

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, entry):
        self.ram[address] = entry

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        NOP = 0b00000000
        MUL = 0b10100010
        ADD = 0b10100000 
        SUB = 0b10100001
        POP = 0b01000110
        PUSH = 0b01000101
        CALL = 0b01010000
        RETURN = 0b00010001
        CMP = 0b10100111
        JEQ = 0b01010101 
        JNE = 0b01010110
        JMP = 0b01010100 

        running = True
        while running:
            a = self.ram_read(self.pc)
            b = self.ram_read(self.pc + 1)
            c = self.ram_read(self.pc + 2)

            if a == HLT:
                running = False
                self.pc += 1
                sys.exit()
            
            elif a == PRN:
                print(self.reg[b])
                self.pc += 2
    
            
            elif a == LDI:
                self.reg[b] = c
                self.pc += 3

            elif a == MUL:
                self.alu("MUL", b, c)

            elif a == ADD:
                self.alu("ADD", b, c)

            elif a == SUB:
                self.alu("SUB", b, c)

            elif a == POP:
                self.reg[self.SP] -= 1
                _num = self.ram[self.pc+1]
                value = self.reg[_num]  
                location = self.reg[self.SP]
                self.ram[location] = value
                self.pc += 2

            elif a == PUSH:
                value = self.ram_read(self.reg[self.SP])
                self.reg[b] = value
                self.reg[self.SP] += 1
                self.pc += 2

            elif a == CALL:
                _return = self.pc + 2
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = _return
                _num = self.ram[self.pc + 1]
                _destination = self.reg[_num]
            
            elif a == RETURN:
                _return = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                self.pc = _return

            elif a == CMP:
                self.alu("CMP", b, c)
            elif a == JMP:
                self.pc = self.reg[b]
            elif a == JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.reg[b]
                else:
                    self.pc += 2
            elif a == JNE:
                if self.fl & 0b00000001 == 0:
                    self.pc = self.reg[b]
                else:
                    self.pc += 2

            elif a == NOP:
                pass

            else:
                print("not an instruction")
                running = False


