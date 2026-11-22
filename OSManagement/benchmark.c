#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "arena.h"

#define NUM_ALLOCATIONS 100000
#define ALLOC_SIZE 64 // Simulated tensor chunk or pixel buffer size

// Helper to get high-resolution time in milliseconds
double get_time_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (ts.tv_sec * 1000.0) + (ts.tv_nsec / 1000000.0);
}

int main() {
    printf("=== Memory Allocator Benchmark (%d iterations) ===\n", NUM_ALLOCATIONS);

    // ----------------------------------------------------
    // 1. Benchmark Standard malloc / free
    // ----------------------------------------------------
    double start_malloc = get_time_ms();

    void *ptrs[NUM_ALLOCATIONS];
    for (int i = 0; i < NUM_ALLOCATIONS; i++) {
        ptrs[i] = malloc(ALLOC_SIZE);
        if (!ptrs[i]) {
            perror("malloc failed");
            return 1;
        }
    }
    for (int i = 0; i < NUM_ALLOCATIONS; i++) {
        free(ptrs[i]);
    }

    double end_malloc = get_time_ms();
    double malloc_time = end_malloc - start_malloc;
    printf("[Standard Malloc] Time taken: %.3f ms\n", malloc_time);

    // ----------------------------------------------------
    // 2. Benchmark Arena Allocator (Bump Allocation & Bulk Reset)
    // ----------------------------------------------------
    // Pre-allocate enough space for all allocations combined
    size_t arena_capacity = NUM_ALLOCATIONS * (ALLOC_SIZE + 8); // Account for alignment
    Arena *arena = arena_create(arena_capacity);
    if (!arena) {
        fprintf(stderr, "Failed to create arena\n");
        return 1;
    }

    double start_arena = get_time_ms();

    // Allocate 100,000 times sequentially
    for (int i = 0; i < NUM_ALLOCATIONS; i++) {
        void *p = arena_alloc(arena, ALLOC_SIZE);
        if (!p) {
            fprintf(stderr, "Arena out of memory at index %d\n", i);
            break;
        }
    }

    // Bulk reset instead of 100,000 individual free() calls
    arena_reset(arena);

    double end_arena = get_time_ms();
    double arena_time = end_arena - start_arena;
    printf("[Arena Allocator] Time taken: %.3f ms\n", arena_time);

    // Calculate speedup factor
    if (arena_time > 0) {
        printf("[Performance] Arena is approximately %.1fx faster than malloc/free.\n", malloc_time / arena_time);
    }

    // Clean up arena memory block
    arena_free(arena);
    return 0;
}
