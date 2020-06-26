#include <iostream>
#include <memory>
#include "maarray.h"

using namespace std;

int *apply_all(int const *const arr1, const size_t arr1_size, int const *const arr2, const size_t arr2_size) {
    if (arr1 == nullptr || arr2 == nullptr) {
        cout << "Šta si mi ovo dao" << endl;
        return nullptr;
    }

    int *result = new int[arr1_size * arr2_size];
    for (int i = arr1_size - 1; i >= 0; i--) {
        for (int j = arr2_size - 1; j >= 0; j--) {
            *(result + j * arr1_size + i) = arr1[i] * arr2[j];
        }
    }
    return result;
}

void print(int const *const array, const size_t array_size) {
    if (array == nullptr) {
        cout << "Šta si mi ovo dao" << endl;
        return;
    }

    cout << "[";
    for (size_t i = 0; i < array_size; i++) {
        cout << array[i] << (i == array_size - 1 ? "" : ", ");
    }
    cout << "]" << endl;
}

class B {
public:
    virtual int prva() = 0;

    virtual int druga() = 0;
};

class D : public B {
public:
    virtual int prva() { return 42; }

    virtual int druga(int x) { return prva() + x; }
};

// // declare bar as volatile pointer to array 64 of const int
//const int (*volatile bar)[64];

// // cast foo into block(int, long long) returning double
//(double ((*)(int, long long)) ) de;

int main() {

    // ### ooup peti ###
    D *de = nullptr;


    // ### smart pointers ###
    std::unique_ptr<int> ptr;
    std::unique_ptr<int> ptr2;

//    int i = 10;
    ptr = make_unique<int>(10);
    {
        int i = 10;
        int *int_ptr(&i);
        ptr = unique_ptr<int>(int_ptr); // Well, don't do this. i is on stack, smart pointers should point to heap!!
        *int_ptr = 20;
        cout << "x-->{.} <--x The unique int pointer is now: " << *ptr << endl;
    }
    cout << "x-->{}. <--x The unique int pointer is now: " << *ptr << endl;
    int x = 21;
    int y = 22;
    int z = 23;
    cout << "x-->{}_. <--x The unique int pointer is now: " << *ptr << endl;

    // ### ref vs ptr 2 ###
    int array1[]{1, 2, 3, 4, 5};
    const size_t array1_size{5};
    int array2[]{100, 200, 300};
    const size_t array2_size{3};


    print(array1, array1_size);
    print(array2, array2_size);

    int *result = apply_all(array1, 5, array2, 3);
    constexpr size_t result_size{array1_size * array2_size};

    cout << "The result is: ";
    print(result, result_size);

    delete[] result;

    // ### ma array ###
    // The things below are templates, not ref_vs_pointer :P
    MaArray<int, 10> maArray{};

    maArray.fill(1);
    maArray.print();


    maArray[0] = 10;
    maArray[1] = 9;
    maArray.print();

    cout << "The size of the array is " << maArray.getSize() << endl;
    maArray.update(2, 8);
    maArray.update(3, 7);
    maArray.update(4, 6);
    cout << maArray << endl;

    // maArray.get(-1); // throws invalid_argument("Invalid index given")
    // maArray.get(10); // throws invalid_argument("Invalid index given")

    return 0;
}

/**
 * About smart pointers:
 *  https://en.wikipedia.org/wiki/Smart_pointer
 *  https://stackoverflow.com/questions/106508/what-is-a-smart-pointer-and-when-should-i-use-one
 *  https://stackoverflow.com/questions/8334886/c11-smart-pointer-policies
 */