```
~ ➤ hey -n 5000 -c 10 -m POST -H "Accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NTgzMTc3OCwianRpIjoiY2JlMmQ5MmItYzI3MS00OGUyLWJkNjItOWU0MDAxNjIzNzI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjllOWY4NDBjLTQ4NGMtNDRiMS1iNjcyLTRlYWZmNTgxNGU1ZiIsIm5iZiI6MTY1NTgzMTc3OCwiZXhwIjoxNjU1ODM1Mzc4LCJyb2xlcyI6W10sImFkbWluIjowfQ.7TdDlQ_UpFqo1JsrVwzbLCLpAD03weJNJWq0HkHLlU0"   -T "application/json" -d '{"user_id":"123", "film_id":"321", "film_timestamp":1}' http://127.0.0.1:8000/api/v1/
```

Summary:
  Total:	1.8415 secs
  Slowest:	0.0141 secs
  Fastest:	0.0008 secs
  Average:	0.0037 secs
  Requests/sec:	2715.1840

  Total data:	20000 bytes
  Size/request:	4 bytes

Response time histogram:
  0.001 [1]	|
  0.002 [33]	|■
  0.003 [2361]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.005 [2301]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.006 [227]	|■■■■
  0.007 [27]	|
  0.009 [18]	|
  0.010 [12]	|
  0.011 [8]	|
  0.013 [8]	|
  0.014 [4]	|


Latency distribution:
  10% in 0.0029 secs
  25% in 0.0032 secs
  50% in 0.0035 secs
  75% in 0.0040 secs
  90% in 0.0045 secs
  95% in 0.0049 secs
  99% in 0.0076 secs

Details (average, fastest, slowest):
  DNS+dialup:	0.0000 secs, 0.0008 secs, 0.0141 secs
  DNS-lookup:	0.0000 secs, 0.0000 secs, 0.0000 secs
  req write:	0.0000 secs, 0.0000 secs, 0.0003 secs
  resp wait:	0.0036 secs, 0.0008 secs, 0.0140 secs
  resp read:	0.0000 secs, 0.0000 secs, 0.0005 secs

Status code distribution:
  [200]	5000 responses
