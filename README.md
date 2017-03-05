# sorting-network
Python script to check sorting networks and generate sorting network diagrams
This work is an extension of [https://github.com/brianpursley/sorting-network](https://github.com/brianpursley/sorting-network), which only has implemented the network diagrams of 4,5 and must have a connection network file supplied.
My work is to automatically generate the connetion network of N=2^k and improve the original drawing logic which is not capable to extend to other N.

## Usage

```
usage: sortingnetwork.py [-h] [-i inputfile] [-o [outputfile]] [-c] [-s [list]] [--svg [outputfile]]

optional arguments:
  -h, --help                                show this help message and exit
  -i n, --input n           specify the size of network. where n=2^k only
  -s [list], --sort [list]                  sorts the list using the input comparison network
  --svg [outputfile]                        generate SVG

## Examples


##### Read a comparison network from a file called example.cn and generate SVG to stdout.
```
./sortingnetwork.py --input 16 --svg
```

##### Read a comparison network from a file called example.cn and generate SVG, saved to a file called output.svg.
```
./sortingnetwork.py --input 16 --svg output.svg
```

##### Pipe the output to rsvg-convert to generate a PNG (or other format) instead of SVG.
(*rsvg-convert can be installed by using `sudo apt-get install librsvg2-bin` on Ubuntu.*)

```
./sortingnetwork.py --input 16 --svg | rsvg-convert > examples/16-input.png
```

##### Use a specified sorting network to sort a list.**The swap operation of the same layer haven't been parralled!**

```
./sortingnetwork.py --input 4 --sort [2,4,1,3]
```
Outputs `[1, 2, 3, 4]`

Using a 16-input sorting network to sort a list containing 16 items:
```
./sortingnetwork.py --input 16 --sort [4,2,7,2,5,8,12,5,2,4,1,3,19,21,20,29]
```
Outputs `[1, 2, 2, 2, 3, 4, 4, 5, 5, 7, 8, 12, 19, 20, 21, 29]`
