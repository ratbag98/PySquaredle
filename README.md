# PySquaredle

## About this project

I'm learning Python as a 53-year old who grew up with BASIC, 6502, Pascal, C, C++,
Java, Perl, SQL, HTML, Elixir and maybe some others (shunned JavaScript and
avoid CSS like the plague). Always avoided Python due to the silly (to me)
whitespace stuff. Held my nose, dived in and found I rather liked it. So without
further ado, here's my first Python program:

## A Noddy Python program to solve the daily [Squaredle puzzle](https://squaredle.app/)

The puzzle involves a grid of letters. You start from any letter in the grid and
then join them continuously and without repetition to make words of four of more
letters. You have to find all the "normal" words in the grid in order to
complete the puzzle. There are additional "bonus" words, generally less common,
and these are used to differentiate contestants on the high score table.

The puzzle is susceptible to a recursive word-list "attack" and this simple
Python project does exactly that.

See the [wiki](https://github.com/ratbag98/PySquaredle/wiki) for more details
and help using the program.

There are bugs that I'm aware of (see the Issues page), but feel free to add any
other problems you find.

One key thing to note - my word list is not the same as Squaredle's, so there
will be false positives and negatives.

The program can also be used to generate new puzzles. See the -x and -g options
for displaying randomly-generated grids, using a sensible letter distribution
from a well-known word board game.

## Getting Started

I use a conda environment, and there are some dependencies, notably for the
GUI and development. You can run the following to clone my conda setup.

```bash
conda create --name squaredle --file conda_requirements.txt
conda activate squaredle
```

If you're using another package manager, take a quick look at the file and see
if you're missing anything on the list. I've included a pip_requirements.txt
file but have no idea how you use that (I think PyQt6 was installed via pip but
the rest came from conda).

Clone the repo. Make sure you've got a recent Python installed (I'm using
3.11 but it worked with 3.10 as well)).

### Minimal requirements

* Python 3.10.8 (now using 3.11, and may work with older 3.x versions)
* PyQt6 (for the GUI)
* requests (for fetching the daily puzzle)
* black (or blue), `pylint`, `pytest`, `pytest-qt`, `pytest-cov` (for development)

### Setup TODOs

* [ ] setup `pyproject.toml`
* [ ] create an installer for Python-deficient Mac Users
* [ ] consider creating other platform installers (Linux easy, Windows might be tough)

### Running the solver

We're going to use a grid that looks like:

```text
GAC
SNE
WID
```

So we run the solver with the letters organized as a single string reading the
grid from left to right, top to bottom:

```bash
./squaredle.py GACSNEWID
```

(upper or lower-case, live a little). If you're on Windows, sorry-not-sorry, but
use ```python squaredle.py GACSNEWID``` instead or do something funky.

The program will check that the letters can represent a Squaredle grid. There
should be a "square" number of letters (eg 3x3, 4x4, 5x5, etc). If the number of
letters is not square the program will quit.

Assuming you have entered a valid list of letters, the solver will come back
with all the valid words that can be made within the rules of Squaredle.

In this case the start of the results looks like:

```text
GANE
GAEN
GAED
GNIDE
ACNE
ACNED
ACED
ASWING
ASIDE
...
```

The ordering is primitive: I start with each letter in the list and recurse
depth-first from there. Once I've exhausted that letter it's on to the next in
the list you provided.

Note: the word list I'm using is hefty, but it still omits some valid words.
I'll endeavor to update it. If you've got a better word list you can substitute
it. You should trim short words from it (only include four letters and more). I
used:

```bash
rg -Nw '^[a-z]{4,}$' words.txt > word_list.txt
```

to trim the list appropriately.

## GUI

New feature: a PyQt6-based GUI that shows individual word solutions by the magic
of squiggly lines.

There's a video of it in action on the [Wiki](https://github.com/ratbag98/PySquaredle/wiki)

## Scraping

Another new feature: running the script without a word list will fetch today's
puzzle for you. It reads the Javascript directly, since I hate web-page scraping
with a passion. If the author of Squaredle changes the format then my code will
break, which is sad.

## Basic program logic

The puzzle is represented as a string. Most of the code uses indexes into this
string. A function is provided that maps between grid coordinates and indexes.

The word list is stored as a "trie" which allows for efficient searching for
words that start with a set of letters.

The solution algorithm iterates over each letter in the puzzle string. Using the
character it then recursively generates chains of letters. The next letter in
the chain is selected from the last item in the chain's "neighbors". For
example if we have a grid of letters:

```text
ABC
DEF
GHI
```

then the puzzle string looks like:

```text
012345678
ABCDEFGHI
```

(the numbers are the index into the string).

We'll start with the first letter, A, index 0. To calculate the neighbors,
imagine this grid of indexes:

```text
012
345
678
```

So letter A, top-left in the grid, has three neighbors: 1,3 and 4. These
translate into the letters B, D and E. So the chain recursion routine will check
01, 03, 04 in turn. It actually works depth first, but this shows the flattened
logic in the function itself.

The chain recursion will check chains like 0124, 0125, 0145, 0143, 01436 etc.

The chains are converted back to strings by dereferencing the puzzle character
array (ABCE, ABCF, ABEF, etc.). If the word is in the trie structure it gets
added to the solution. If there are words in the trie that start with the
candidate "word" (string of letters), then we keep searching down the chain (ie
call the recursive function with the chain and add new neighbors).

If there are no further words in the trie that start with our current chain's
letters then we go to the next neighbour and recurse into that chain.

The recursion unwinds as chains fail to match anything in the trie.

The recursion is called once per letter in the puzzle grid and once all the
letters have been checked the set of solutions is returned.

A set is used since the same word can be found in multiple ways sometimes.
Whilst this is interesting to know, it doesn't help solve the puzzle so
repetitions are dropped.

### Optimizations

A run with CProfile showed that the word list loading was the slowest part of
the code, specifically the string processing in the Trie. With that in mind I
narrowed the word list to avoid loading impossible words, ie those that are too
long or composed of letters not found in the puzzle

### Possible things to try in the code as mental exercises

* DONE. Relax the uniqueness requirement, in case we want to show the solution in some
  graphical fashion on the grid and to include alternatives. The GUI now shows
  multiple solutions for a given word, in spangly technicolor
* DONE: Consider RadixTrie for word list storage, but I think the efficiencies it
  gives (space, search) are less useful when set against the cost of initially
  adding the words. I was right about this, so I kept the Trie. If I was making
  a long-lived program that persisted as many puzzles were loaded then it might
  be appropriate to go the RadixTrie route.

## Roadmap

* [ ] Optionally separate results for "common" vs "uncommon" words (struggling
  to find appropriate wordlists or to decrypt Squaredle's lists)
* [ ] Keep word list up to date (see above)
* [ ] Live update of the search like in the movies (would need a rejig of the
  Solver class to give access to the GUI as the solution is generated)
* [ ] Reverse the logic somewhat in order to generate puzzles (still thinking
  about this one - could generate a grid from a set of letters then iteratively
  solve it until a desired word/complexity is present)
* [ ] Automate dependency file creation (`conda list -e > req.txt`) on change.
* [ ] Installer
* [ ] [`pyproject.toml`](https://godatadriven.com/blog/a-practical-guide-to-setuptools-and-pyproject-toml/)
* [ ] GUI preferences
* [x] Handle gaps in the square. Presentation-side.
* [x] Handle gaps:  download logic needs an overhaul
* [x] Test suite (needs revisiting since I wasn't a good little TDDer)
* [x] Make code more idiomatic (ongoing)
* [x] Some graphical pizazz to show word formation in the grid

## Contributing

Not looking for contributions right now. This is a learning exercise as I start
my journey in Python. Once it's "finished" I'll be happy to accept
contributions.

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact

Project link: <https://github.com/ratbag98/PySquaredle.git>

## Acknowledgements

* Trie structure (basis):
  [AskPython](https://www.askpython.com/python/examples/trie-data-structure)
* Word list from: [`dwyl`](https://github.com/dwyl/english-words.git)
* Half way through this I started using Github Copilot. "It's a bit of a mixed
  bag, but it's fun to see what it comes up with. I've tried to keep the code
  idiomatic, but it's hard to resist the temptation to use some of the
  suggestions" is what it just typed for me! I agree entirely.
* Made good use of [this book](https://www.pythonguis.com/pyqt6-book/) and the
  site it's based on
* I didn't look at anyone else's solver, since this is a learning exercise
  rather than something that aims to be "the best".
