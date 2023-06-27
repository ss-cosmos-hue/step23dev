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
const int bin_num = 10;
my_heap_t my_heap_bins[10]; // bins[i] → i * 1000 <= size && size < (i + 1) * 1000
const int bin_size = 1000;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_print_free_list(my_metadata_t *heap_head)
{
  my_metadata_t *metadata = heap_head;
  int count = 0;
  while (metadata)
  {
    size_t size = metadata->size;
    printf("%d番目\tサイズ%ld\n", count, size);
    count++;
    metadata = metadata->next;
  }
}

void my_print_free_list_bin()
{
  for (size_t i = 0; i < bin_num; i++)
  {
    printf("bin サイズ範囲\t%ld~%ld\n", bin_size * i, bin_size * (i + 1) - 1);
    my_print_free_list(my_heap_bins[i].free_head);
  }
}

my_heap_t *size_to_bin(const size_t size)
{
  return &my_heap_bins[size / bin_size];
}

my_heap_t *metadata_to_bin(my_metadata_t *metadata)
{
  return size_to_bin(metadata->size);
}

void my_add_to_free_list(my_metadata_t *metadata)
{
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;
}

void my_add_to_free_list_bin(my_metadata_t *metadata)
{
  assert(!metadata->next);
  my_heap_t *bin = metadata_to_bin(metadata);
  metadata->next = bin->free_head;
  bin->free_head = metadata;
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev)
{
  printf("removing from free list size\t%ld\n", metadata->size);
  assert(metadata->size < bin_num * bin_size);
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

void my_remove_from_free_list_bin(my_metadata_t *metadata, my_metadata_t *prev)
{
  my_heap_t *bin = metadata_to_bin(metadata);
  if (prev)
  {
    prev->next = metadata->next;
  }
  else
  {
    bin->free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

void my_initialize_free_list_bin()
{
  for (int i = 0; i < bin_num; i++)
  {
    my_heap_bins[i].free_head = &my_heap_bins[i].dummy;
    my_heap_bins[i].dummy.size = 0;
    my_heap_bins[i].dummy.next = NULL;
  }
}

// This is called at the beginning of each challenge.
void my_initialize()
{
  my_initialize_free_list_bin();
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
/**
 * @brief レベル指定にあった空き領域を見つけて返す。
 */
my_metadata_pair_t customFit(const size_t size, my_metadata_t *metadata, my_metadata_t *prev, const int fit_level)
{
  const int kFirstFit = 0;
  const int kBestFit = 1;
  const int kWorstFit = 2;

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
  return new_cur_prev_metadata;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size)
{
  // Free list binがないときは、my_heapを用いる。
  // my_metadata_t *metadata;
  // my_metadata_t *prev = NULL;

  const int kBestFit = 1;

  // Free list binがあるときは、sizeごとに、適切なheapを選択する。
  // printf("start mallocing%ld\n", size);
  int bin_index = size / bin_size;
  my_heap_t bin = my_heap_bins[bin_index];
  my_metadata_t *metadata = bin.free_head;
  my_metadata_t *prev = NULL;
  bool is_found = false;
  for (int i = bin_index; i < bin_num; i++)
  {
    bin = my_heap_bins[i];
    // 今のbinに空き領域が一つも無ければ、次のbinを見る。
    if (bin.free_head->size == 0)
    {
      continue;
    }
    // 今のbinに少なくとも1つ空き領域があるならば、bestFitで空き領域を探す。
    metadata = bin.free_head;
    prev = NULL;
    my_metadata_pair_t cur_prev_metadata = customFit(size, metadata, prev, kBestFit);
    metadata = cur_prev_metadata.metadata;
    prev = cur_prev_metadata.prev;
    // 条件に合う空き領域が見つかれば、ループを抜け、そうでなければ次のbinを見る。
    if (metadata)
    {
      is_found = true;
      break;
    }
  }
  if (!is_found)
  {
    metadata = NULL;
    prev = NULL; // prevは、mallocがなされるまでは、使われないので、適当な値で良い。
  }

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
    my_add_to_free_list_bin(metadata);
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
  // Remove the free slot from the free list.
  my_remove_from_free_list_bin(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t))
  {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
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
    my_add_to_free_list_bin(new_metadata);
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
  my_add_to_free_list_bin(metadata);
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
  my_initialize();
  my_malloc(100);
  my_print_free_list_bin();
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
