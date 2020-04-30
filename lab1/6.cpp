//
// Created by m43 on 28. 03. 2020..
//

#include <stdio.h>

class Base {
public:
    Base() {
        metoda();
    }

    virtual void virtualnaMetoda() {
        printf("ja sam bazna implementacija!\n");
    }

    void metoda() {
        printf("Metoda kaze: ");
        virtualnaMetoda();
    }
};

class Derived : public Base {
public:
    Derived() : Base() {
        metoda();
    }

    virtual void virtualnaMetoda() {
        printf("ja sam izvedena implementacija!\n");
    }
};

int main() {
    Derived *pd = new Derived();
    pd->metoda();
}

/* * * * * * * * * * * * * * * * * ZADATCI * * * * * * * * * * * * * * * *

  Task: "This exercise indicates the different behavior of polymorphic calls during and after completion of the object's
        construction. Explain the program output by analyzing translated machine code. Notice who, when, and where
        initializes/modifies the pointer to the virtual function table."

    This is the order of execution when creating Derived pointer `*pd`:
        1.  +enter Derived::Derived()
        2.  |   +enter Base::Base()
        3.  |   |   +enter Base::metoda()                --> "Metoda kaze: "
        4.  |   |   |   +enter Base::virtualnaMetoda()   --> "ja sam bazna implementacija!"
        5.  |   |   |   -leave Base::virtualnaMetoda()
        6.  |   |   -leave Base::metoda()
        7.  |   -leave Base::Base()
        8.  |   +enter Derived::metoda()                --> "Metoda kaze: "
        9.  |   |   +enter Derived::virtualnaMetoda()   --> "ja sam bazna implementacija!"
        10. |   |   -leave Derived::virtualnaMetoda()
        11. |   -leave Derived::metoda()
        12. -leave Derived::Derived()

    This is what happens inside the constructor of Derived:
    ```
        ; ...
        ; ...
        call	Base::Base()					; call the base constructor
        lea	rdx, vtable for Derived[rip+16]		; set the vTable for Derived (overwrites the vTable of the Base class)
        ; ...
        call	Base::metoda()					; call to metoda(), staticaly bound to Base::metoda()
        ; ...
        ; ...
    ```

     This is what happens inside the constructor of Base:
     ```
        ; ...
        ; ...
        lea	rdx, vtable for Base[rip+16]		; initialize the vTable for Base
        ; ...
        call	Base::metoda()					; call to metoda(), staticaly bound to Base::metoda()
        ; ...
        ; ...
     ```

    And by calling Base::metoda(), this is what gets called:
    ```
        ; ...
        ; ...
        call	printf@PLT              ; printf "Metoda kaze: "
        mov	rax, QWORD PTR -8[rbp]
        mov	rax, QWORD PTR [rax]
        mov	rdx, QWORD PTR [rax]		; take the first virtual method
        mov	rax, QWORD PTR -8[rbp]
        mov	rdi, rax
        call	rdx						; dynamically call the first method in the vTable
        ; ...
        ; ...
    ```

    To summarize what happened at the assembly code level to the virtual tables:
        1.  'Derived::Derived()' is called and the first thing it does is call the base constructor aka 'Base::Base()'.
            The base constructor sets the vTable of the object to it's own vTable and then calls 'Base::metoda()' which
            calls 'virtualnaMetoda()' that then gets dynamically bound to 'Base::virtualnaMetoda()'.
        2.  After the Base constructor has finished, we are back at in the 'Derived::Derived' constructor, and
            the second thing this constructor does is set the object's vTable pointer to it's own vTable.
        3.  The third thing 'Derived::Derived' does is make a static call to 'Base::metoda()'. In this function,
            'virtualnaMetoda' gets called, and that call is dynamically bound to call 'Derived::virtualnaMetoda()'.

    N.B. Java, C# and Python are for example different:
        - https://stackoverflow.com/questions/10404879/polymorphism-and-constructors
        - https://stackoverflow.com/questions/119506/virtual-member-call-in-a-constructor
        - https://stackoverflow.com/questions/3091833/calling-member-functions-from-a-constructor
        - Python does not call the base constructor automatically as in Java, C# and C++, one needs to do it
          explicitly: https://stackoverflow.com/questions/60015319/is-it-necessary-to-call-super-init-explicitly-in-python
          As self is passed all around, the virtual method called will be the one associated with the concrete object.
          ./6_playground.py has a demonstration program

    "What is the basic difference when writing code that accesses data members or class member functions
    from inside class member functions in Java and Python programming languages?"

    Well the obvious difference is self vs this. For class function members it is important to note
    that self.someVirtualFunction() would look for the function in the self.__dict__ member variable,
    whereas in Java someVirtualFunction() would look for the function in the vtable of the object.


 * * * * * * * * * * * * * * * *  * * * * * * * * * * * * * * * * * * * */