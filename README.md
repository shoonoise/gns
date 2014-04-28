[![Build Status](https://travis-ci.org/yandex-sysmon/gns.svg?branch=master)](https://travis-ci.org/yandex-sysmon/gns)
[![Coverage Status](https://coveralls.io/repos/yandex-sysmon/gns/badge.png?branch=master)](https://coveralls.io/r/yandex-sysmon/gns?branch=master)
[![Docker Repository on Quay.io](https://quay.io/repository/yandexsysmon/gns/status "Docker Repository on Quay.io")](https://quay.io/repository/yandexsysmon/gns)
[![Latest Version](https://pypip.in/v/gns/badge.png)](https://pypi.python.org/pypi/gns/)
[![Dependency Status](https://gemnasium.com/yandex-sysmon/gns.svg)](https://gemnasium.com/yandex-sysmon/gns)
##Global Notification System##

###Running services###
Some services need to be run using PyPy3, others can work from the usual Python3.
Pypy3 services:
* `gns-splitter.py`
* `gns-worker.py`
* `gns-collector.py`

Example commands to start:
```
gns-cli fetcher -c etc/gns.d/gns.yaml
```

###Basic API usage###
Compatibility layer with [Golem/submit.sbml](http://nda.ya.ru/3QTLzG):
```
curl --data 'info=test' http://localhost:7887/api/compat/golem/submit?object=foo&eventtype=bar&info=test&status=critical'
```

Native pushing of event:
```
curl -H 'Content-Type: application/json' --data '{"host":"foo", "service":"bar", "status":"CRIT", "description":"test"}' http://localhost:7887/api/rest/v1/jobs
```
Dropping the event:
```
curl -X DELETE http://localhost:7887/api/rest/v1/jobs/<UUID>
```
Getting the information about the event:
```
curl http://localhost:7887/api/rest/v1/jobs/<UUID>
```
