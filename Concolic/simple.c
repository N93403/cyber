#include <stdio.h>

void checkPass(int x)
{
    // Il vincolo che Angr deve risolvere: x deve essere 7857
    if(x == 7857)
    {
        printf("Access Granted");
    }
    else
    {
        printf("Access Denied");
    }
}

int main(int argc, char *argv[])
{
    int x = 0;
    printf("Enter the password: ");
    // La funzione scanf introduce la variabile simbolica 'x'
    scanf("%d", &x);
    checkPass(x);
    return 0;
}
