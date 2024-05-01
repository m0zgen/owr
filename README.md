# OWS

OISD wildcards to Go (re2) regex

Example:

```shell
$ ./owr.py https://small.oisd.nl/domainswild /path/to/dest/hosts.txt
```

Input:

```shell
*.example.com
```

Output:

```shell
/(^|^.*\.)example.(com)/
```

## Ref

- https://oisd.nl/setup
- https://github.com/google/re2/wiki/Syntax
