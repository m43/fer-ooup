#ifndef FER_OOUP_MAARRAY_H
#define FER_OOUP_MAARRAY_H

template<class T, size_t N>
class MaArray {
private:
    size_t size{N};
    T values[N];

public:
    MaArray() = default;

    explicit MaArray(T init_value) {
        for (T &val: values) {
            val = init_value;
        }
    }


    void throwExceptionForInvalidIndex(int index) {
        if (!(index >= 0 && index < size)) {
            throw std::invalid_argument("Invalid index given.");
        }
    }


    void update(int index, T new_value) {
        throwExceptionForInvalidIndex(index);
        values[index] = new_value;
    }

    T get(int index) {
        throwExceptionForInvalidIndex(index);
        return values[index];
    }

    void fill(T value) {
        for (T &val: values) {
            val = value;
        }
    }

    size_t getSize() {
        return size;
    }

    void print() {
        print(std::cout);
    }

    void print(std::ostream &os) const {
        os << "[ ";
        for (T const &val: values) {
            // val = 300; // Compiler does not understand that this is forbidden and it does not get red or anything :(
            os << val << " ";
        }
        os << "]\n";
    }

    friend std::ostream &operator<<(std::ostream &os, const MaArray<T, N> &mar) {
        mar.print(os);
        return os;
    }

    T &operator[](int index) {
        return values[index];
    }// wait, how can i stop the changing of the variable when using a reference in the for loop?
};

#endif //FER_OOUP_MAARRAY_H
