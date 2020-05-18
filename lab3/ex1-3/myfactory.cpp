//
// Created by m43 on 18. 05. 2020..
//

#include "myfactory.h"


MyFactory &MyFactory::instance() {
    static MyFactory instance_;
    return instance_;
}

int MyFactory::registerCreator(const string &name, CREATORFUN creatorFunction) {
    creatorsMap_.insert({name, creatorFunction});
    return creatorsMap_.size() - 1;
}

const map<string, MyFactory::CREATORFUN> &MyFactory::getCreators() {
    return creatorsMap_;
}

MyFactory::CREATORFUN MyFactory::getCreator(const string &name) {
    for (const auto &c: creatorsMap_) {
        if (c.first == name) {
            return c.second;
        }
    }
    return nullptr;
}
