# Conway's Game of Life

Conway's Game of Life written in C! I've created a serial and parallel version for benchmarking purposes. This game runs as expected, but note that
keys may need to be pressed multiple times to register. I used the ncurses library to render the game as it runs faster than printf and has some neat
features. PAPI must be installed to use `make`, if you want to use wall-clock time check out conway_serial.c. Unfortunately, only the rules application
was able to be parallelized. Printing with ncurses must be done serially or else the game won't render correctly.

## Benchmarking

I integrated a "benchmark" mode into the game. Benchmark mode can be accessed by pressing 'b' in the start menu. This mode is needed as the typical
game size is a bit too small to show parallel performance increases. I benchmarked on two machines, my desktop and a university machine (Haswell-EP).
My desktop has a Ryzen 3600 (6 cores, 12 threads) and 16GB of DDR4 memory. Haswell-EP has 16 cores, 32 threads and 80GB of RAM.

Results from benchmarking are in the tables below.

**Desktop PC**

| Thread Count | Loop Time | Speedup | Parallel Efficiency |
| :----------: | :-------: | :-----: | :-----------------: |
|      1      |     e     |   N/A   |         N/A         |
|      2      |          |        |                    |
|      4      |          |        |                    |
|      8      |          |        |                    |
|      12      |          |        |                    |

**Haswell-EP**

| Thread Count | Loop Time | Speedup | Parallel Efficiency |
| :----------: | :-------: | :-----: | :-----------------: |
|      1      |     e     |   N/A   |         N/A         |
|      2      |          |        |                    |
|      4      |          |        |                    |
|      8      |          |        |                    |
|      12      |          |        |                    |
|      16      |          |        |                    |
|      32      |          |        |                    |

## Related Works:

* [Shodor](http://www.shodor.org/media/content/petascale/materials/UPModules/GameOfLife/Life_Module_Document_pdf.pdf)
* [Argonne National Lab](https://wordpress.cels.anl.gov/atpesc/wp-content/uploads/sites/96/2017/08/ATPESC_2017_Track-2_2_8-1_830am_Balaji-Gropp-Thakur-Hands-on_Mlife-code-desc.pdf)
* [Colombia](https://www.cs.columbia.edu/~sedwards/classes/2021/4995-fall/reports/ParLife.pdf)
* [Scientific American, 1970](https://www.ibiblio.org/lifepatterns/october1970.html)

## References:

* [GNU ncurses documentation](https://invisible-island.net/ncurses/ncurses-intro.html)
* [tldp ncurses](https://tldp.org/HOWTO/NCURSES-Programming-HOWTO/)
* [Cheatsheet for ncurses](https://github.com/thenamankumar/ncurses-cheatsheet)
* [Example of existing game](https://github.com/AWikramanayake/conway-game-of-life)
