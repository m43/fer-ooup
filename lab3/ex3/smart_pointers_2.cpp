#include <vector>
#include <iostream>
#include <memory>

using namespace std;

class Tiger {
public:
    Tiger(string name) : name_(name) { cout << "tiger " << name << " constructor" << endl; };

    ~Tiger() { cout << "tiger destructor" << endl; };

    const string &getName() const {
        return name_;
    }

private:
    string name_;
};

int main() {
    vector<shared_ptr<Tiger> > tigers;
    auto tiger = make_shared<Tiger>("Rikola");
    tigers.push_back(tiger); // AVOID: makes a copy of the shared pointer! now there are two owners of Rikola
    tigers.push_back(move(tiger)); // GOOD: moves the shared pointer into the vector. 'tiger' is no longer a owner
    // For more info: https://stackoverflow.com/questions/19334889/vector-of-shared-pointers-memory-problems-after-clearing-the-vector

    cout << "All done. Lets iterate over all tigers." << endl;

    for (const auto &t: tigers) {
        cout << t->getName() << endl;
    }

    tigers.clear();
    cout << "Tigers vector cleaned. All done." << endl;

    return 0;
}