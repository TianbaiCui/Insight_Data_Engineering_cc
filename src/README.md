# Source Code

The only source code for this project is `h1b_counting.py`. Three arguments are needed in order the run the python script properly. For example:

```bash
$ python h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
```

The first argument is the path to the input dataset. The last two arguments are the paths to the output files. The order of these arguments do not matter. However, the input dataset must be placed in the `input` folder, the output file for the top 10 occupations must contain the word "occupation", and the output file for the top 10 states must contain the word "state".
