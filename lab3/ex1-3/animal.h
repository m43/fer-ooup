//
// Created by m43 on 18. 05. 2020..
//

#ifndef FER_OOUP_ANIMAL_H
#define FER_OOUP_ANIMAL_H

class Animal {
public:
    virtual char const *name() = 0;

    virtual char const *greet() = 0;

    virtual char const *menu() = 0;
};

#endif //FER_OOUP_ANIMAL_H
