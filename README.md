# Multibuild package for Maven Projects

This setup is intended to run multiple builds against a specific Indy instance.

## Installing

To install, you'll need to have virtualenv and python 3 installed:

```
    $ ./setup.sh
    $ source ./venv/bin/activate
```

## Test Setup

To run a test, the user must capture the build parameters in a YAML file. This file should be
in its own directory, since the output / logs / other data related to the build execution
will also be captured there. This allows the user to keep track of the circumstances under which
a particular type of build was run, and the result of that test.

The basic structure is:

```
    ./my-test-build
    +- test.yaml
```

## YAML Format

You can find a sample of the build specification in `sample-testfile.yaml`. The build specification allows
the user to specify the following:

* HTTProx proxy port (if used)
* section for build, containing:
  * number of build threads
  * number of total builds
  * project directory to use as a location for cloning build sources
* section for report verification, containing:
  * number of threads for verifying folo tracking reports

## Building a Test Project

The user must provide the following arguments to the `multibuild` command:

* TESTFILE - A path to the YAML file, which is outlined above. This file's directory will collect the build results
* INDY_URL - An Indy URL, with everything setup to work with the `public` group

