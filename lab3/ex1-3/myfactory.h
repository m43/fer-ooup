//
// Created by m43 on 18. 05. 2020..
//

#ifndef FER_OOUP_MYFACTORY_H
#define FER_OOUP_MYFACTORY_H

#include <map>
#include <memory>

using namespace std;

template<typename PRODUCT>
class MyFactory {
public:
    typedef PRODUCT *(*CREATORFUN)(const string &);

    static MyFactory<PRODUCT> &instance();

    int registerCreator(const string &name, CREATORFUN creatorFunction);

    const map<string, CREATORFUN> &getCreators();

    CREATORFUN getCreator(const string &name);

private:
    MyFactory() = default;;

    ~MyFactory() = default;

    map<std::string, CREATORFUN> creatorsMap_;
};

// NOTE: decl and def are in one file cause:
//      https://stackoverflow.com/questions/115703/storing-c-template-function-definitions-in-a-cpp-file
//      https://isocpp.org/wiki/faq/templates#templates-defn-vs-decl

template<typename PRODUCT>
MyFactory<PRODUCT> &MyFactory<PRODUCT>::instance() {
    static MyFactory instance_;
    return instance_;
}

template<typename PRODUCT>
int MyFactory<PRODUCT>::registerCreator(const string &name, MyFactory::CREATORFUN creatorFunction) {
    creatorsMap_.insert({name, creatorFunction});
    return creatorsMap_.size() - 1;
}

template<typename PRODUCT>
const map<string, typename MyFactory<PRODUCT>::CREATORFUN> &MyFactory<PRODUCT>::getCreators() {
    return creatorsMap_;
}

template<typename PRODUCT>
typename MyFactory<PRODUCT>::CREATORFUN MyFactory<PRODUCT>::getCreator(const string &name) {
    for (const auto &c: creatorsMap_) {
        if (c.first == name) {
            return c.second;
        }
    }
    return nullptr;
}

#endif //FER_OOUP_MYFACTORY_H
