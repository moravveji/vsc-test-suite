# vsc-test-suite
VSC test suite

## How to run the tests

run script that works recursively

```bash
cd vsc-test-suite
./run.sh args
```

Optional `args` will be passed to the reframe command.

To filter out tests and execute a subset of tests under the `tests` folder, you may use, e.g.:

```bash
./run.sh -c ./tests/cue
```

To (re)run a specific test (with a known test `<hash>`) and to enable `--verbose` output, do e.g.:

```bash
# the <hash> looks like '/75be71de'
./run.sh -c tests/cue/tools.py -n <hash> -p standard --system genius:single-node -r --verbose
```

If for some reason, the local config file is not automatically picked up by ReFrame, you may pass
`-C config_vsc.py` explicitly, too.

## Output location

Log files and output will be saved in $HOME/reframe

## Requirements 

- Reframe 4.3.3 installed as a module
- Python3
