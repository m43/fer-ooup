//
// Created by m43 on 18. 05. 2020..
//

#include "myfactory.h"

#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>

void *myfactory(const char *libname, const char *ctorarg) {
    void *handle = dlopen(libname, RTLD_LAZY);
    char *error;
    void *(*construct)(void *, const char *);
    int (*sizeOfAnimal)();

    if (!handle) {
        return NULL;
    }
    dlerror(); // to clear any existing errors

    *(void **) (&construct) =
            dlsym(handle, "construct");
    sizeOfAnimal = dlsym(handle, "size");

    if ((error = dlerror()) != NULL) {
        dlclose(handle);
        return NULL;
    }

    void *result = malloc(sizeOfAnimal());
    (*construct)(result, ctorarg);
    // dlclose(handle); // TODO Do i need to close the handle at some point? Closing it will remove the loaded vTables
    return result;
}
