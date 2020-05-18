//
// Created by m43 on 18. 05. 2020..
//

#include <stdlib.h>

typedef const char *(*PTRFUN)();

typedef struct {
    PTRFUN *vTable;
    const char *name;
} Parrot;

const char *name(Parrot *p) {
    return p->name;
}

const char *greet() {
    return "Paapiga!!";
}

const char *menu() {
    return "Hladni kajmak s mrkvom.";
}

PTRFUN parrotVTable[] = {name, greet, menu};

void construct(Parrot *p, const char *name) {
    p->vTable = parrotVTable;
    p->name = name;
}

Parrot *create(const char *name) {
    Parrot *p = malloc(sizeof(Parrot));
    construct(p, name);
    return p;
}

Parrot **createMultiple(int n, const char **names) {
    Parrot **ps = malloc(n * sizeof(Parrot));
    for (int i = 0; i < n; i++) {
        construct(ps[i], names[i]);
    }
    return ps;
}
