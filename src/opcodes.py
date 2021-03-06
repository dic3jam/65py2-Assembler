'''
6502 Opcodes

Organizes the opcodes for 6502 processors into dictionaries
based upon addressing mode.

Places those dictionaries into the list "opcodes"
'''

# Indirect X
# V2
indx = {
    "adc": 0x61,
    "and": 0x21,
    "cmp": 0xc1,
    "eor": 0x41,
    "lda": 0xa1,
    "ora": 0x01,
    "sbc": 0xe1,
    "sta": 0x81
    }

# Indirect Y
# V2
indy = {
    "adc": 0x71,
    "and": 0x31,
    "cmp": 0xd1,
    "eor": 0x51,
    "lda": 0xb1,
    "ora": 0x11,
    "sbc": 0xf1,
    "sta": 0x91
    }

# Absolute
# V1
abso = {
    "adc": 0x6d,
    "and": 0x2d,
    "asl": 0x0e,
    "bit": 0x2c,
    "cmp": 0xcd,
    "cpx": 0xec,
    "cpy": 0xcc,
    "dec": 0xce,
    "eor": 0x4d,
    "inc": 0xee,
    "jmp": 0x4c,
    "jsr": 0x20,
    "lda": 0xad,
    "ldx": 0xae,
    "ldy": 0xac,
    "lsr": 0x4e,
    "ora": 0x0d,
    "rol": 0x2e,
    "ror": 0x6e,
    "sbc": 0xed,
    "sta": 0x8d,
    "stx": 0x8e,
    "sty": 0x8c
    }

# Absolute Indexed X
# V2
absx = {
    "adc": 0x7d,
    "and": 0x3d,
    "asl": 0x1e,
    "cmp": 0xdd,
    "dec": 0xde,
    "eor": 0x5d,
    "inc": 0xfe,
    "lda": 0xbd,
    "ldy": 0xbc,
    "lsr": 0x5e,
    "ora": 0x1d,
    "rol": 0x3e,
    "ror": 0x7e,
    "sbc": 0xfd,
    "sta": 0x9d
    }

# Absolute Indexed Y
# V2
absy = {
    "adc": 0x79,
    "and": 0x39,
    "cmp": 0xd9,
    "eor": 0x59,
    "lda": 0xb9,
    "ldx": 0xbe,
    "ora": 0x19,
    "sbc": 0xf9,
    "sta": 0x99
    }

# Accumulator
# V1
# will be no data
acc = {
    "asl": 0x0a,
    "lsr": 0x4a,
    "rol": 0x2a,
    "ror": 0x6a,
    }

# Immediate
# V1
# will be prefixed with a #
imm = {
    "adc": 0x69,
    "and": 0x29,
    "cmp": 0xc9,
    "cpx": 0xe0,
    "cpy": 0xc0,
    "eor": 0x49,
    "lda": 0xa9,
    "ldx": 0xa2,
    "ldy": 0xa0,
    "ora": 0x09,
    "sbc": 0xe9
    }

# Implied
# V1
# unique
imp = {
    "brk": 0x00,
    "clc": 0x18,
    "cld": 0xd8,
    "cli": 0x58,
    "clv": 0xb8,
    "dex": 0xca,
    "dey": 0x88,
    "inx": 0xe8,
    "iny": 0xc8,
    "nop": 0xea,
    "pha": 0x48,
    "php": 0x08,
    "pla": 0x68,
    "plp": 0x28,
    "rti": 0x40,
    "rts": 0x60,
    "sec": 0x38,
    "sed": 0xf8,
    "sei": 0x78,
    "tax": 0xaa,
    "tay": 0xa8,
    "tsx": 0xba,
    "txa": 0x8a,
    "txs": 0x9a,
    "tya": 0x98
    }

# Indirect
# V1
# unique
ind = {
    "jmp": 0x6C,
    }

# Relative
# V1
# unique
rel = {
    "bcc": 0x90,
    "bcs": 0xb0,
    "beq": 0xf0,
    "bmi": 0x30,
    "bne": 0xd0,
    "bpl": 0x10,
    "bvs": 0x70,
    "bvc": 0x50
    }

# Zero Page
# V2
zp = {
    "adc": 0x65,
    "and": 0x25,
    "asl": 0x06,
    "bit": 0x24,
    "cmp": 0xc5,
    "cpx": 0xe4,
    "cpy": 0xc4,
    "dec": 0xc6,
    "eor": 0x45,
    "inc": 0xe6,
    "lda": 0xa5,
    "ldx": 0xa6,
    "ldy": 0xa4,
    "lsr": 0x46,
    "ora": 0x05,
    "rol": 0x26,
    "ror": 0x66,
    "sbc": 0xe5,
    "sta": 0x85,
    "stx": 0x86,
    "sty": 0x84
    }

# Zero Page, X
# V2
zpx = {
    "adc": 0x75,
    "and": 0x35,
    "asl": 0x16,
    "cmp": 0xd5,
    "dec": 0xd6,
    "eor": 0x55,
    "inc": 0xf6,
    "lda": 0xb5,
    "ldy": 0xb4,
    "lsr": 0x56,
    "ora": 0x15,
    "rol": 0x36,
    "ror": 0x76,
    "sbc": 0xf5,
    "sta": 0x95,
    "sty": 0x94
    }

# Zero Page, Y
# V2
zpy = {
    "ldx": 0xb6,
    "stx": 0x96
    }

opcodes_list = [indx, indy, abso, absx, absy, acc, imm, imp, ind, rel, zp, zpx, zpy]
