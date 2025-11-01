# Nome del binario risultante che sarà analizzato da Angr
TARGET = simple

# File sorgente C
SOURCE = simple.c

# Compilatore C e flag
CC = gcc
# -Wall: Abilita tutti gli avvisi
# -m32: Compila il binario a 32-bit. Cruciale per la compatibilità con molte configurazioni di Angr
CFLAGS = -Wall -m32

# Target principale: 'make'
.PHONY: all
all: $(TARGET)

# Regola per la compilazione del target 'simple'
$(TARGET): $(SOURCE)
	@echo "Compilazione di $(TARGET)..."
	$(CC) $(SOURCE) -o $(TARGET) $(CFLAGS)
	@echo "Compilazione completata. Binario: $(TARGET)"

# Target per l'esecuzione di un test rapido
.PHONY: test
test: $(TARGET)
	@echo "\n--- Test Binario Fallimento (Input 1234) ---"
	@echo 1234 | ./$(TARGET) 
	@echo "\n--- Test Binario Successo (Input 7857) ---"
	@echo 7857 | ./$(TARGET)

# Target per la pulizia: 'make clean'
.PHONY: clean
clean:
	@echo "Pulizia file generati..."
	# Rimuove il binario e tutti i potenziali file oggetto
	rm -f $(TARGET) *.o
	@echo "Pulizia completata."
