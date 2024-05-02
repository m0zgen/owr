# OWS

Wildcard listed domains list to Go (re2) regex converter.

## Features

- Different sourses (file or URL)
- Output to file or stdout
- Multi thread processing

## Example

Process a URL and save the result to a file:

```shell
$ ./owr.py https://small.oisd.nl/domainswild /path/to/dest/hosts.txt
```
### Results

Input:

```shell
*.example.com
```

Output:

```shell
/(^|^.*\.)example.(com)/
```

