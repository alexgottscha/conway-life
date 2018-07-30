# Conway's Game of Life

This implements the cellular autonoma named "Life", invented by John Conway.

## Getting Started

Nothing yet.

### Prerequisites

No package prerequisites.  Needs Python 3.6 or a from_future import, as the 3.6 format string syntax is vastly better than in previous pythons.

### Installing

This is currently in library form only.  Run it in iPython and try the following:

```
run life.py
grid = Grid(80, 24, torus=False)
grid.print()
grid.update()
grid.print()
[etc]
```

## TODO
### Multiprocessing (see branch)
Basic idea is to split the grid into N sections where N is the number of processes.  Initial implentation can be just two or four sections, that will catch 95% of use cases.  Each section will need to have overlap with its adjacent sections, in order to be able to count neighbors for cells on the edges of the secton.  Thinking about it, there are two possible ways of doing this.
The first way would be to literally create N new sections that implement Grid.  The update method would have to be updated to ignore the edge rows, as they'd be included as overlap.  The second way would be to put the multiprocessing into the update() function, and have each process' loop iterate over its section.

## Contributing

Forks and pull requests are always welcome!

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Alex Gottschalk**

See also the list of [contributors](https://github.com/invertigo/conway-life/contributors) who participated in this project.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Coming soon!


