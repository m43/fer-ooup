//
// Created by m43 on 18. 05. 2020..
//

#include <string>
#include <utility>
#include "animal.h"
#include "myfactory.h"

using namespace std;

class Tiger : public Animal {
public:
    Tiger(string name) : name_(std::move(name)) {}

private:
    const char *name() override {
        return name_.c_str();
    }

    const char *greet() override {
        return "Roar!";
    }

    const char *menu() override {
        return "Sarma od srnetine sa kajmakom!";
    }

private:
    string name_;
};

static Animal* myCreator(const string &arg) {
    return new Tiger(arg);
}

static int hreg = MyFactory<Animal>::instance().registerCreator("tiger", myCreator);
