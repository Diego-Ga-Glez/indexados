E5 ORG $4000
E1 EQU $3FF0
LDAA #20
LDAA %101
LDAA 7,SP
LDAA -16,SP
LDAA 34,PC
LDAA 16,SP
LDAA 256,SP
LDAA [16,SP]
LDAA [256,SP]
LDAA [-256,SP]
IBNE A, E4
JMP E4
JMP E5
BNE E4
BNE E5
BSZ 5
FILL 4,6
E4 START
BSZ 6
END
