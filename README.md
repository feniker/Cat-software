# My GitHub Project

This is my GitHub project about data analysis on the CAT intallation.
-
If you want to use virtual enviroment you have to add ROOT to your PYTHONPATH:

```
# add ROOT to my venv
export OLD_PYTHONPATH="$PYTHONPATH" # to restore initial value save it to oldpath
export PYTHONPATH="/lib64/python3.6/site-packages"
```
and add it to deactivate
```
if [ -n "${OLD_PYTHONPATH:-}" ] ; then
    PYTHONPATH="$OLD_PYTHONPATH"
    export PYTHONPATH
    unset OLD_PYTHONPATH
fi
```