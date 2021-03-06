//
// Created by m43 on 18. 05. 2020..
//

#include "myfactory.h"
#include "animal.h"

#include <iostream>

using namespace std;

const char *names[] = {
        "Modrobradi", "X Æ A-11", "Alcabú",
        "Covarrubias", "Bautista", "Miguel",
        "Mancebo", "Piñón", "Nico", "Ramon",
        "Sancho"};

const char *getRandomName() {
    int idx = rand() % (sizeof(names) / sizeof(names[0]));
    return names[idx];
}

int main() {
    srand(time(NULL));
    for (const auto &c: MyFactory<Animal>::instance().getCreators()) {
        Animal *a = c.second(getRandomName());
        cout << a->name() << " pozdravlja: " << a->greet() << endl;
        cout << a->name() << " voli: " << a->menu() << endl;
    }

    // this one does not exist (but will not throw):
    MyFactory<Animal>::instance().getCreator("Ćuko");
}