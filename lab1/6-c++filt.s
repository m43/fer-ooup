	.file	"6.cpp"
	.intel_syntax noprefix
	.text
	.section	.text._ZN4BaseC2Ev,"axG",@progbits,Base::Base(),comdat
	.align 2
	.weak	Base::Base()
	.type	Base::Base(), @function
Base::Base():
.LFB1:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rdx, vtable for Base[rip+16]		; initialize the vtable for Base
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::metoda()					; call to metoda(), staticaly bound to Base::metoda()
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	Base::Base(), .-Base::Base()
	.weak	Base::Base()
	.set	Base::Base(),Base::Base()



	.section	.rodata
.LC0:
	.string	"ja sam bazna implementacija!"



	.section	.text._ZN4Base15virtualnaMetodaEv,"axG",@progbits,Base::virtualnaMetoda(),comdat
	.align 2
	.weak	Base::virtualnaMetoda()
	.type	Base::virtualnaMetoda(), @function
Base::virtualnaMetoda():
.LFB3:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rdi, .LC0[rip]
	call	puts@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	Base::virtualnaMetoda(), .-Base::virtualnaMetoda()



	.section	.rodata
.LC1:
	.string	"Metoda kaze: "



	.section	.text._ZN4Base6metodaEv,"axG",@progbits,Base::metoda(),comdat
	.align 2
	.weak	Base::metoda()
	.type	Base::metoda(), @function
Base::metoda():
.LFB4:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rdi, .LC1[rip]
	mov	eax, 0
	call	printf@PLT
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]		; take the first virtual method
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	rdx						; dynamically call the first method in the vtable
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	Base::metoda(), .-Base::metoda()



	.section	.text._ZN7DerivedC2Ev,"axG",@progbits,Derived::Derived(),comdat
	.align 2
	.weak	Derived::Derived()
	.type	Derived::Derived(), @function
Derived::Derived():
.LFB6:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::Base()					; call the base constructor
	lea	rdx, vtable for Derived[rip+16]		; set the vtable for Derived (overwrites the vtable of the Base class)
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::metoda()					; call to metoda(), staticaly bound to Base::metoda()
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	Derived::Derived(), .-Derived::Derived()
	.weak	Derived::Derived()
	.set	Derived::Derived(),Derived::Derived()



	.section	.rodata
	.align 8
.LC2:
	.string	"ja sam izvedena implementacija!"



	.section	.text._ZN7Derived15virtualnaMetodaEv,"axG",@progbits,Derived::virtualnaMetoda(),comdat
	.align 2
	.weak	Derived::virtualnaMetoda()
	.type	Derived::virtualnaMetoda(), @function
Derived::virtualnaMetoda():
.LFB8:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rdi, .LC2[rip]
	call	puts@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	Derived::virtualnaMetoda(), .-Derived::virtualnaMetoda()



	.text
	.globl	main
	.type	main, @function
main:
.LFB9:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA9
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	push	r12
	push	rbx
	sub	rsp, 16
	.cfi_offset 12, -24
	.cfi_offset 3, -32
	mov	edi, 8
.LEHB0:
	call	operator new(unsigned long)@PLT	; allocate heap memory for a Derived object
.LEHE0:
	mov	rbx, rax
	mov	rdi, rbx
.LEHB1:
	call	Derived::Derived()	; call the constructor of class Derived
.LEHE1:
	mov	QWORD PTR -24[rbp], rbx
	mov	rax, QWORD PTR -24[rbp]
	mov	rdi, rax
.LEHB2:
	call	Base::metoda()		; compiler knows that Base::metoda will be called because it can be staticaly determined aka metoda() is not virtual!
	mov	eax, 0
	jmp	.L10
.L9:
	mov	r12, rax
	mov	esi, 8
	mov	rdi, rbx
	call	operator delete(void*, unsigned long)@PLT
	mov	rax, r12
	mov	rdi, rax
	call	_Unwind_Resume@PLT
.LEHE2:
.L10:
	add	rsp, 16
	pop	rbx
	pop	r12
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.globl	__gxx_personality_v0
	.section	.gcc_except_table,"a",@progbits
.LLSDA9:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9-.LLSDACSB9
.LLSDACSB9:
	.uleb128 .LEHB0-.LFB9
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB9
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L9-.LFB9
	.uleb128 0
	.uleb128 .LEHB2-.LFB9
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE9:
	.text
	.size	main, .-main


	.weak	vtable for Derived
	.section	.data.rel.ro.local._ZTV7Derived,"awG",@progbits,vtable for Derived,comdat
	.align 8
	.type	vtable for Derived, @object
	.size	vtable for Derived, 24
vtable for Derived:
	.quad	0
	.quad	typeinfo for Derived
	.quad	Derived::virtualnaMetoda()


	.weak	vtable for Base
	.section	.data.rel.ro.local._ZTV4Base,"awG",@progbits,vtable for Base,comdat
	.align 8
	.type	vtable for Base, @object
	.size	vtable for Base, 24
vtable for Base:
	.quad	0
	.quad	typeinfo for Base
	.quad	Base::virtualnaMetoda()


	.weak	typeinfo for Derived
	.section	.data.rel.ro._ZTI7Derived,"awG",@progbits,typeinfo for Derived,comdat
	.align 8
	.type	typeinfo for Derived, @object
	.size	typeinfo for Derived, 24
typeinfo for Derived:
	.quad	vtable for __cxxabiv1::__si_class_type_info+16
	.quad	typeinfo name for Derived
	.quad	typeinfo for Base


	.weak	typeinfo name for Derived
	.section	.rodata._ZTS7Derived,"aG",@progbits,typeinfo name for Derived,comdat
	.align 8
	.type	typeinfo name for Derived, @object
	.size	typeinfo name for Derived, 9
typeinfo name for Derived:
	.string	"7Derived"


	.weak	typeinfo for Base
	.section	.data.rel.ro._ZTI4Base,"awG",@progbits,typeinfo for Base,comdat
	.align 8
	.type	typeinfo for Base, @object
	.size	typeinfo for Base, 16
typeinfo for Base:
	.quad	vtable for __cxxabiv1::__class_type_info+16
	.quad	typeinfo name for Base


	.weak	typeinfo name for Base
	.section	.rodata._ZTS4Base,"aG",@progbits,typeinfo name for Base,comdat
	.type	typeinfo name for Base, @object
	.size	typeinfo name for Base, 6
typeinfo name for Base:
	.string	"4Base"
	.hidden	DW.ref.__gxx_personality_v0


	.weak	DW.ref.__gxx_personality_v0
	.section	.data.rel.local.DW.ref.__gxx_personality_v0,"awG",@progbits,DW.ref.__gxx_personality_v0,comdat
	.align 8
	.type	DW.ref.__gxx_personality_v0, @object
	.size	DW.ref.__gxx_personality_v0, 8
DW.ref.__gxx_personality_v0:
	.quad	__gxx_personality_v0
	.ident	"GCC: (Arch Linux 9.3.0-1) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
