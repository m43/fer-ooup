//
// Created by m43 on 18. 05. 2020..
//

#ifndef FER_OOUP_MYFACTORY_H
#define FER_OOUP_MYFACTORY_H

#include <map>
#include <memory>

using namespace std;


class MyFactory {
public:
    typedef void *(*CREATORFUN)(const string &);

    static MyFactory &instance();

    int registerCreator(const string &name, void *(*creatorFunction)(const string &));

    const map<string, CREATORFUN> &getCreators();

    CREATORFUN getCreator(const string &name);

private:
    MyFactory() = default;;

    ~MyFactory() = default;

    map<std::string, CREATORFUN> creatorsMap_;
};

#endif //FER_OOUP_MYFACTORY_H
