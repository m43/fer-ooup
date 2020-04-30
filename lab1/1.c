#include <stdio.h>
#include <stdlib.h>

// Analogies with OO programming are marked next to particular lines of code, as comments starting with ~

//typedef char const *(*PTRFUN)();


// Preparing the animals

typedef struct Animal {  // ~ class
    void **vtable;  // ~ pointer to virtual table
    char const *name;  // ~ a member variable
} Animal;

void animalPrintGreeting(Animal *a) {  // ~ static method of class Animal, usually impl. through early binding (c++)
    printf("%s pozdravlja: %s\n", a->name, ((const char *(*)()) a->vtable[0])());
    // Note that:
    // "((const char *(*)()) a->vTable[0])()"
    // Could also have been written as:
    // "((PTRFUN) a->vTable[0])()"
}

void animalPrintMenu(Animal *a) {  // ~ static method of class Animal
    printf("%s voli: %s\n", a->name, ((const char *(*)()) a->vtable[1])());
}

// Here comes the dogy
char const *dogGreet(void) {  // ~ derived method, dynamic polymorphism in action
    return "vau!";
}

char const *dogMenu(void) {  // ~ derived method
    return "kuhanu govedinu";
}

void *dogsVTable[2] = {dogGreet, dogMenu};  // ~ virtual table for derived class
// void **doggies = dogsVTable;

void constructDog(Animal *a, char const *name) {  // ~ class constructor for class Dog, binding
    /* What is the difference between &dogsVTable and dogsVTable? Both work. A: They both work because dogsVTable is
     * defined as an array, and for arrays the following is true &array=array. If that variable was not an array,
     * just like doggies is not, then one must be more careful with using &doggies and doggies, because &doggies is now
     * the address of the pointer not of the array it's pointing to.
     * In other words, for doggies this would be correct:
     *      a->vtable = doggies;
     * .. while this would not work:
     *      a-vtable = *doggies;
     *
     * Debug that proves this:
     *      printf("\tDoggies:\n");
     *      printf("%d\n", (int) doggies);
     *      printf("%d\n", (int) &doggies);
     *      printf("\tdogsVTable\n");
     *      printf("%d\n", (int) dogsVTable);
     *      printf("%d\n", (int) &dogsVTable);
     */
    a->vtable = dogsVTable;

    // TODO will this now point to the same location as given "name"? Could this make problems if name was on stack?
    a->name = name;
}

Animal *createDog(char const *name) {  // ~ class constructor for class Dog, memory allocation
    Animal *a = malloc(sizeof(Animal));
    constructDog(a, name);
    return a;
}

Animal *createDogs(int n, char const *names[]) {  // ~ could be a static method of class Dog
    Animal *dogs = malloc(sizeof(Animal) * n);
    for (int i = 0; i < n; i++) {
        constructDog(&dogs[i], names[i]);
    }
    return dogs;
}

// Is "Ofelija" really a cat?
char const *catGreet(void) {  // ~ derived mehod
    return "mijau!";
}

char const *catMenu(void) {  // ~ derived mehod
    return "konzerviranu tunjevinu";
}

void *catsVTable[2] = {catGreet, catMenu};  // ~ virtual table for class Cat

void constructCat(Animal *a, char const *name) {  // ~ constructor for class Cat, binding
    a->vtable = catsVTable;
    a->name = name;
}

Animal *createCat(char const *name) {  // ~ constructor for class Cat, memory allocation
    Animal *a = malloc(sizeof(Animal));
    constructCat(a, name);
    return a;
}

// The animal demonstration function
void testAnimals(void) {  // ~ demonstration program or a very simple unit test with no asserts
    struct Animal *p1 = createDog("Hamlet");
    struct Animal *p2 = createCat("Ofelija");
    struct Animal *p3 = createDog("Polonije");

    animalPrintGreeting(p1);
    animalPrintGreeting(p2);
    animalPrintGreeting(p3);

    animalPrintMenu(p1);
    animalPrintMenu(p2);
    animalPrintMenu(p3);

    free(p1);
    free(p2);
    free(p3);
}

// This demonstration program creates objects
void testAnimalsStack(void) {
    // Note that for doing this:
    //      "Pokažite da je konkretne objekte moguće kreirati i na gomili i na stogu
    //      (detalji). Memorijski prostor na stogu zauzmite lokalnom varijablom, a za
    //      zauzimanje memorije na gomili pozovite malloc."
    // I would need to call constructor(Animal*, char const*) directly, and that needs to be done
    // so that the variable created on stack and passed as the first argument of that constructor
    // is of the same or wider scope as the scope in which it will be used afterwards.
    // In other words, animals created in this help method, must not leave the method
    // (because they'll) get removed from stack! 

    Animal a1 = {};
    Animal a2 = {};
    Animal a3 = {};

    constructDog(&a1, "Hamlet");
    {
        char *ofelija = "Ofelija";  // This works
        // TODO check this
        // char *ofelija = {'O', 'f', 'e', 'l', 'i', 'j', 'a', '\0'};  //This way ofelija is on stack -> 139 (signal 11: SIGSEGV)
        constructCat(&a2, ofelija);
    }
    constructDog(&a3, "Polonije");

    animalPrintGreeting(&a1);
    animalPrintGreeting(&a2);
    animalPrintGreeting(&a3);

    animalPrintMenu(&a1);
    animalPrintMenu(&a2);
    animalPrintMenu(&a3);
}


// Mexican dogs creation utility
void testNDogs(void) {  // ~ demonstration program or a very simple unit test with no asserts
    char const *dogNames[6] = {"Alba", "Bonita", "Alma", "Amigo", "Sol", "Burrito"};
    Animal *dogs = createDogs(6, dogNames);
    for (int i = 0; i < 6; i++) {
        animalPrintGreeting(&dogs[i]);
    }
    free(dogs);
}

// After all, lets run it
int main(void) {  // ~ program main entry point

    testAnimals();
    printf("\n");

    testAnimalsStack();
    printf("\n");

    testNDogs();

    return 0;
}