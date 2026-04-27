#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
long long comparacoes = 0;
long long trocas      = 0;
 
static int selection_sort(int *arr, int n)
{
    for (int i = 0; i < n - 1; i++) {
        int idx_min = i;
 
        for (int j = i + 1; j < n; j++) {
            comparacoes++;
            if (arr[j] < arr[idx_min])
                idx_min = j;
        }
 
        if (idx_min != i) {
            int tmp      = arr[idx_min];
            arr[idx_min] = arr[i];
            arr[i]       = tmp;
            trocas++;
        }
    }
    return 0;
}
 
/* Leitura rapida: carrega o arquivo inteiro em memoria de uma vez
   e faz o parsing manual — evita o overhead do fscanf por chamada */
static int fast_read_ints(const char *path, int *a, int capacity)
{
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
 
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    rewind(f);
 
    char *buf = (char *)malloc(fsize + 1);
    if (!buf) { fclose(f); return -1; }
 
    if (fread(buf, 1, fsize, f) != (size_t)fsize) { free(buf); fclose(f); return -1; }
    fclose(f);
    buf[fsize] = '\0';
 
    int n = 0;
    char *p   = buf;
    char *end = buf + fsize;
 
    while (p < end && n < capacity) {
        while (p < end && (*p < '0' || *p > '9') && *p != '-') p++;
        if (p >= end) break;
 
        int sign = 1;
        if (*p == '-') { sign = -1; p++; }
 
        int val = 0;
        while (p < end && *p >= '0' && *p <= '9')
            val = val * 10 + (*p++ - '0');
 
        a[n++] = sign * val;
    }
 
    free(buf);
    return n;
}
 
int main(int argc, char *argv[])
{
    if (argc < 2) return 1;
 
    int capacity = 10000000;
    int *a = (int *)malloc(capacity * sizeof(int));
    if (!a) return 1;
 
    int n = fast_read_ints(argv[1], a, capacity);
    if (n <= 0) { free(a); return 1; }
    
    struct timespec t0, t1;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t0);
    selection_sort(a, n);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t1);
 
    double cpu_time_used = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
 
    printf("RESULTADO|Algoritmo:SelectionSort|N:%d|Comparacoes:%lld|Trocas:%lld|Tempo:%.6f\n",
           n, comparacoes, trocas, cpu_time_used);
 
    free(a);
    return 0;
}
 
