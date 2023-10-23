## Efficiency:

Our LRU cache using Python's OrderedDict is efficient:

- Time Efficiency: 'get' and 'set' operations are O(1) thanks to OrderedDict's quick reordering and eviction functions (move_to_end and popitem).

- Space Efficiency: The space complexity is O(N), directly related to the cache's capacity. It keeps memory usage in check.

## Code Design:

We chose OrderedDict for simplicity and performance:

- Simplicity and Clarity: OrderedDict manages order automatically, eliminating the need for manual management. It simplifies LRU logic and keeps the code clean.

- Native Library Advantage: We opted for Python's built-in libraries for reliability and optimization. They are well-tested, widely used, and offer robustness and efficiency.

