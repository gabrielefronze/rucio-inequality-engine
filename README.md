# Rucio Inequality Engine

This repository is a work in progress place where the Rucio Inequality Engine will be developed during early stages.

The aim for this piece of software is to provide a CLI to apply inequality filters to DiDs' metadata.
For example limiting the creation date between two days should be as easy as writing something like:

```
rucio-ie dateA < creation_date < dateB
```
where `creation_date` is a database column.

## Operations support
The Rucio Inequality Engine supports the following clusters of operations:

* equality: `==`, ` = `, ` eq `, ` -eq `
* greater: ` > `, ` gt `, ` -gt `
* greater or equal: `>=`, ` ge `, ` -ge `
* smaller: ` < `, ` lt `, ` -lt `
* smaller or equal: `<=`, ` le `, ` -le `
* logic and: `&&`, ` & `, ` and `
* logic or: `||`, ` | `, ` or `

A translation function reflects any of the supported operators to the corresponding python operator which can be directly evaluated.

## Composite filters
The Rucio Inequality Engine can be instanced using composite filters.
A single string of conditions can contain many sets of required conditions.
For example a filter string is:

```
user == jdoe, 1 < n_replicas < 2, upload_date > two_days_ago; user == gfronze, n_replicas >= 12; 
```

which, since `,` is interpreted as `and` and `;` as `or`, means:

```
Select all DiD of user "jdoe" with a number of replicas between 1 and 2 uploaded between now and two days ago

OR

Select all DiD of user "gfronze" with a number of replicas greater or equal to 12
```

Such request is organized by the Rucio Inequality Engine in a matrix form:

|                  | Condition 1      |  Condition 2         |  Condition 3                 | ...                        |  Condition N               |
|:----------------:|:----------------:|:--------------------:|:----------------------------:|:--------------------------:|:--------------------------:|
| **AND group 1**  | `user == jdoe`   | `1 < n_replicas < 2` | `upload_date > two_days_ago` |
| **AND group 2**  | `user == gfronze`| `n_replicas >= 12`   |                              |
| ...              | 
| **AND group N**  |

The matrix is then evaluated by lines requiring all conditions to be `True` (since these are AND Groups).

The resulting column vector formed by the And Groups evaluation is then evaluated requiring at least one AND Group to be `True`.

The final result, which is therefore the `or` of the multiple `and` defined by the lines, is the Rucio Inequality Engine output, hence can be used as filter flag.