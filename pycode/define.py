# python
#      lable  type 1
# annotation  type 2
# instruction type 3
ILABEL = 1
IANNOT = 2
IINSTR = 3

# weather or not add access memory flag type
# 0 not init
# 1 src dst --> register
# 2 src -->  register , dst --> memory 
# 3 src --> memory, dst --> register
# 4 src --> memory, dst --> memory
OPDREGREG = 1
OPDREGMEM = 2
OPDMEMREG = 3
OPDMEMMEM = 4
OPDREG = 5
OPDMEM = 6
OPDIMEREG = 7
OPDLABLE = 8

OPDIMEREGREG = 9
OPDIMEMEMREG = 10
OPDREGIMEREG = 11
OPDREGREGREG = 12



SFI_ADD_LABLE_NUM = 0
