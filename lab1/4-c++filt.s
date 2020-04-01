	.file	"4.cpp"
	.intel_syntax noprefix
	.text



	.section	.text._ZN9CoolClass3setEi,"axG",@progbits,CoolClass::set(int),comdat
	.align 2
	.weak	CoolClass::set(int)
	.type	CoolClass::set(int), @function
CoolClass::set(int):
.LFB0:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi
	mov	DWORD PTR -12[rbp], esi
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, DWORD PTR -12[rbp]
	mov	DWORD PTR 8[rax], edx
	nop
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	CoolClass::set(int), .-CoolClass::set(int)



	.section	.text._ZN9CoolClass3getEv,"axG",@progbits,CoolClass::get(),comdat
	.align 2
	.weak	CoolClass::get()
	.type	CoolClass::get(), @function
CoolClass::get():
.LFB1:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi
	mov	rax, QWORD PTR -8[rbp]
	mov	eax, DWORD PTR 8[rax]
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	CoolClass::get(), .-CoolClass::get()



	.section	.text._ZN13PlainOldClass3setEi,"axG",@progbits,PlainOldClass::set(int),comdat
	.align 2
	.weak	PlainOldClass::set(int)
	.type	PlainOldClass::set(int), @function
PlainOldClass::set(int):
.LFB2:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi
	mov	DWORD PTR -12[rbp], esi
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, DWORD PTR -12[rbp]
	mov	DWORD PTR [rax], edx
	nop
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	PlainOldClass::set(int), .-PlainOldClass::set(int)



	.section	.text._ZN4BaseC2Ev,"axG",@progbits,Base::Base(),comdat
	.align 2
	.weak	Base::Base()
	.type	Base::Base(), @function
Base::Base():
.LFB7:
	; prepare stack
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp

	; save the location of the object that was given in rdi
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi

	; put the Base vtable on the memory location where the object starts 
	lea	rdx, vtable for Base[rip+16]
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx

	; leave function
	nop
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	Base::Base(), .-Base::Base()
	.weak	Base::Base()
	.set	Base::Base(),Base::Base()



	.section	.text._ZN9CoolClassC2Ev,"axG",@progbits,CoolClass::CoolClass(),comdat
	.align 2
	.weak	CoolClass::CoolClass()
	.type	CoolClass::CoolClass(), @function
CoolClass::CoolClass():
.LFB9:
	; prepare stack aka rbp and rsp
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	
	; create space for local variables
	.cfi_def_cfa_register 6
	sub	rsp, 16

	mov	QWORD PTR -8[rbp], rdi ; first local variable - pointer to the CoolClass object that was stored in the rdi register
	mov	rax, QWORD PTR -8[rbp] ; load the object pointer into rax
	mov	rdi, rax			; put the address of the object into rdi and call the base constructor
	call	Base::Base()
	
	lea	rdx, vtable for CoolClass[rip+16]	; load vtable into rdx 
	mov	rax, QWORD PTR -8[rbp]				; get object address
	mov	QWORD PTR [rax], rdx				; save the vtable onto memory location where the object starts
	
	; leave the function
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	CoolClass::CoolClass(), .-CoolClass::CoolClass()
	.weak	CoolClass::CoolClass()
	.set	CoolClass::CoolClass(),CoolClass::CoolClass()



	.text
	.globl	main
	.type	main, @function
main:
.LFB4:
	; prepare stack, save context
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	push	rbx

	; make the "workspace" aka space for local variables for main - 5 bytes of space 
	; rsp is moved because other functions that use stack will be called and for them the stack pointer must be proprly set
	sub	rsp, 40 ; why so much? This is why:
                ;       8 for pb pointer
                ;       8 ( = 4 + maybe 4 for padding) for poco object that is saved on stack
                ;       8 for stack canary protection
                ;       16 as by _86x64 calling convention that requires non-leaf functions to maintain 16-byte
                ;           alignment of stack pointer outside of prolog. Source (page 526., paragraph 3):
                ;           https://books.google.hr/books?id=plInCgAAQBAJ&pg=PA526&lpg=PA526&dq=x86+assembly+why+function+allocates+16+bytes+that+are+not+used&source=bl&ots=-MLt08Dq5w&sig=ACfU3U0342GcM7FswbX2ceo5eAvcBofuvg&hl=en&sa=X&ved=2ahUKEwiPnOze1MToAhWR6aYKHRQsAHUQ6AEwAHoECAkQAQ#v=onepage&q=x86%20assembly%20why%20function%20allocates%2016%20bytes%20that%20are%20not%20used&f=false
                ;           Wikipedia, but no citations (accessed 31.3.2020.) :( https://en.wikipedia.org/wiki/X86_calling_conventions
                ; What is the purpose of the remaining 16B?

	; stack canary protection
	;	https://stackoverflow.com/questions/42118030/how-do-canary-words-allow-gcc-to-detect-buffer-overflows
	;	https://stackoverflow.com/questions/42118030/how-do-canary-words-allow-gcc-to-detect-buffer-overflows
	.cfi_offset 3, -24
	mov	rax, QWORD PTR fs:40
	mov	QWORD PTR -24[rbp], rax

	; call new to create space on heap for the cool class
	xor	eax, eax	; eax to 0
	mov	edi, 16		; 16 is the size of the object to be allocated
	call	operator new(unsigned long)@PLT
	mov	rbx, rax ; rax holds the pointer to memory allocated by new for the cool class
	; Later, after calling the CoolClass constructor, will the returned address be saved at location [rbp-32]

	; call the constructor of the cool class
	mov	rdi, rbx ; rdi holds the pointer to the objects itself - in this case it is the heap memory address of the allocated cool class
	call	CoolClass::CoolClass() ; constructor call
	mov	QWORD PTR -32[rbp], rbx ; rbx holds the pointer to the created class on the heap

	
    ; calling set of poc
	lea	rax, -36[rbp] ; object memory address into rax
	mov	esi, 42 ; esi holds the parameter of the funciton call - 42
	mov	rdi, rax ; rdi will hold the address of the object, the function called will use it
	call	PlainOldClass::set(int)

	; calling set of cool class
	mov	rax, QWORD PTR -32[rbp]	; get the object location
	mov	rax, QWORD PTR [rax]	; load the vtable pointer provided it is saved at the start of the object	
	mov	rdx, QWORD PTR [rax]	; load the concrete function from the vtable. set is stored at the first slot in the vtable.
								; for calling get, one should take the pointer at location [rax+8]
	mov	rax, QWORD PTR -32[rbp]	; put the object locatio into rax
	mov	esi, 42		; put the function parameter into esi
	mov	rdi, rax	; put the object address into rdi
	call	rdx		; call CoolClass::set(int i)

	; Checking the stack protection and returning 0
	mov	eax, 0
	mov	rcx, QWORD PTR -24[rbp]
	xor	rcx, QWORD PTR fs:40
	je	.L9
	call	__stack_chk_fail@PLT
.L9:
	add	rsp, 40
	pop	rbx
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	main, .-main



	.weak	vtable for CoolClass
	.section	.data.rel.ro.local._ZTV9CoolClass,"awG",@progbits,vtable for CoolClass,comdat
	.align 8
	.type	vtable for CoolClass, @object
	.size	vtable for CoolClass, 32
vtable for CoolClass:
	.quad	0
	.quad	typeinfo for CoolClass ; points to the section below
	.quad	CoolClass::set(int)
	.quad	CoolClass::get()



	.weak	vtable for Base
	.section	.data.rel.ro._ZTV4Base,"awG",@progbits,vtable for Base,comdat
	.align 8
	.type	vtable for Base, @object
	.size	vtable for Base, 32
vtable for Base:
	.quad	0
	.quad	typeinfo for Base
	.quad	__cxa_pure_virtual
	.quad	__cxa_pure_virtual



	.weak	typeinfo for CoolClass
	.section	.data.rel.ro._ZTI9CoolClass,"awG",@progbits,typeinfo for CoolClass,comdat
	.align 8
	.type	typeinfo for CoolClass, @object
	.size	typeinfo for CoolClass, 24
typeinfo for CoolClass:
	.quad	vtable for __cxxabiv1::__si_class_type_info+16
	.quad	typeinfo name for CoolClass
	.quad	typeinfo for Base



	.weak	typeinfo name for CoolClass
	.section	.rodata._ZTS9CoolClass,"aG",@progbits,typeinfo name for CoolClass,comdat
	.align 8
	.type	typeinfo name for CoolClass, @object
	.size	typeinfo name for CoolClass, 11
typeinfo name for CoolClass:
	.string	"9CoolClass"




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
	.ident	"GCC: (Arch Linux 9.3.0-1) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
