ParaView and Jupyter at CSCS. 2022 User Day in Bern (02-09-2022)

Where do I find these notes and the examples?

    git clone https://github.com/jfavre/Visualization-training

    goto directory [ParaView]([url](https://github.com/jfavre/Visualization-training/ParaView))
    
Motivations:

    Demonstrate that ParaView Python code can be run on a jupyter notebook
    A lightweight replacement to a dekstop ParaView client with many features:
        Data processing/Analysis/Filtering without graphics
        All of the above with an interactive 3D rendering window
        Can use all CPU threads for accelerated algorithms
        Can use MPI on-the-node,or on neighboring nodes
        Can use plugins, such as the NVIDIA IndeX plugin for advanced volume rendering
        Can import numpy arrays into ParaView (grid) objects

How to:

    Install [ipyparaview]([url](https://github.com/NVIDIA/ipyparaview)) 
    Create a Python virtual env as per our [documentation]([url](https://user.cscs.ch/tools/interactive/python/#python-virtual-environments))
    Use a [classic notebook]([url](https://user.cscs.ch/tools/interactive/jupyterlab/#introduction))

Load the ParaView module and other stuff:

    edit $HOME/.local/share/jupyter/kernels/myenv-kernel/launcher

```
#!/usr/bin/env bash

export PYTHONPATH=''
if [ "$SOURCE_JUPYTERHUBENV" == true ]; then
    source $HOME/.jupyterhub.env
fi

export PMI_NO_FORK=1
export PMI_NO_PREINITIALIZE=1
export PMI_MMAP_SYNC_WAIT_TIME=300

module load FFmpeg/5.0-CrayGNU-21.09
module load ParaView/5.10.1-CrayGNU-21.09-EGL
module load matplotlib

source /users/jfavre/myvenv/bin/activate
/users/jfavre/myvenv/bin/python -m ipykernel_launcher $@
```
Demonstrators:

    Hello_Sphere-ParaView.0.ipynb

    Hello_Sphere-ParaView.1.ipynb

    Hello_Sphere-ParaView.2.ipynb

    Hello_Molecule.ipynb

    XArrays-ParaView-Import.ipynb

    pvNVIDIA-IndeX.ipynb

    ParaView-SMP-Contours.ipynb

Questions? visit support.cscs.ch
