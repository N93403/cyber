#include <stdio.h>
#include <stdlib.h> // Incluso per potenziali estensioni future

/**
 * @brief Controlla la password.
 * * Questa funzione contiene la logica che l'esecutore simbolico deve invertire.
 *
 * @param x L'input intero fornito dall'utente.
 */
void checkPass(int x)
{
    // Il vincolo logico: se l'input è uguale a un valore hardcoded.
    if(x == 7857)
    {
        // Questo output definisce il PATH DI SUCCESSO per Angr (il target 'find').
        printf("Access Granted");
    }
    else
    {
        // Questo output definisce il PATH DI FALLIMENTO (il target 'avoid').
        printf("Access Denied");
    }
}

int main(int argc, char *argv[])
{
    int x = 0;
    
    printf("Enter the password: ");
    
    // La funzione scanf è dove Angr introduce il valore simbolico (Symbolic Variable)
    // che deve essere risolto.
    if (scanf("%d", &x) != 1) {
        fprintf(stderr, "Errore nella lettura dell'input.\n");
        return 1;
    }

    checkPass(x);
    return 0;
}
