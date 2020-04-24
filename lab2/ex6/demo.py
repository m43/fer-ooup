from ex6.sheet import Sheet

if __name__ == "__main__":
    s = Sheet(5, 5)
    print()

    s.set('A1', '2')
    s.set('A2', '5')
    s.set('A3', 'A1+A2')
    s.prettyPrint()
    print()

    s.set('A1', '4')
    s.set('A4', 'A1+A3')
    s.prettyPrint()
    print()

    try:
        s.set('A1', 'A3')
    except ValueError as e:
        print("Caught exception:", e)
    s.set('A5', "A1+A2+A3")
    s.set("A1", "3")
    s.set('B1', "A1+A2+A3+A4+A5")
    s.prettyPrint()
    print()
