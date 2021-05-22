# Smart Contract Playground

## Introduction

This repo contains test contracts that can be compiled and tested to serve as a
baseline for more complex applications.

## Installation

### Dockerized

```bash
docker build --rm -t tezos/sc-playground .
```

### Non-Dockerized

- [Install](https://smartpy.io/cli/) smartpy

```bash
sh <(curl -s https://smartpy.io/cli/install.sh)
```

- export `$PATH` to use globally

```bash
export PATH="$SMARTPY_HOME/SmartPy.sh:$PATH"
```


## Running


### Dockerized

```bash
docker run -v $PWD:/app -p 8080:8000 -e PORT=8000 -it tezos/sc-playground # [optional args to smartpy]
```
- Browse `localhost:8080/` to view the tests and outputs.
- Note: If you don't pass any args, all contract tests will be run and stored at
  `$OUTPUT_DIR` (default: `/app/results/`)

### Non-Dockerized

```bash
Usage:
   ~/.local/smartpy/smartpy test        <script> <output> <options>* (execute all test targets)
   ~/.local/smartpy/smartpy compile     <script> <output> <options>* (execute all compilation targets)
   ~/.local/smartpy/smartpy kind <kind> <script> <output> <options>* (execute all custom targets added by sp.add_target(..., kind=<kind>))

   Parameters:
         <script>                                 : a python script containing SmartPy code
         <output>                                 : a directory for the results
         <kind>                                   : a custom target kind

   Options:
         --purge                                  : optional, clean output_directory before running
         --html                                   : optional, add html logs and outputs
         --protocol <delphi|edo|florence|granada> : optional, select target protocol - default is florence
         --<flag> <arguments>                     : optional, set some flag with arguments
         --<flag>                                 : optional, activate some boolean flag
         --no-<flag>                              : optional, deactivate some boolean flag
         --mockup                                 : optional, run in mockup (experimental, needs installed source)
         --sandbox                                : optional, run in sandbox (experimental, needs installed source)
```
