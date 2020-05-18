def mymax(iterable, key=lambda x: x):
    max_x = max_key = None

    for x in iterable:
        current_key = key(x)
        if max_key is None or current_key > max_key:
            max_x = x
            max_key = current_key

    return max_x


if __name__ == "__main__":
    maxint = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
    print("The max integer among the integers is:", maxint)
    maxchar = mymax("Suncana strana ulice")
    print("The biggest char among the chars:", maxchar)

    maxstring = mymax([
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"])
    print("The biggest string among the strings:", maxstring)

    D = {'burek': 8, 'buhtla': 5}
    print("The most expensive product in the bakery on the corner is:",
          mymax(D, D.get))

    maxperson = mymax(
        [("Josip", "Petrović"), ("Will", "Smith"), ("Julián", "Seco"), ("Angela", "Luque"), ("Mauricio", "Dengra"),
         ("Jose", "Fraga"), ("Marco", "Venegas"), ("Marcos", "Arnal"), ("Iván", "Japón"), ("Gerardo", "Moruga"),
         ("Enrique", "Barrueco"), ("Alfredo", "Muñoz"), ("Bárbara", "Palacio")])
    print("Who is a legend? -->", maxperson[0], maxperson[1])

"""
    "Find the most expensive product in Dictionary D containing
    the price list of the bakery on the corner of the street:
        D = {'burek': 8, 'buhtla': 5}
    To accomplish this task, pass the get dictionary method to D
    as a key. Explain how and why we can use the method as a
    free function."
    Functions are objects in Python that can be freely passed
    around. Python is very flexible in regards to functions.
    For example, one can change the definition of functions in
    runtime or even define entirely new functions in runtime
    and bind them to a class.
"""
