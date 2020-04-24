#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct UnaryFunction {
    void **vTable;
    int lower_bound;
    int upper_bound;
} UnaryFunction;

double value_at(UnaryFunction *uff, double x) {
    return ((double (*)()) uff->vTable[0])(uff, x);
}

double negative_value_at(UnaryFunction *uff, double x) {
    return ((double (*)()) uff->vTable[1])(uff, x);
}

double __unaryFunction__negative_value_at(UnaryFunction *uff, double x) {
    return -value_at(uff, x);
}

void tabulate(UnaryFunction *uff) {
    for (int x = uff->lower_bound; x <= uff->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, value_at(uff, x));
    }
};

_Bool same_functions_for_ints(UnaryFunction *f1, UnaryFunction *f2, double tolerance) {
    if (f1->lower_bound != f2->lower_bound) return false;
    if (f1->upper_bound != f2->upper_bound) return false;
    for (int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = value_at(f1, x) - value_at(f2, x);
        if (delta < 0) delta = -delta;
        if (delta > tolerance) return false;
    }
    return true;
}

void *_unaryFunction__vTable[2] = {NULL, __unaryFunction__negative_value_at};

void __unaryFunction__constructor(UnaryFunction *uff, int lb, int ub) {
    uff->vTable = _unaryFunction__vTable;
    uff->lower_bound = lb;
    uff->upper_bound = ub;
}

typedef struct Square {
    void **vTable;
    int lower_bound;
    int upper_bound;
} Square;

double __square__value_at(Square square, double x) {
    return x * x;
}

void *__square_vTable[2] = {__square__value_at, __unaryFunction__negative_value_at};

void __square__constructor(Square *square, int lb, int ub) {
    __unaryFunction__constructor((UnaryFunction *) square, lb, ub);
    square->vTable = __square_vTable;
}

Square *create_square(int lb, int ub) {
    Square *square = malloc(sizeof(Square));
    __square__constructor(square, lb, ub);
    return square;
}

typedef struct Linear {
    void **vTable;
    int lower_bound;
    int upper_bound;
    double a;
    double b;
} Linear;

double __linear__value_at(Linear *linear, double x) {
    return linear->a * x + linear->b;
}

void __linear__print_equation(Linear *linear) {
    printf("y = %.2fx + %.2f", linear->a, linear->b);
}

void print_equation(Linear *linear) {
    ((void (*)(Linear *)) linear->vTable[2])(linear);
}

void *__linear__vTable[3] = {__linear__value_at, __unaryFunction__negative_value_at, __linear__print_equation};

void __linear__constructor(Linear *linear, int lb, int ub, double a, double b) {
    __unaryFunction__constructor((UnaryFunction *) linear, lb, ub);
    linear->a = a;
    linear->b = b;
    linear->vTable = __linear__vTable;
}

Linear *create_linear(int lb, int ub, double a, double b) {
    Linear *linear = malloc(sizeof(Linear));
    __linear__constructor(linear, lb, ub, a, b);
    return linear;
}

int main(void) {

    UnaryFunction *f1 = create_square(-2, 2);
    tabulate(f1);

    UnaryFunction *f2 = create_linear(-2, 2, 5, -2);
    tabulate(f2);

    printf("f1==f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", negative_value_at(f2, 1.0));

    free(f1);
    free(f2);
    return 0;
}