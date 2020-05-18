cmake_minimum_required(VERSION 3.15 FATAL_ERROR)
project(fer_ooup C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -Wall -Wextra -ldl -rdynamic -Werror")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra") # -Werror

## LAB1
#add_executable(lab1-ex01 lab1/1.c)
#add_executable(lab1-ex02-01 lab1/2.cpp)
#add_executable(lab1-ex02-02 lab1/2.c)
#add_executable(lab1-ex03 lab1/3.cpp)
#add_executable(lab1-ex04 lab1/4.cpp)
#add_executable(lab1-ex05 lab1/5.cpp)
#add_executable(lab1-ex06 lab1/6.cpp)

## LAB2
#add_executable(lab2-ex00-procedural lab2/ex0/procedural.cpp)
#add_executable(lab2-ex00-oop lab2/ex0/oop.cpp)
#add_executable(lab2-ex01 lab2/ex1/mymax.c)
#add_executable(lab2-ex02 lab2/ex2/mymax.cpp)

## LAB3
## 1.1
# ./run.sh
add_executable(lab3-ex01-1 lab3/ex1-1/main.c lab3/ex1-1/myfactory.c)

