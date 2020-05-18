class A:
    def __init__(self):
        print("A constructor")
        self.virtual(123)

    def virtual(self, some_number):
        print("A-->" + str(some_number))


class B(A):
    def __init__(self, x):
        super().__init__()  # If super not called, base constructor won't be called at al
        # https://stackoverflow.com/questions/60015319/is-it-necessary-to-call-super-init-explicitly-in-python

        print("B constructor")
        self.virtual(123)

    def virtual(self, some_number):
        print("B-->" + str(some_number * 2))


class C(A):
    def __init__(self, x):
        # super().__init__()  # will raise an attribute error because self.x does not exist

        print("C constructor")
        self.x = x * 10000
        self.virtual(123)

        # .. but as python is flexible, one can just move the call to the base constructor to
        # an appropriate place. It is not necessary for it to be at the beginning of the function
        super().__init__()

    def virtual(self, some_number):
        print("B-->" + str(self.x + some_number))


if __name__ == '__main__':
    b = B(72)
    print()

    c = C(72)
