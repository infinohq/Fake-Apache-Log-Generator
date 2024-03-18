# Fake Apache Log Generator

This script generates a boatload of fake apache logs very quickly. Its useful for generating fake workloads for [data ingest](http://github.com/streamsets/datacollector) and/or analytics applications.

It can write log lines to console, to log files or directly to gzip files.

It utilizes the excellent [Faker](https://github.com/joke2k/faker/) library to generate realistic ip's, URI's etc.

***

## Requirements
* Python 3.10.10

## Generating Fake logs for Infino
1. Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).
2. [Setup your shell](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv) to automatically activate virtual env assigned to a directory.
2. Install python 3.10.10 using pyenv.
   ```
   pyenv install 3.10.10
   ```
3. Create a virtual env based on python 3.10.10
   ```
   pyenv virtualenv 3.10.10 py-3.10.10
   ```
4. Set the new virtualenv as the default for the Fake-Apache-Log-Generator directory.
   ```
   cd <Path to Fake-Apache-Log-Generator>
   pyenv local py-3.10.10
   ```
5. Install the dependencies using `pip install -r requirements.txt`
6. Run the fake log generator and specify the size of the log file to be generated.
   ```
   python apache-fake-log-gen.py --size 10g &> Apache-10G.log &`
   ```


## Detailed help
```
$ python apache-fake-log-gen.py -h
usage: apache-fake-log-gen.py [-h] [--output {LOG,GZ,CONSOLE}]
                              [--num NUM_LINES] [--prefix FILE_PREFIX]
                              [--sleep SLEEP] [--size FILE_SIZE]

Fake Apache Log Generator

optional arguments:
  -h, --help            show this help message and exit
  --output {LOG,GZ,CONSOLE}, -o {LOG,GZ,CONSOLE}
                        Write to a Log file, a gzip file or to STDOUT
  --num NUM_LINES, -n NUM_LINES
                        Number of lines to generate (0 for infinite)
  --prefix FILE_PREFIX, -p FILE_PREFIX
                        Prefix the output file name
  --sleep SLEEP, -s SLEEP
                        Sleep this long between lines (in seconds)
  --size FILE_SIZE, -z FILE_SIZE
                        Size limit of the generated file (e.g., 100k, 10m, 1g)
```

## Usage in Docker

Build the image:
```
docker build -t apache-fake-log-gen .
```

Run the application, and provide application command line arguments as Docker CMD args:
```
docker run --rm apache-fake-log-gen -n 10 -s 1
```
NOTE: `-o LOG` option does not work in this case.

## License
This script is released under the [Apache version 2](LICENSE) license.
