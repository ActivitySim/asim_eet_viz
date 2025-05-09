import nbformat
import os
import sys
from nbconvert.preprocessors import ClearMetadataPreprocessor, ExecutePreprocessor, ClearOutputPreprocessor
import yaml

"""
Compile base-vs.-build result visualizations
from ActivitySim output tables, creating
summaries of the changes between two sets
of outputs across the variety of ActivitySim
models.

The compiler first executes the listed Jupyter
notebooks individually, then strips out all
notebook metadata to prepare the executed notebook
for rendering using `quarto`. The render procedure
then creates a set of HTML files from the config
file `_quarto.yml`, with a main page as defined in
`index.qmd` and a separate page for the notebook
itself.
"""

def compile():

    with open('_quarto.yml') as f:
        cfg = yaml.safe_load(f)
    
    # Read the list of Jupyter notebooks from the Quarto YAML config file
    notebooks = [x for x in cfg['book']['chapters'] if x.endswith('.ipynb')]

    for filename in notebooks:

        print(f"Executing notebook {filename}...")

        # open the notebook
        with open(filename) as fi:
            nb_in = nbformat.read(fi, nbformat.NO_CONVERT)

        # execute it 
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb_in)

        # strip out all metadata that causes issues for Quarto
        cmp = ClearMetadataPreprocessor(timeout=600, kernel_name='python3')
        cmp.preprocess(nb_in, resources={})

        # write the file back out, with execution results
        with open(filename, 'w', encoding='utf-8') as fo:
            nbformat.write(nb_in,fo)

    # combine all notebooks and markdown pages as HTML
    cmd = "quarto render"
    retval = os.system(cmd)

    if retval != 0:
        print(f"Quarto exited with return value {retval}")
        sys.exit(retval)

def clean():
    """
    This method cleans all output from the Jupyter notebooks to make
    them more appropriate for committing to the repository.
    """
    with open('_quarto.yml') as f:
        cfg = yaml.safe_load(f)
    
    # Read the list of Jupyter notebooks from the Quarto YAML config file
    notebooks = [x for x in cfg['book']['chapters'] if x.endswith('.ipynb')]

    for filename in notebooks:

        print(f"Cleaning notebook {filename}...")

        # open the notebook
        with open(filename) as fi:
            nb_in = nbformat.read(fi, nbformat.NO_CONVERT)

        # execute it 
        cp = ClearOutputPreprocessor(timeout=600, kernel_name='python3')
        cp.preprocess(nb_in, resources={})


if __name__ == "__main__":
    if "--clean" in sys.argv:
        clean()
    else:
        compile()