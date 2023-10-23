## Code Design:

Active Directory management leverages intuitive structuring and systematic search capabilities through:

- **`Group` Class Implementation:** Mimicking real-world organizational hierarchies, this design simplifies the containment of users and subgroups. It's a direct, natural representation that promotes organized data handling.

- **Recursive Searching:** Chosen for its inherent ability to navigate through deeply nested structures, the recursive function systematically locates users across varying group levels without complexity constraints.

## Efficiency:

The approach harbors specific efficiency implications:

- **Time Complexity:** The search functionality, recursive in nature, can escalate to O(n) time complexity, especially evident when traversing extensive user groups or deeply nested subgroups, directly influencing operation duration.

- **Space Complexity:** The stack space corresponds to the depth of recursive calls, significant in deep searches. This space demand, though manageable in standard applications, might stress larger, more complex directory structures.

These design choices reflect a preference for conceptual clarity and ease of implementation, with a mindful acceptance of the trade-offs in large-scale efficiency.
