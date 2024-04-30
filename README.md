# OWS

OISD wildcards to Go regex

Example:

```shell
$ ./owr.py https://small.oisd.nl/domainswild > hosts.txt
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
