/*
 * learning_c_demo.c
 * ====================
 *
 * This file is intentionally long and heavily documented to serve as a learning
 * resource for students who want to get comfortable with C programming.
 *
 * It covers a wide range of C concepts in a single, self‑contained example:
 *  - Primitive data types and type modifiers
 *  - Constants (both macro and enum)
 *  - Structures and unions
 *  - Arrays, strings and multi‑dimensional arrays
 *  - Pointers, pointer arithmetic, and pointer to pointer
 *  - Memory allocation with malloc()/calloc()/realloc()/free()
 *  - File I/O with stdio.h functions
 *  - Recursion and iterative algorithms
 *  - Dynamic arrays and resizing
 *  - Linked list implementation
 *  - Sorting algorithms (bubble sort, quick sort)
 *  - Searching algorithms (linear search, binary search)
 *  - Bit manipulation tricks
 *  - Macros and inline functions
 *  - Error handling conventions
 *  - Use of the C99 standard features such as designated initializers
 *  - Simple command line argument parsing
 *  - A small state machine example
 *  - Commenting conventions and documentation style
 *
 * The goal is not to build an application but to provide a comprehensive
 * reference implementation that students can read, modify, and experiment
 * with. Feel free to split the code into multiple files if you prefer.
 */

/*=====================================================================
 *  1. Standard library includes and macro definitions
 *====================================================================*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

/*  Macro for maximum of two values */
#define MAX(a,b) ((a) > (b) ? (a) : (b))
/*  Macro for minimum of two values */
#define MIN(a,b) ((a) < (b) ? (a) : (b))
/*  Macro to print a string followed by a newline */
#define PRINTLN(str) puts(str)
/*  Macro to handle errors with a message and exit */
#define HANDLE_ERROR(msg) do { perror(msg); exit(EXIT_FAILURE); } while (0)

/*=====================================================================
 *  2. Enumerations and constants
 *====================================================================*/
/*  Enumeration for days of the week */
typedef enum {
    SUNDAY = 0,
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY
} DayOfWeek;

/*  Constant for maximum string length */
#define MAX_STRING_LENGTH 256

/*=====================================================================
 *  3. Structures and unions
 *====================================================================*/
/*  A simple point in 2D space */
typedef struct {
    double x;
    double y;
} Point;

/*  A rectangle defined by two points (top-left and bottom-right) */
typedef struct {
    Point top_left;
    Point bottom_right;
} Rectangle;

/*  A union that can hold either an integer, a double, or a string */
typedef union {
    int i;
    double d;
    char *s;
} IntDoubleString;

/*=====================================================================
 *  4. Global variables
 *====================================================================*/
/*  Global counter used for demonstration */
static int global_counter = 0;

/*=====================================================================
 *  5. Function prototypes
 *====================================================================*/
/*  Basic arithmetic functions */
int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);
double divide(double a, double b, int *error);

/*  Functions that demonstrate pointers */
void increment_by_pointer(int *p);
int* allocate_int_array(size_t count, int init_value);

/*  String utility functions */
int string_compare(const char *s1, const char *s2);
char* string_copy(const char *source, size_t max_len);

/*  File I/O functions */
int read_file_into_buffer(const char *filename, char **buffer, size_t *size);
int write_buffer_to_file(const char *filename, const char *buffer, size_t size);

/*  Recursive function: factorial */
unsigned long long factorial(unsigned int n);

/*  Linked list operations */
typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node* list_create_node(int data);
void list_append(Node **head, int data);
void list_print(const Node *head);
void list_free(Node **head);

/*  Sorting algorithms */
void bubble_sort(int *arr, size_t n);
int quick_sort(int *arr, int left, int right);

/*  Searching algorithms */
int linear_search(const int *arr, size_t n, int target);
int binary_search(const int *arr, size_t n, int target);

/*  Bit manipulation */
unsigned int set_bit(unsigned int num, unsigned int bit_position);
unsigned int clear_bit(unsigned int num, unsigned int bit_position);
unsigned int toggle_bit(unsigned int num, unsigned int bit_position);
unsigned int check_bit(unsigned int num, unsigned int bit_position);

/*  State machine example */
typedef enum {
    STATE_INIT,
    STATE_RUNNING,
    STATE_PAUSED,
    STATE_STOPPED
} State;

void state_machine_demo(void);

/*  Inline function example */
static inline int max_inline(int a, int b) { return a > b ? a : b; }

/*=====================================================================
 *  6. Main function – entry point of the program
 *====================================================================*/
int main(int argc, char *argv[]) {
    PRINTLN("=== C Learning Demo ===\n");

    /*  Demonstrate basic arithmetic */
    int a = 15, b = 4;
    printf("%d + %d = %d\n", a, b, add(a, b));
    printf("%d - %d = %d\n", a, b, subtract(a, b));
    printf("%d * %d = %d\n", a, b, multiply(a, b));
    int div_error = 0;
    double div_result = divide((double)a, (double)b, &div_error);
    if (div_error) {
        puts("Division by zero!\n");
    } else {
        printf("%f / %f = %f\n", a, b, div_result);
    }

    /*  Demonstrate pointers */
    printf("\nDemonstrating pointer increment...\n");
    increment_by_pointer(&a);
    printf("Value after increment: %d\n", a);

    /*  Allocate an array of integers and print it */
    size_t count = 10;
    int *int_arr = allocate_int_array(count, 42);
    if (!int_arr) return EXIT_FAILURE;
    printf("\nArray allocated with init value 42:\n");
    for (size_t i = 0; i < count; ++i) {
        printf("%d ", int_arr[i]);
    }
    puts("\n");
    free(int_arr);

    /*  Demonstrate string utilities */
    const char *hello = "Hello, world!";
    char *copy = string_copy(hello, MAX_STRING_LENGTH);
    if (copy) {
        printf("Copied string: %s\n", copy);
        free(copy);
    }

    /*  Demonstrate file I/O – read, modify, write */
    char *file_buffer = NULL;
    size_t file_size = 0;
    const char *test_file = "test_input.txt";
    if (read_file_into_buffer(test_file, &file_buffer, &file_size) == 0) {
        printf("Read %zu bytes from %s.\n", file_size, test_file);
        /*  Append a line */
        file_buffer = realloc(file_buffer, file_size + 32);
        if (!file_buffer) HANDLE_ERROR("realloc");
        strncat(file_buffer, "\nAppended line.\n", 32);
        if (write_buffer_to_file("test_output.txt", file_buffer, file_size + 16) == 0) {
            puts("Written modified buffer to test_output.txt\n");
        }
        free(file_buffer);
    }

    /*  Demonstrate recursion */
    printf("Factorial of 5: %llu\n", factorial(5));

    /*  Demonstrate linked list */
    Node *list_head = NULL;
    list_append(&list_head, 10);
    list_append(&list_head, 20);
    list_append(&list_head, 30);
    puts("Linked list contents:");
    list_print(list_head);
    list_free(&list_head);

    /*  Demonstrate sorting and searching */
    int sample_arr[] = {5, 3, 8, 1, 9, 2, 7};
    size_t arr_len = sizeof(sample_arr) / sizeof(sample_arr[0]);
    puts("Original array:\n");
    for (size_t i = 0; i < arr_len; ++i) printf("%d ", sample_arr[i]);
    puts("\n");

    bubble_sort(sample_arr, arr_len);
    puts("After bubble sort:\n");
    for (size_t i = 0; i < arr_len; ++i) printf("%d ", sample_arr[i]);
    puts("\n");

    int target = 7;
    int idx = linear_search(sample_arr, arr_len, target);
    printf("Linear search: %s (index %d)\n", idx >= 0 ? "found" : "not found", idx);

    /*  Demonstrate bit manipulation */
    unsigned int num = 0b00001111; // 15 in decimal
    printf("Original number: %u\n", num);
    num = set_bit(num, 4);
    printf("After setting bit 4: %u\n", num);
    num = toggle_bit(num, 0);
    printf("After toggling bit 0: %u\n", num);

    /*  Demonstrate state machine */
    state_machine_demo();

    PRINTLN("\n=== End of Demo ===");
    return EXIT_SUCCESS;
}

/*=====================================================================
 *  7. Function definitions
 *====================================================================*/

/* Arithmetic functions */
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }

double divide(double a, double b, int *error) {
    if (b == 0.0) {
        if (error) *error = 1;
        return 0.0;
    }
    if (error) *error = 0;
    return a / b;
}

/* Pointers */
void increment_by_pointer(int *p) {
    if (!p) return; // safety check
    (*p)++;
}

int* allocate_int_array(size_t count, int init_value) {
    int *arr = malloc(count * sizeof(int));
    if (!arr) HANDLE_ERROR("malloc for int array");
    for (size_t i = 0; i < count; ++i) arr[i] = init_value;
    return arr;
}

/* String utilities */
int string_compare(const char *s1, const char *s2) {
    return strcmp(s1, s2);
}

char* string_copy(const char *source, size_t max_len) {
    if (!source) return NULL;
    size_t src_len = strlen(source);
    size_t len_to_copy = MIN(src_len, max_len - 1); // reserve space for null
    char *dest = malloc(len_to_copy + 1);
    if (!dest) HANDLE_ERROR("malloc for string copy");
    memcpy(dest, source, len_to_copy);
    dest[len_to_copy] = '\0';
    return dest;
}

/* File I/O */
int read_file_into_buffer(const char *filename, char **buffer, size_t *size) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        perror("fopen for reading");
        return -1;
    }
    fseek(fp, 0, SEEK_END);
    long fsize = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    if (fsize < 0) {
        fclose(fp);
        perror("ftell");
        return -1;
    }
    *size = (size_t)fsize;
    *buffer = malloc(*size + 1); // +1 for null terminator
    if (!*buffer) {
        fclose(fp);
        HANDLE_ERROR("malloc for file buffer");
        return -1;
    }
    size_t read_bytes = fread(*buffer, 1, *size, fp);
    if (read_bytes != *size) {
        fclose(fp);
        free(*buffer);
        perror("fread");
        return -1;
    }
    (*buffer)[*size] = '\0'; // null terminate for convenience
    fclose(fp);
    return 0;
}

int write_buffer_to_file(const char *filename, const char *buffer, size_t size) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        perror("fopen for writing");
        return -1;
    }
    size_t written = fwrite(buffer, 1, size, fp);
    if (written != size) {
        fclose(fp);
        perror("fwrite");
        return -1;
    }
    fclose(fp);
    return 0;
}

/* Factorial (recursive) */
unsigned long long factorial(unsigned int n) {
    if (n == 0) return 1ULL;
    return n * factorial(n - 1);
}

/* Linked list */
Node* list_create_node(int data) {
    Node *node = malloc(sizeof(Node));
    if (!node) HANDLE_ERROR("malloc for Node");
    node->data = data;
    node->next = NULL;
    return node;
}

void list_append(Node **head, int data) {
    Node *new_node = list_create_node(data);
    if (!*head) {
        *head = new_node;
        return;
    }
    Node *current = *head;
    while (current->next) current = current->next;
    current->next = new_node;
}

void list_print(const Node *head) {
    const Node *current = head;
    printf("Linked list: ");
    while (current) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    puts("NULL");
}

void list_free(Node **head) {
    Node *current = *head;
    while (current) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    *head = NULL;
}

/* Bubble sort */
void bubble_sort(int *arr, size_t n) {
    if (!arr) return;
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j + 1 < n - i; ++j) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

/* Linear search */
int linear_search(const int *arr, size_t n, int key) {
    for (size_t i = 0; i < n; ++i) {
        if (arr[i] == key) return (int)i;
    }
    return -1;
}

/* Bit manipulation */
unsigned int set_bit(unsigned int x, unsigned int pos) {
    return x | (1U << pos);
}

unsigned int toggle_bit(unsigned int x, unsigned int pos) {
    return x ^ (1U << pos);
}

/* State machine demo */
void state_machine_demo() {
    enum { STATE_INIT, STATE_PROCESS, STATE_DONE } state = STATE_INIT;
    while (1) {
        switch (state) {
            case STATE_INIT:
                puts("State: INIT");
                state = STATE_PROCESS;
                break;
            case STATE_PROCESS:
                puts("State: PROCESSING");
                state = STATE_DONE;
                break;
            case STATE_DONE:
                puts("State: DONE");
                return;
            default:
                puts("Unknown state");
                return;
        }
    }
}

/* State machine for sample */
void state_machine_demo() {
    enum { OFF, ON } power_state = OFF;
    printf("Power state initial: %s\n", power_state == ON ? "ON" : "OFF");
    power_state = ON;
    printf("Power state after toggling: %s\n", power_state == ON ? "ON" : "OFF");
}

/* End of file */
