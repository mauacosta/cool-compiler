from re import T
from string import Template

globalData =  """	.data
	.align  2
	.globl  class_nameTab
	.globl  Main_protObj
	.globl  Int_protObj
	.globl  String_protObj
	.globl  bool_const0
	.globl  bool_const1
	.globl  _int_tag
	.globl  _bool_tag
	.globl  _string_tag
_int_tag:
	.word   2
_bool_tag:
	.word   3
_string_tag:
	.word  4
	.globl  _MemMgr_INITIALIZER
_MemMgr_INITIALIZER:
	.word   _NoGC_Init
	.globl  _MemMgr_COLLECTOR
_MemMgr_COLLECTOR:
	.word   _NoGC_Collect
	.globl  _MemMgr_TEST
_MemMgr_TEST:
	.word   0
"""

stringConst = Template("""	.word	-1               
str_const$index:
	.word	4
	.word	$size
	.word	String_dispTab
	.word	int_const$intIndex
	.ascii	"$value"
	.byte	0	
	.align	2   
""")

intConst = Template("""	.word	-1
int_const$index:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	$value
""")

boolConst = Template("""	.word	-1
bool_const0:
	.word	3
	.word	4
	.word	Bool_dispTab
    .word	0
     .word	-1
bool_const1:
	.word	3
	.word	4
	.word	Bool_dispTab
    .word	1
""")

heap = Template("""	.globl	heap_start 
heap_start:
	.word	0 
	.text	 
	.globl	Main_init 
	.globl	Int_init 
	.globl	String_init 
	.globl	Bool_init 
	.globl	Main.main 
""")

objInit = Template("""
Object_init:
	addiu	$$sp $$sp -12 
	sw	$$fp 12($$sp) 
	sw	$$s0 8($$sp) 
	sw	$$ra 4($$sp) 
	addiu	$$fp $$sp 4  
	move	$$s0 $$a0 
	move	$$a0 $$s0 
	lw	$$fp 12($$sp) 
	lw	$$s0 8($$sp) 
	lw	$$ra 4($$sp) 
	addiu	$$sp $$sp 12 
	jr	$$ra 
""")


protInit= Template("""
$classInit:
	addiu	$$sp $$sp -12 
	sw	$$fp 12($$sp) 
	sw	$$s0 8($$sp) 
	sw	$$ra 4($$sp) 
	addiu	$$fp $$sp 4 
	move	$$s0 $$a0 
	jal	$jal
	move	$$a0 $$s0 
	lw	$$fp 12($$sp) 
	lw	$$s0 8($$sp) 
	lw	$$ra 4($$sp) 
	addiu	$$sp $$sp 12 
	jr	$$ra 
""")

protEnterMethod= Template("""
${className}.${methodName}:
	addiu	$$sp $$sp -$ts 		# m: frame has $nLocal locals
	sw	$$fp $fp ($$sp) 		# m: save $fp
	sw	$$s0 ${s0}($$sp) 		# m: save $$s0 (self)
	sw	$$ra ${ra}($$sp) 		# m: save $$ra
	addiu	$$fp $$sp 4 		# m: $$fp points to locals
	move	$$s0 $$a0 		# m: self to $$s0
""")
