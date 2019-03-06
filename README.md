# Forknotes
I love this tool that was created, though having to use it through the terminal was a bit annoying. As a result, I GUIfied most of the input arguments for easier input, albeit slower as well. The convenience in my opinion however outweighs the speed.

## Running
*Note: You need to install Python3 before you can run any of this.*
You can run either `glitch_tool.py` or `runglitch.bat`. The latter just runs the former, but sets the output folder as `glitches/` automatically.
On Windows you can double-click either to run. On Linux, you most likely need to use the terminal.

# glitch-tool
glitch-tool is a simple Python script for messing with files in a few different ways. This tool was created for making glitch art, more specifically doing databending. You can read more about my results in [this blog post](https://tobloef.com/fun/glitch-art). This tool was mostly created for this one-time use and therefore the code quality isn't great. 

## Usage
```
usage: glitch_tool.py [-h] [-o OUTDIR] [-s SEED]
                      [-q] [--output-iterations OUTPUT_ITERATIONS]

Optional arguments:
  -o, --outdir         Output folder
  -s, --seed           Seed to use for random
  -q, --quiet          Surpress logging
  --output-iterations  How many changes between outputs
```

### Modes
The valid modes are:

* `change` - Change bytes in chunk to random values.
* `reverse` - Reverse order of bytes in chunk.
* `repeat` - Repeat first X bytes (specfied with `--repeat-width`) of chunk throughout the chunk.
* `remove` - Remove the chunk entirely.
* `zero` - Make the chunk all zeroes.
* `insert` - Insert random chunk of data at a random point.
* `replace` - Replace chunk with a chunk of random data.
* `move` - Remove a chunk from one position to another.