#!/bin/sh
# automate release testing steps
#
# check local tests pass

if hg sum --remote
    then echo "** no remote changegs **"
    else
    echo "** FAIL ** repository out of sync"
    exit 1
fi
# check setup.py required setup.py attributes
if python setup.py check --strict
    then echo "** Attribute Testing passed. **"
    else
    echo "** FAIL ** Testing failed $?- Exiting release script"
    exit 1
fi

# check long_description RST formatting
if python setup.py check --restructuredtext --strict
    then echo "** long_description RST Testing passed. **"
    else
    echo "** FAIL ** Testing failed $?- Exiting release script"
    exit 2
fi

# check unit tests
if py.test
    then echo "** Testing passed. **"
    else
    echo "** FAIL ** Testing failed $?- Exiting release script"
    exit 3
fi

# check docs build locally
cd docs
make clean
if make html
    then echo "** Doc Build passed. **"
    else
    cd ..
    echo "** FAIL ** Document Build failed - Exiting release script"
    exit 4
fi
cd ..
# clean up the build directories
rm -rf pysftp.egg-info/
# build
python setup.py sdist