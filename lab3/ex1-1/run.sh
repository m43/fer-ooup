gcc -rdynamic -o lab3-ex01.out main.c myfactory.c -ldl
gcc -shared -fPIC tiger.c -o tiger.so
gcc -shared -fPIC parrot.c -o parrot.so
./lab3-ex01.out ./tiger.so ./parrot.so