//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t
{
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t
{
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

typedef struct my_metadata_pair_t
{
  my_metadata_t *metadata;
  my_metadata_t *prev;
} my_metadata_pair_t;
//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata)
{
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev)
{
  if (prev)
  {
    prev->next = metadata->next;
  }
  else
  {
    my_heap.free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize()
{
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}

/**
 * @brief metadataをfirst free slotの位置に更新する。prevはその一つ前のentryを指す。
 */
my_metadata_pair_t firstFit(const size_t size, my_metadata_t *metadata, my_metadata_t *prev)
{
  // First-fit: Find the first free slot the object fits.
  //  TODO: Update this logic to Best-fit!
  while (metadata && metadata->size < size)
  {
    prev = metadata;
    metadata = metadata->next;
  }
  // now, metadata points to the first free slot
  // and prev is the previous entry.
  // in case there is no free slot,
  // prev points to the final slot and metadata is NULL.
  my_metadata_pair_t cur_prev_metadata;
  cur_prev_metadata.metadata = metadata;
  cur_prev_metadata.prev = prev;
  return cur_prev_metadata;
}

/**
 * @brief metadataをfirst best slotの位置に更新する。prevはその一つ前のentryを指す。
 */
my_metadata_pair_t bestFit(const size_t size, my_metadata_t *metadata, my_metadata_t *prev)
{
  // Best-fit:
  // 暫定的な空き領域を初期化する。
  my_metadata_t *current_best_fit = NULL;
  my_metadata_t *current_best_fit_prev = NULL;
  while (metadata)
  {
    // 条件を満たす領域が初めて見つかった場合の操作をする。
    if ((!current_best_fit) && metadata->size >= size)
    {
      current_best_fit = metadata;
      current_best_fit_prev = prev;
    }
    // 少なくとも１つ、条件を満たす領域が見つかっているという条件の下で、
    // 要求されたsize以上かつ、暫定的な最善の空き領域より小さい空き領域が見つかった場合の操作をする。
    if (current_best_fit && metadata->size >= size && metadata->size < current_best_fit->size)
    {
      // 暫定的な最善の空き領域を更新する。
      current_best_fit = metadata;
      current_best_fit_prev = prev;
    }
    // 次の領域を見る。
    prev = metadata;
    metadata = metadata->next;
  }

  if (current_best_fit)
  {
    metadata = current_best_fit;
    prev = current_best_fit_prev;
    // now, metadata points to the best free slot
    // and prev is the previous entry.
  }
  else
  {
    metadata = current_best_fit;
    // in case there is no free slot,
    // prev points to the final slot and metadata is NULL.
  }
  my_metadata_pair_t cur_prev_metadata;
  cur_prev_metadata.metadata = metadata;
  cur_prev_metadata.prev = prev;
  return cur_prev_metadata;
}

/**
 * @brief metadataをworst slotの位置に更新する。prevはその一つ前のentryを指す。
 */
my_metadata_pair_t worstFit(const size_t size, my_metadata_t *metadata, my_metadata_t *prev)
{
  // Worst-fit:
  // 暫定的な空き領域を初期化する。
  my_metadata_t *current_worst_fit = NULL;
  my_metadata_t *current_worst_fit_prev = NULL;
  while (metadata)
  {
    // 条件を満たす領域が初めて見つかった場合の操作をする。
    if ((!current_worst_fit) && metadata->size >= size)
    {
      current_worst_fit = metadata;
      current_worst_fit = prev;
    }
    // 少なくとも１つ、条件を満たす領域が見つかっているという条件の下で、
    // 要求されたsize以上かつ、暫定的な最善の空き領域より小さい空き領域が見つかった場合の操作をする。
    if (current_worst_fit && metadata->size >= size && metadata->size > current_worst_fit->size)
    {
      // 暫定的な最善の空き領域を更新する。
      current_worst_fit = metadata;
      current_worst_fit_prev = prev;
    }
    // 次の領域を見る。
    prev = metadata;
    metadata = metadata->next;
  }

  if (current_worst_fit)
  {
    metadata = current_worst_fit;
    prev = current_worst_fit_prev;
    // now, metadata points to the worst free slot
    // and prev is the previous entry.
  }
  else
  {
    metadata = current_worst_fit;
    // in case there is no free slot,
    // prev points to the final slot and metadata is NULL.
  }
  my_metadata_pair_t cur_prev_metadata;
  cur_prev_metadata.metadata = metadata;
  cur_prev_metadata.prev = prev;
  return cur_prev_metadata;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size)
{
  // Free list binの実装をする
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;

  const int kFirstFit = 0;
  const int kBestFit = 1;
  const int kWorstFit = 2;

  const int fit_level = kWorstFit;

  my_metadata_pair_t new_cur_prev_metadata;
  if (fit_level == kFirstFit)
  {
    new_cur_prev_metadata = firstFit(size, metadata, prev);
  }
  else if (fit_level == kBestFit)
  {
    new_cur_prev_metadata = bestFit(size, metadata, prev);
  }
  else if (fit_level == kWorstFit)
  {
    new_cur_prev_metadata = worstFit(size, metadata, prev);
  }
  else
  {
    new_cur_prev_metadata = firstFit(size, metadata, prev);
  }
  metadata = new_cur_prev_metadata.metadata;
  prev = new_cur_prev_metadata.prev;

  if (!metadata)
  {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  metadata->size = size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t))
  {
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr)
{
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize()
{
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test()
{
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
