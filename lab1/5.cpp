//
// Created by m43 on 28. 03. 2020..
//

#include <iostream>

class B {
public:
    virtual int prva() = 0;

    virtual int druga(int) = 0;

    virtual ~B() = default;;
};

class D : public B {
public:
    int prva() override { return 42; }

    int druga(int x) override { return prva() + x; }
};

void pokucajNaDrugaVrata(B *b) {
    void ** vTable = *(void ***) b;

    int first = ((int (*)(B*)) vTable[0])(b);
    printf("%d\n", first);

    int second = ((int (*)(B *, int)) vTable[1])(b, 72000);
    printf("%d\n\n", second);
}

int main() {
    B *pb = new D();

    pokucajNaDrugaVrata(pb);

    delete pb;
    return 0;
}