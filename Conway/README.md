# Conway's Game of Life

Conway's Game of Life written in C! I've created a serial and parallel version for benchmarking purposes. This game runs as expected, but note that
keys may need to be pressed multiple times to register. I used the ncurses library to render the game as it runs faster than printf and has some neat
features. PAPI must be installed to use `make`, if you want to use wall-clock time check out conway_serial.c. The rules application was able to be
parallelized. I was able to parallelize statistic generation, but I'm doubtful that made a significant impact. Printing with ncurses must be done
serially or else the game won't render correctly.

## Benchmarking

I integrated a "benchmark" mode into the game. Benchmark mode can be accessed by pressing 'b' in the start menu. This mode is needed as the typical
game size is a bit too small to show parallel performance increases. I benchmarked on two machines, my desktop and a university machine (Haswell-EP).
My desktop has a Ryzen 3600 (6 cores, 12 threads) and 16GB of DDR4 memory. Haswell-EP has 16 cores, 32 threads and 80GB of RAM. I generated the
average computation time for the rules and loop using a circular buffer (N=30). The averages seemed to stabilize after 50 generations, so I documented
my calculated averages at the 60th generation.

Results from benchmarking are in the tables below. I

**Desktop PC**

| Thread Count | Rules Time | Loop Time | Loop Speedup | Rules Speedup | Rules Parallel Efficiency |
| :----------: | :--------: | :-------: | :----------: | :-----------: | :-----------------------: |
|      1      |   23.0ms   |  61.1ms  |     N/A     |      N/A      |            N/A            |
|      2      |   21.5ms   |  59.6ms  |    1.03x    |     1.07x     |           53.5%           |
|      4      |   12.2ms   |  51.1ms  |    1.20x    |     1.89x     |           47.3%           |
|      8      |   10.8ms   |  49.3ms  |    1.24x    |     2.13x     |           26.7%           |
|      12      |   8.2ms   |  50.3ms  |    1.21x    |     2.80x     |           23.3%           |

**Haswell-EP**

| Thread Count | Rules Time | Loop Time | Loop Speedup | Rules Speedup | Rules Parallel Efficiency |
| :----------: | :--------: | :-------: | :----------: | :-----------: | :-----------------------: |
|      1      |   81.1ms   |  174.9ms  |     N/A     |      N/A      |            N/A            |
|      2      |   42.5ms   |  148.8ms  |    1.18x    |     1.91x     |           95.5%           |
|      4      |   21.8ms   |  108.1ms  |    1.62x    |     3.72x     |           93.0%           |
|      8      |   12.4ms   |  92.9ms  |    1.88x    |     6.54x     |           81.8%           |
|      12      |   10.8ms   |  88.2ms  |    1.98x    |     7.51x     |           62.6%           |
|      16      |   10.2ms   |  89.5ms  |    1.95x    |     7.95x     |           49.7%           |
|      32      |   10.7ms   |  95.7ms  |    1.83x    |     7.58x     |           23.7%           |

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
