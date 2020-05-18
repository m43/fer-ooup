#include "myfactory.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdlib.h>

typedef char const *(*PTRFUN)();

struct Animal {
    PTRFUN *vtable;
    // vtable entries:
    // 0: char const* name(void* this);
    // 1: char const* greet();
    // 2: char const* menu();
};

void animalPrintGreeting(struct Animal *a) {
    printf("%s pozdravlja: %s\n", ((PTRFUN) a->vtable[0])(), ((PTRFUN) a->vtable[1])());
}

void animalPrintMenu(struct Animal *a) {
    printf("%s voli: %s\n", ((PTRFUN) a->vtable[0])(a), ((PTRFUN) a->vtable[2])());
}

const char *names[] = {
        "Modrobradi", "X Æ A-11", "Alcabú",
        "Covarrubias", "Bautista", "Miguel",
        "Mancebo", "Piñón", "Nico", "Ramon",
        "Sancho"};

const char *getRandomName() {
    int idx = rand() % (sizeof(names) / sizeof(names[0]));
    return names[idx];
}

int main(int argc, char *argv[]) {
    srand(time(NULL));
    for (int i = 1; i < argc; ++i) {
        struct Animal *p = (struct Animal *) myfactory(argv[i], getRandomName());
        if (!p) {
            printf("Creation of plug-in object %s failed.\n", argv[i]);
            continue;
        }

        animalPrintGreeting(p);
        animalPrintMenu(p);
        free(p);
    }
}