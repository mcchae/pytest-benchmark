#!/bin/bash

rm -rf __pycache__
if [ -z $TMPDIR ];then
    rm -rf /tmp/tmp*
else
    rm -rf $TMPDIR/tmp*
fi
pytest --benchmark-autosave pybench.py 
