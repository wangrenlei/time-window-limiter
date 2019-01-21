# -*- coding: utf-8 -*-

# @Date  :  18-11-9 下午2:59
# @Author:  pubcoder_wj

import time
import re


class Lm(object):
    def __init__(self):
        self.limit_dic = dict()

    def check_params(self, req_url, cycle_time, cycle_times, start_time, end_time, timer, is_strict):
        """
        :param req_url:
        :param cycle_time:
        :param cycle_times:
        :param start_time:
        :param end_time:
        :param timer:
        :param is_strict:
        :return:
        """
        if start_time > end_time:
            print('start_time > end_time is error!')
            return False
        else:
            return True

    def parse_time(self, start_time, end_time, timer):
        """
        :param start_time:
        :param end_time:
        :param timer:
        :return:
        """
        now_time = int(time.time())
        if (now_time >= start_time) and (now_time <= end_time):
            # TODO if timer_parser
            return True
        else:
            return False

    def trans_req_url(self, req_url):
        """
        :param req_url:
        :return:
        """
        for k_pattern, v in self.limit_dic.items():
            if re.match(k_pattern, req_url):
                print(f'req url is match, the url: {k_pattern}')
                return k_pattern
        return None

    def add_limit(self, req_url, cycle_time, cycle_times, start_time, end_time, timer, is_strict):
        """
        :param req_url:
        :param cycle_time:
        :param cycle_times:
        :param start_time:
        :param end_time:
        :param timer:
        :param is_strict:
        :return:
        """
        if self.check_params(req_url, cycle_time, cycle_times, start_time, end_time, timer, is_strict):
            trans_req_checked = self.trans_req_url(req_url)
            if trans_req_checked:
                print(f'the req url is exist -> {trans_req_checked}')
                return False
            else:
                limit_info = dict()
                limit_info['cycle_time'] = cycle_time
                limit_info['cycle_times'] = cycle_times
                limit_info['pre_req_time'] = start_time
                limit_info['current_used_times'] = 0
                limit_info['start_time'] = start_time
                limit_info['end_time'] = end_time
                limit_info['timer'] = timer
                limit_info['is_strict'] = is_strict
                self.limit_dic[req_url] = limit_info
                return True
        else:
            print('error limit params!')
            return False

    def get_limit(self, req_url):
        """
        :param req_url:
        :return:
        """
        return self.limit_dic[req_url]

    def get_all_limit(self):
        """
        :return:
        """
        return self.limit_dic

    def is_limit(self, req_url):
        """
        :param req_url:
        :return:
        """
        real_req_url = self.trans_req_url(req_url)
        if real_req_url:
            req_limit = self.get_limit(real_req_url)

            start_time = req_limit['start_time']
            end_time = req_limit['end_time']
            timer = req_limit['timer']
            time_checked = self.parse_time(start_time, end_time, timer)
            if time_checked:
                is_strict = req_limit['is_strict']
                start_req_time = req_limit['pre_req_time']
                cycle_time = req_limit['cycle_time']
                cycle_times = req_limit['cycle_times']
                current_used_times = req_limit['current_used_times']
                now_time = int(time.time())
                end_req_time = start_req_time + cycle_time
                if now_time > end_req_time:
                    print('out of the first cycle time range')
                    # reset
                    start_req_time = end_req_time + ((now_time - end_req_time) // cycle_time) * cycle_time
                    print(now_time)
                    print(end_req_time)
                    print(start_req_time)
                    self.limit_dic[real_req_url]['pre_req_time'] = start_req_time
                    current_used_times = 0
                    self.limit_dic[real_req_url]['current_used_times'] = current_used_times
                if current_used_times + 1 <= cycle_times:
                    current_used_times += 1
                    self.limit_dic[real_req_url]['current_used_times'] = current_used_times
                    return 1
                else:
                    print('out of the req limit!')
                    return 0
            else:
                print('not in excuting time！')
                return 0
        else:
            return 2

    def check_is_reset_cycle(self):
        pass

    def clear_rule_cache(self):
        pass


if __name__ == '__main__':
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
