//
// Created by m43 on 18. 05. 2020..
//

//
// Created by m43 on 18. 05. 2020..
//

#include <string>
#include <utility>
#include "animal.h"
#include "myfactory.h"

using namespace std;

class Parrot : public Animal {
public:
    Parrot(string name) : name_(std::move(name)) {}

private:
    const char *name() override {
        return name_.c_str();
    }

    const char *greet() override {
        return "Papiga!";
    }

    const char *menu() override {
        return "Sirnica!!";
    }

private:
    string name_;
};

static Animal* myCreator(const string &arg) {
    return new Parrot(arg);
}

static int hreg = MyFactory<Animal>::instance().registerCreator("parrot", myCreator);
