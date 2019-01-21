# time-window-limiter
a center limiter based on the time window
# Example
```python
    c = Lm()
    req_url = 'http://127.0.0.1/test_api/.*'
    cycle_time = 60
    cycle_times = 10
    start_time = 1542004896
    end_time = 1542091296
    timer = '0,14,29,44 * * * *'
    is_strict = False

    res = c.add_limit(req_url, cycle_time, cycle_times, start_time, end_time, timer, is_strict)
    if res:
        print('add limiter successfully!')
    else:
        print('failed to add limiter!')
    print(c.limit_dic)

    req_url = 'http://127.0.0.1/test_api/get_aa'
    limit_flag = c.is_limit(req_url)
    if limit_flag == 2:
        print('no limiter about this req!')
    elif limit_flag == 1:
        print('available req!')
    else:
        print('the req is limited!')
    print(c.get_all_limit())
```
