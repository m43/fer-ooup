cmake_minimum_required(VERSION 3.15 FATAL_ERROR)
project(fer_ooup C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra ") # -Werror

add_executable(lab1-ex01 lab1/1.c)
add_executable(lab1-ex02-01 lab1/2.cpp)
add_executable(lab1-ex02-02 lab1/2.c)
add_executable(lab1-ex03 lab1/3.cpp)
add_executable(lab1-ex04 lab1/4.cpp)
add_executable(lab1-ex05 lab1/5.cpp)
add_executable(lab1-ex06 lab1/6.cpp)
