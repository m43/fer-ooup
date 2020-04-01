//
// Created by m43 on 28. 03. 2020..
//

#include <iostream>

// class __attribute__((__packed__)) CoolClass { // this attribute forces the class to be packed aka with no padding
class CoolClass {
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
    int x_;
};

int main() {

    auto *poco = new PlainOldClass;
    auto *cool = new CoolClass;

    printf("Lets check the sizes of classes PlainOldClass and CoolClass\n");
    printf("\tsizeof(PlainOldClass)=%lu\n", sizeof(PlainOldClass));
    printf("\tsizeof(CoolClass))=%lu\n\n", sizeof(CoolClass));

    printf("From this results one can see that the CoolClass is bigger. This is because the CoolClass has\n"
           "virtual class member functions and therefore must have a pointer to a virtual table. The total\n"
           "overhead of providing this dynamic polymorphism functionality is in this case of size %lu.\n\n"
           "N.B. The output will depend on the compiler (how the packing is done and how dynamic\n"
           "polymorphisms is implemented) and computer architecture (32 vs 64 bit). In my case it was 4 vs\n"
           "16 bytes, and that is because in the memory it would look like this for PlainOldClass:\n"
           "\t|#############|##############|\n"
           "\t|#############|##############|\n"
           "\t| int x_-->4B |##############|\n"
           "\t|#############|##############|\n"
           "\t|#############|##############|\n"
           "Whereas for the CoolClass the memory would look like this:\n"
           "\t|#############|##############|\n"
           "\t|#############|##############|\n"
           "\t| int x_-->4B | padding-->4B |\n"
           "\t|    VTable pointer --> 8B   |\n"
           "\t|#############|##############|\n"
           "\t|#############|##############|\n",
           sizeof(CoolClass) - sizeof(PlainOldClass));

    delete poco;
    delete cool;

    return 0;
}
