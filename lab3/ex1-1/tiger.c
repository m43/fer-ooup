//
// Created by m43 on 18. 05. 2020..
//

#include <stdlib.h>

typedef char const *(*PTRFUN)();

typedef struct Animal {
    PTRFUN *vTable;
    const char *name;
} Tiger;

const char *name(Tiger *tiger) {
    return tiger->name;
}

const char *greet() {
    return "Roaar!";
}

const char *menu() {
    return "Srne s ajvarom!";
}

PTRFUN tigerVTable[] = {name, greet, menu};

int size() {
    return sizeof(Tiger);
}

void construct(Tiger *tiger, char const *name) {
    tiger->vTable = tigerVTable;
    tiger->name = name;
}

Tiger *create(char const *name) {
    Tiger *t = malloc(sizeof(Tiger));
    construct(t, name);
    return t;
}

Tiger **createMultiple(int n, char const **names) {
    Tiger **tigers = malloc(n * sizeof(Tiger));
    for (int i = 0; i < n; i++) {
        construct(tigers[i], names[i]);
    }
    return tigers;
}
