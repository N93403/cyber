#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void vulnerable_function(char *input) {
    char buffer[100];
    strcpy(buffer, input); // Buffer overflow vulnerability
    printf("Input processed: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <input>\n", argv[0]);
        return 1;
    }
    
    vulnerable_function(argv[1]);
    return 0;
}
