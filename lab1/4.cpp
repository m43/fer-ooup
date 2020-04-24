//
// Created by m43 on 28. 03. 2020..
//

#include <iostream>

class Base {
public:
    //if in doubt, google "pure virtual"
    virtual void set(int x) = 0;

    virtual int get() = 0;
};

class CoolClass : public Base {
public:
    virtual void set(int x) { x_ = x; };

    virtual int get() { return x_; };
private:
    int x_;
};

class PlainOldClass {
public:
    void set(int x) { x_ = x; };

    int get() { return x_; };
private:
    int x_; // if `x_ = 3` was written, then it would be initialized directly in the main (in assembly instructions)
};


int main() {

    PlainOldClass poc;
    Base *pb = new CoolClass;
    poc.set(42);
    pb->set(42);


    std::cout << sizeof(poc ) << std::endl;
    std::cout << sizeof(CoolClass) << std::endl;
    std::cout << sizeof(pb) << std::endl;

    return 0;
}

/* * * * * * * * * * * * * * * * * ZADATCI * * * * * * * * * * * * * * * *

 Note: I have an 64 bit processor and therefore will the memory addresses (as well as pointers to memory) be of 8 bytes.

 1. "Locate the parts of the assembler code that allocate memory for the objects poc and * pb."

    As poc and *pb are local variables, the memory for both of them is allocated in the call where the stack pointer
    (rsp) is moved to make room for all the local variables used by main, which is 40B. The call is "sub	rsp, 40".
    Of that 40B, Locations [-36,-32> is the space for the poc object and [-32,-24> is the space for the *pb pointer.


 2. "Explain the difference in how these objects are allocated."

    As the poc object is created right on stack and no initialization is needed. The space is reserved by the call
    `sub	rsp, 40`.

    For the cool class object, heap memory is allocated in the call "call	operator new(unsigned long)@PLT", and the
    pointer that gets returned by that call (and stored in rax). The constructor of CoolClass is later called with this
    heap memory address.

    Assembly code snippet:
    ```
        ; call new to create space on heap for the cool class
        xor	eax, eax	; eax to 0
        mov	edi, 16		; 16 is the size of the object to be allocated
        call	operator new(unsigned long)@PLT
        mov	rbx, rax ; rax holds the pointer to memory allocated by new for the cool class
        ; Later, after calling the CoolClass constructor, will the returned address be saved at location [rbp-32]
    ```


 3. "Find the part of the code in the assembler code that is responsible for calling the poc object's constructor."

    The poc does not have an constructor and has no variables or a vTable that needs to be initialized. If on the other
    hand, PlainOldClass object had to initialize x_, then the initialization lines would be directly added to main, and
    that would look like that:
    ```
        ;this are the assembly instructions that appear in main if x_=3 was written in PlainOldClass definition:
        mov	DWORD PTR -36[rbp], 3
        mov	edi, 16
    ```

    If plainOldClass had for some reason a virtual method, then a constructor should be automatically made in the
    assembly code that would call the base class (if there is any) and that would initialize the vTable. That is the
    case with CoolClass


 4. "Find the part of code in the assembler code that is responsible for calling the * pb object constructor. Consider
    exactly how that code is executed. What's going on in it?"

    The assembly code that takes care about calling the constructor of CoolClass is this assembly code snippet:
    ```
        ; call the constructor of the cool class
        mov	rdi, rbx    ; rdi holds the pointer to the objects itself - in this case it is the allocated heap memory address
                        ; of the CoolClass object
        call	CoolClass::CoolClass() ; constructor call
        mov	QWORD PTR -32[rbp], rbx ; rbx holds the pointer to the created class on the heap
    ```

    The call to the constructor is calling the code in this code snipped:
    ```
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

            lea	rdx, vtable for CoolClass[rip+16]	; load vTable into rdx
            mov	rax, QWORD PTR -8[rbp]				; get object address
            mov	QWORD PTR [rax], rdx				; save the vTable onto memory location where the object starts

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
    ```

    At some point, the constructor of the base class Base::BaseClass() gets called, in that part the following
    assembly code gets executed:
    ```
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

            ; put the Base vTable on the memory location where the object starts
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
    ```

 5. "Observe how the translator made calls pb-> set and poc.set. Explain the difference between the performance of
    these two calls. Which of these two calls requires less instruction? For which of these two implementations could
    an optimizing compiler generate code without a CALL instruction, or insert inlining directly?"

    The code snippet of the `poc.set` cal:
    ```
        ; calling set of poc
        lea	rax, -36[rbp] ; object memory address into rax
        mov	esi, 42 ; esi holds the parameter of the funciton call - 42
        mov	rdi, rax ; rdi will hold the address of the object, the function called will use it
        call	PlainOldClass::set(int)
    ```

    The code snippet of the `pb->set` call:
    ```
        ; calling set of cool class
        mov	rax, QWORD PTR -32[rbp]	; get the object location
        mov	rax, QWORD PTR [rax]	; load the vTable pointer provided it is saved at the start of the object
        mov	rdx, QWORD PTR [rax]	; load the concrete function from the vTabl. set is stored at the first slot in the vTabl.
                                    ; for calling get, one should take the pointer at location [rax+8]
        mov	rax, QWORD PTR -32[rbp]	; put the object locatio into rax
        mov	esi, 42		; put the function parameter into esi
        mov	rdi, rax	; put the object address into rdi
        call	rdx		; call CoolClass::set(int i)
    ```

    By observing these two snippets of code, one can conclude that the call to poc function takes less instructions and
    is therefore faster. Furthermore the call to poc function could be replaced with an inline implementation of the
    function, as the assembly code that gets called is known at compile time. Using an inline implementation,
    the compiler would optimise the execution of the function by 1. not using CALL and 2. being able to optimise
    the inline code with the surrounding instructions in main.

    For CoolClass::set(int i) call it is not the same because the compiler does not know at compile time which function
    is going to be called, but needs to determine that dynamically (aka dynamic binding aka run-time binding aka late
    binding). This is the cost of dynamic polymorphism in C++.

 6. "Find the assembler code to define and initialize the CoolClass class virtual function table."

    The definition of the CoolClass vTable is below the main. This are the assembly instructions:
    ```
            .section	.data.rel.ro.local._ZTV9CoolClass,"awG",@progbits,vtable for CoolClass,comdat
            .align 8
            .type	vtable for CoolClass, @object
            .size	vtable for CoolClass, 32
        vtable for CoolClass:
            .quad	0
            .quad	typeinfo for CoolClass
            .quad	CoolClass::set(int)
            .quad	CoolClass::get()
            .weak	vtable for Base
    ```

    The definition of the Base class vTable is "linked" in the vTable of CoolClass and is here:
    ```
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
    ```

    The initialization of the CoolClass object's vTable is here:
    ```
        ;... inside CoolClass::CoolClass() constructor
        lea	rdx, vtable for CoolClass[rip+16]	; load vTable into rdx
        mov	rax, QWORD PTR -8[rbp]				; get object address
        mov	QWORD PTR [rax], rdx				; save the vTable onto memory location where the object starts
        ;...
    ```

 * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * */