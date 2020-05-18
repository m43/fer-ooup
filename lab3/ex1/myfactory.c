//
// Created by m43 on 18. 05. 2020..
//

#include "myfactory.h"

#include <stdio.h>
#include <dlfcn.h>

void *myfactory(const char *libname, const char *ctorarg) {
    void *handle = dlopen(libname, RTLD_LAZY);
    char *error;
    void *(*create)(const char *);

    if (!handle) {
        return NULL;
    }
    dlerror(); // to clear any existing errors

    *(void **) (&create) = dlsym(handle, "create");
    if ((error = dlerror()) != NULL) {
        dlclose(handle);
        return NULL;
    }

    void *result = (*create)(ctorarg);
    // dlclose(handle); // TODO Do i need to close the handle at some point? Closing it will remove the loaded vTables
    return result;
}
