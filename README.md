# Fake Apache Log Generator

This script generates a boatload of fake apache logs very quickly. Its useful for generating fake workloads for [data ingest](http://github.com/streamsets/datacollector) and/or analytics applications.

It can write log lines to console, to log files or directly to gzip files.

It utilizes the excellent [Faker](https://github.com/joke2k/faker/) library to generate realistic ip's, URI's etc.

***

## Basic Usage

Generate a single log line to STDOUT
```
$ python apache-fake-log-gen.py  
```

Generate 100 log lines into a .log file
```
$ python apache-fake-log-gen.py -n 100 -o LOG 
```

Generate 100 log lines into a .gz file at intervals of 10 seconds
```
$ python apache-fake-log-gen.py -n 100 -o GZ -s 10
```

Infinite log file generation (useful for testing File Tail Readers)
```
$ python apache-fake-log-gen.py -n 0 -o LOG 
```

Prefix the output filename 
```
$ python apache-fake-log-gen.py -n 100 -o LOG -p WEB1
```


Detailed help
```
$ python3 apache-fake-log-gen.py -h
usage: apache-fake-log-gen.py [-h] [--output {LOG,GZ,CONSOLE}] [--log-format {CLF,ELF}] [--num NUM_LINES]
                                   [--prefix FILE_PREFIX] [--sleep SLEEP] [--domain DOMAIN] [--min_ip MIN_IP]
                                   [--max_ip MAX_IP] [--auth_page AUTH_PAGE] [--register_page REGISTER_PAGE]

Fake Apache Log Generator

options:
  -h, --help            show this help message and exit
  --output {LOG,GZ,CONSOLE}, -o {LOG,GZ,CONSOLE}
                        Write to a Log file, a gzip file or to STDOUT
  --log-format {CLF,ELF}, -l {CLF,ELF}
                        Log format, Common or Extended Log Format
  --num NUM_LINES, -n NUM_LINES
                        Number of lines to generate (0 for infinite)
  --prefix FILE_PREFIX, -p FILE_PREFIX
                        Prefix the output file name
  --sleep SLEEP, -s SLEEP
                        Sleep this long between lines (in seconds)
  --domain DOMAIN, -d DOMAIN
                        domain of current website
  --min_ip MIN_IP       minimum value to before changing IP
  --max_ip MAX_IP       maximum value to before changing IP
  --auth_page AUTH_PAGE
                        Authentification page, script will post this page.
  --register_page REGISTER_PAGE
                        Authentification page, script will post this page.
```


## Requirements
* Python 2.7
* ```pip install -r requirements.txt```

## License
This script is released under the [Apache version 2](LICENSE) license.
