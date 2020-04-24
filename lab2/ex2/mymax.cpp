//
// Created by m43 on 22. 04. 2020..
//

#include <iostream>
#include <string>
#include <vector>
#include <set>

using namespace std;

template<typename Iterator, typename Predicate>
Iterator mymax(
        Iterator first, Iterator last, Predicate pred) {

    Iterator max_iterator = first;
    while (first != last) {
        if (pred(*max_iterator, *first) != 1) {
            max_iterator = first;
        }
        first++;
    }

    return max_iterator;
}

int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 72};
const string arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
};
vector<string> str_vector(arr_str, arr_str + sizeof(arr_str) / sizeof(char *));
set<string> str_set(arr_str, arr_str + sizeof(arr_str) / sizeof(char *));

int main() {
    // C++ is smart so "mymax<int *, int (*)(int&,int&)>(...)" becomes "mymax(...)"
    const int *maxint = mymax(
            &arr_int[0],
            &arr_int[sizeof(arr_int) / sizeof(*arr_int)],
            [](int &x, int &y) { return x > y ? 1 : 0; }
    );
    cout << "Max integer is " << *maxint << "\n";

    auto max_arr = mymax(
            &arr_str[0],
            &arr_str[sizeof(arr_str) / sizeof(*arr_str)],
            [](const string &x, const string &y) { return x.compare(y) > 0 ? 1 : 0; }
    );
    cout << "Max string in array is " << *max_arr << "\n";


    auto max_vec = mymax(
            str_vector.begin(),
            str_vector.end(),
            [](auto &x, auto &y) { return x.compare(y) > 0 ? 1 : 0; }
    );
    cout << "Max string in vector is " << *max_vec << "\n";

    auto max_set = mymax(
            str_set.begin(),
            str_set.end(),
            [](auto x, auto y) { return x.compare(y) > 0 ? 1 : 0; }
    );
    cout << "Max string in set is " << *max_set << "\n";

    return 0;
}

/*

 "Comment on the advantages and disadvantages of this implementation over the implementation from the previous task"
    In the previous task the solution was not as flexible as it is here. In this solution, mymax can accept any data
    structure for which some kind of iterator can be defined: bare arrays (though one needs to construct the iterator
    manually), std::vector, std::set etc.

 */