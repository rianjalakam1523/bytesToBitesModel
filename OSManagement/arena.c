#include "arena.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// AUTHOR: RIAN JALAKAM, FALL 2026

// Initialize the arena by grabbing a large chunk of memory upfront
Arena* arena_create(size_t capacity) {
    Arena *arena = (Arena*)malloc(sizeof(Arena));
    arena->capacity = capacity;
    arena->offset = 0;
    arena->buffer = (uint8_t*)malloc(capacity);
    
    if (!arena->buffer) {
        perror("Failed to allocate memory for arena");
        exit(1);
    }
    return arena;
}

void* arena_alloc(Arena *arena, size_t size) {
    // Align allocations to 8-byte boundaries for CPU efficiency
    size_t aligned_size = (size + 7) & ~7;
    
    if (arena->offset + aligned_size > arena->capacity) {
        return NULL; // Out of memory in this arena
    }
    
    // Grab the current pointer and advance the offset
    void *ptr = &arena->buffer[arena->offset];
    arena->offset += aligned_size;
    return ptr;
}

// Reset the entire arena
void arena_reset(Arena *arena) {
    arena->offset = 0;
}

// Clean Arena
void arena_free(Arena *arena) {
    free(arena->buffer);
    free(arena);
}

