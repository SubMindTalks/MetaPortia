| Category        | Verb        | Github Usage (approx.) | Definition                                                              | Synonyms to Avoid |
|-----------------|-------------|-------------------------|--------------------------------------------------------------------------|-------------------|
| **Alteration**  | `set`       | 2B                     | Put data in an existing resource (e.g., object attribute)                |                   |
|                 | `change`    | 668M                    | Replace a whole thing (e.g., image)                                     | `edit`           |
|                 | `edit`      | 325M                    | Similar to `change`, often for view rendering                           | `change`        |
|                 | `update`    | 739M                    | Update components, possibly adding new ones                              |                   |
|                 | `add`       | 1B                     | Add something to a group                                                  | `append`, `insert` |
|                 | `append`    | 287M                    | Similar to `add`, often creates a new group without modifying the original | `add`, `insert`  |
|                 | `insert`    | ~                    | Add something to a group at a specific position/index.                   | `add`, `append`, `push` |
|                 | `remove`    | 824M                    | Remove something from a group                                             | `delete`, `erase`, `clear` |
|                 | `delete`    | 455M                    | Similar to `remove`, may imply non-recoverable deletion                 | `remove`, `erase`, `clear` |
|                 | `erase`     | ~                    | Remove something from a group, often implying a specific element or range. | `remove`, `delete`, `clear` |
|                 | `clear`     | ~                    | Remove all elements from a group/container.                             | `remove`, `delete`, `erase` |
|                 | `save`      | 478M                    | Preserve data to avoid loss                                               | `store`, `persist`, `write` |
|                 | `store`     | 396M                    | Similar to `save`                                                        | `save`, `persist`, `write` |
|                 | `persist`   | ~                    | Similar to `save`, often implying more permanent storage (e.g. database). | `save`, `store`, `write` |
|                 | `write`     | ~                    | Write data to a destination/output.  Often used with files or streams. | `save`, `store`, `persist` |
|                 | `disable`   | 586M                    | Make a resource unavailable/inactive                                     | `hide`, `deactivate` |
|                 | `hide`      | 237M                    | Similar to `disable`, but by hiding                                     | `disable`, `deactivate` |
|                 | `deactivate`| ~                    | Make a resource unavailable/inactive                                     | `disable`, `hide` |
|                 | `split`     | 276M                    | Separate parts of a resource                                            | `separate`, `divide`, `partition` |
|                 | `separate` | 151M                    | Similar to `split`                                                       | `split`, `divide`, `partition` |
|                 | `divide`    | ~                    | Similar to `split`, often implying equal parts.                           | `split`, `separate`, `partition` |
|                 | `partition` | ~                    | Similar to `split`, often implying dividing into distinct sections.       | `split`, `separate`, `divide` |
|                 | `merge`     | 312M                    | Combine multiple resources into one                                       | `join`, `combine`, `concatenate` |
|                 | `join`      | 220M                    | Similar to `merge`                                                       | `merge`, `combine`, `concatenate` |
|                 | `combine`   | ~                    | Similar to `merge`.                                                     | `merge`, `join`, `concatenate` |
|                 | `concatenate` | ~                 | Similar to `merge`, specifically for joining strings or sequences.      | `merge`, `join`, `combine` |
| **Creation**   | `create`    | 1B                     | Create a resource                                                       | `make`, `generate`, `build`, `construct` |
|                 | `make`      | 797M                    | Similar to `create`                                                       | `create`, `generate`, `build`, `construct` |
|                 | `generate` | 286M                    | Similar to `create`                                                       | `create`, `make`, `build`, `construct` |
|                 | `build`     | ~                    |  Similar to `create`, often implying a more complex process.             | `create`, `make`, `generate`, `construct` |
|                 | `construct` | ~                    | Similar to `create`, implying deliberate creation/assembly.             | `create`, `make`, `generate`, `build` |
|                 | `copy`      | 1B                     | Create a resource with identical structure and data                     | `clone`, `duplicate`, `replicate` |
|                 | `clone`     | 147M                    | Similar to `copy`                                                        | `copy`, `duplicate`, `replicate` |
|                 | `duplicate` | ~                    | Similar to `copy`.                                                       | `copy`, `clone`, `replicate` |
|                 | `replicate` | ~                    | Similar to `copy`, often implying reproducing behavior/functionality.    | `copy`, `clone`, `duplicate` |
| **Establishment** | `start`     | 1B                     | Initiate an operation                                                    | `begin`, `initiate`, `launch` |
|                 | `begin`     | 342M                    | Similar to `start`                                                       | `start`, `initiate`, `launch` |
|                 | `initiate`  | ~                    | Similar to `start`. Often more formal.                                 | `start`, `begin`, `launch` |
|                 | `launch`    | ~                    | Similar to `start`, often for starting a process or application.       | `start`, `begin`, `initiate` |
|                 | `open`      | 854M                    | Make a resource accessible/usable                                       |                      |


| Category        | Verb       | Github Usage (approx.) | Definition                                                             | Synonyms to Avoid |
|-----------------|------------|-------------------------|-------------------------------------------------------------------------|-------------------|
| **Obtainment** | `get`      | 2B                     | Obtain a resource                                                     | `fetch`, `retrieve`, `acquire`, `obtain` |
|                 | `fetch`    | 146M                    | Similar to `get`                                                     | `get`, `retrieve`, `acquire`, `obtain` |
|                 | `retrieve` | 116M                    | Similar to `get` or `fetch`                                          | `get`, `fetch`, `acquire`, `obtain` |
|                 | `acquire`  | ~                    |  Similar to `get`, often implying gaining possession or control of something. | `get`, `fetch`, `retrieve`, `obtain` |
|                 | `obtain`   | ~                    |  Similar to `get`. More formal.                                        | `get`, `fetch`, `retrieve`, `acquire` |
|                 | `read`     | 1B                     | Acquire data from a source                                              |                   |
|                 | `find`     | 672M                    | Look for unknown data in a container                                   | `search`, `locate`, `discover` |
|                 | `search`   | 438M                    | Similar to `find`, possibly across multiple containers                | `find`, `locate`, `discover` |
|                 | `locate`   | ~                    | Similar to `find`, emphasizing the position or place of something.      | `find`, `search`, `discover` |
|                 | `discover` | ~                    | Similar to `find`, often implying finding something unexpected or unknown. | `find`, `search`, `locate` |
|                 | `close`    | 492M                    | Make a resource inaccessible/unusable                                 | `shut`, `terminate` |
|                 | `shut`     | ~                    | Similar to `close`, often more forceful.                             | `close`, `terminate` |
|                 | `terminate`| ~                    | Similar to `close`, often implying ending a process or connection.      | `close`, `shut` |
| **True/False** | `is`      | 3B                     | Define the state of a resource                                         |                   |
|                 | `has`      | 1B                     | Define if a resource contains certain data                             |                   |
|                 | `can`      | 2B                     | Define a resource's ability                                              |                   |
|                 | `should`   | 1B                     | Define a resource's obligation                                           |                   |
