//
// Created by m43 on 22. 04. 2020..
//
#include <stdio.h>
#include <string.h>

int gt_int(const void *i1, const void *i2) {
    return *(int *) i1 > *(int *) i2 ? 1 : 0;
}

int gt_char(const void *c1, const void *c2) {
    return *(char *) c1 > *(char *) c2 ? 1 : 0;
}

int gt_str(const void *s1, const void *s2) {
    return strcmp(*(char **) s1, *(char **) s2) > 0 ? 1 : 0;
}

const void *mymax(
        const void *base, size_t nmemb, size_t size,
        int (*compar)(const void *, const void *)) {

    int index_of_max = 0;
    for (int i = 1; i < nmemb; i++) {
        if (compar(&base[index_of_max * size], &base[i * size]) != 1) {
            index_of_max = i;
        }
    }

    return &base[index_of_max * size];
}

int main() {
    int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    char arr_char[] = "Suncana strana ulice";
    const char *arr_str[] = {
            "Gle", "malu", "vocku", "poslije", "kise",
            "Puna", "je", "kapi", "pa", "ih", "njise"
    };

    int *max_int = mymax(arr_int, sizeof(arr_int) / sizeof(*arr_int), sizeof(int), gt_int);
    char *max_char = mymax(arr_char, sizeof(arr_char) / sizeof(*arr_char), sizeof(char), gt_char);
    char **max_str = mymax(arr_str, sizeof(arr_str) / sizeof(*arr_str), sizeof(char *), gt_str);

    printf("The max element of arr_int is: %d\n", *max_int);
    printf("The max element of arr_char is: %c\n", *max_char);
    printf("The max element of arr_str is: %s\n", *max_str);

    return 0;
}
