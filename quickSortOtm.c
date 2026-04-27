#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define INSERTION_THRESHOLD 16

static inline void swap(long long *a, long long *b) {
    long long t = *a; *a = *b; *b = t;
}

static void insertion_sort(long long *arr, int lo, int hi) {
    for (int i = lo + 1; i <= hi; i++) {
        long long key = arr[i];
        int j = i - 1;
        while (j >= lo && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

static void dual_pivot_qsort(long long *arr, int lo, int hi) {
    while (hi - lo >= INSERTION_THRESHOLD) {
        int len = hi - lo;
        int m1  = lo + len / 4;
        int mid = lo + len / 2;
        int m3  = lo + 3 * len / 4;

        if (arr[lo] > arr[m1])  swap(&arr[lo],  &arr[m1]);
        if (arr[m3] > arr[hi])  swap(&arr[m3],  &arr[hi]);
        if (arr[lo] > arr[mid]) swap(&arr[lo],  &arr[mid]);
        if (arr[m1] > arr[mid]) swap(&arr[m1],  &arr[mid]);
        if (arr[lo] > arr[m3])  swap(&arr[lo],  &arr[m3]);
        if (arr[mid] > arr[m3]) swap(&arr[mid], &arr[m3]);
        if (arr[m1] > arr[hi])  swap(&arr[m1],  &arr[hi]);
        if (arr[m3] > arr[hi])  swap(&arr[m3],  &arr[hi]);
        if (arr[m1] > arr[mid]) swap(&arr[m1],  &arr[mid]);

        swap(&arr[m1], &arr[lo]);
        swap(&arr[m3], &arr[hi]);

        long long p1 = arr[lo], p2 = arr[hi];

        int lt = lo + 1, gt = hi - 1, k = lt;
        while (k <= gt) {
            if (arr[k] < p1) {
                swap(&arr[k], &arr[lt]);
                lt++; k++;
            } else if (arr[k] > p2) {
                swap(&arr[k], &arr[gt]);
                gt--;
            } else {
                k++;
            }
        }

        lt--; gt++;
        swap(&arr[lo], &arr[lt]);
        swap(&arr[hi], &arr[gt]);

        int left_size  = lt - 1 - lo;
        int right_size = hi - gt - 1;

        if (left_size <= right_size) {
            dual_pivot_qsort(arr, lo, lt - 1);
            dual_pivot_qsort(arr, lt + 1, gt - 1);
            lo = gt + 1;
        } else {
            dual_pivot_qsort(arr, lt + 1, gt - 1);
            dual_pivot_qsort(arr, gt + 1, hi);
            hi = lt - 1;
        }
    }
    if (lo < hi)
        insertion_sort(arr, lo, hi);
}

static long long *read_file(const char *path, size_t *out_n) {
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); return NULL; }

    size_t cap = 1024, n = 0;
    long long *arr = malloc(cap * sizeof(long long));
    if (!arr) { fclose(f); return NULL; }

    char line[64];
    while (fgets(line, sizeof(line), f)) {
        char *end;
        long long v = strtoll(line, &end, 10);
        if (end == line) continue;
        if (n == cap) {
            cap *= 2;
            long long *tmp = realloc(arr, cap * sizeof(long long));
            if (!tmp) { free(arr); fclose(f); return NULL; }
            arr = tmp;
        }
        arr[n++] = v;
    }
    fclose(f);
    *out_n = n;
    return arr;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Uso: %s <arquivo1> [arquivo2 ...]\n", argv[0]);
        return 1;
    }

    for (int i = 1; i < argc; i++) {
        size_t n = 0;
        long long *arr = read_file(argv[i], &n);
        if (!arr) continue;

        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);

        if (n > 1)
            dual_pivot_qsort(arr, 0, (int)(n - 1));

        clock_gettime(CLOCK_MONOTONIC, &t1);

        double ms = (t1.tv_sec - t0.tv_sec) * 1000.0
                  + (t1.tv_nsec - t0.tv_nsec) / 1e6;

        printf("%.3f ms\n", ms);

        free(arr);
    }
    return 0;
}