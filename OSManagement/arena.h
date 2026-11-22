#ifndef ARENA_H
#define ARENA_H

// AUTHOR: RIAN JALAKAM, FALL 2026

#include <stddef.h>
#include <stdint.h>

typedef struct {
    size_t capacity;
    size_t offset;
    uint8_t *buffer;
} Arena;

Arena* arena_create(size_t capacity);
void* arena_alloc(Arena *arena, size_t size);
void arena_reset(Arena *arena);
void arena_free(Arena *arena);

#endif
