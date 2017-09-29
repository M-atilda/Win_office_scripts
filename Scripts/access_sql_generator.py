# -*- coding: utf-8 -*-

import sys
import re


#NOTE: there are lazy processes for simplicity and scalability (i'm not familiar with sql commands' differences in their envs)


def exec_translate_functions(l_funcs, s_target):
    s_result = s_target
    for f_info in l_funcs:
        if len(f_info[1]) == 0:
            s_result = f_info[0](s_target)
        else:
            s_result = f_info[0](s_target, f_info[1])
        s_target = s_result
    return s_result


def replace_chars(s_target, l_p_replace_chars):
    for replace_pair in l_p_replace_chars:
        #print("now debugging...")
        #print("{} {} {}".format(s_target, replace_pair[0], replace_pair[1]))
        s_target = re.sub(replace_pair[0], replace_pair[1], s_target)
    return s_target

def modify_case2switch(s_target):

    def recurse_modify_case2switch(s_acm, s_rest):
        #NOTE: just treat capital commands
        s_start_token = 'CASE'
        s_end_token = 'END'
        if s_start_token in s_rest:
            if s_start_token in s_rest[s_rest.find(s_start_token)+len(s_start_token) : s_rest.find(s_end_token)]:
                #nesting case sentense
                #FIXME: decide names of auto variables more carefully
                read_code_pointer = len(s_start_token)
                case_num = 1
                end_num = 0
                while case_num > end_num:
                    next_start = s_rest[read_code_pointer : ].find(s_start_token)
                    next_end = s_rest[read_code_pointer : ].find(s_end_token)
                    if next_start != -1 and next_start < next_end:
                        case_num = case_num + 1
                        read_code_pointer = read_code_pointer + next_start + len(s_start_token)
                    else:
                        end_num = end_num + 1
                        read_code_pointer = read_code_pointer + next_end + len(s_end_token)
                inner_start = s_rest.find(s_start_token) + len(s_start_token)
                inner_end = read_code_pointer-len(s_end_token)
                #TODO: tail recursion
                s_rest = s_rest[ : inner_start]\
                        + recurse_modify_case2switch("", s_rest[inner_start : inner_end])\
                        + s_rest[inner_end : ]

            s_acm = s_acm + s_rest[ : s_rest.find(s_start_token)]
            s_target = s_rest[s_rest.find(s_start_token) : s_rest.find(s_end_token)+len(s_end_token)]
            s_rest = s_rest[s_rest.find(s_end_token)+len(s_end_token) : ]

            s_result = replace_chars(s_target, [['CASE  WHEN', 'SWITCH ('], ['WHEN', ','], ['THEN', ','], ['ELSE', ', True,'], ['END', ')']])
            return recurse_modify_case2switch(s_acm+s_result, s_rest)
        else:
            return s_acm + s_rest

    return recurse_modify_case2switch("", s_target)



if __name__ == '__main__':
    s_target_file = sys.argv[1]
    s_sql_for_sql_server = ""
    s_sql_for_access = ""

    try:
        with open(s_target_file, 'r', encoding='utf-8') as f:
            s_sql_for_sql_server = f.read()
    except Exception as e:
        print("un exception occures while reading resource file [{}]".format(s_target_file_name))
        print("detail ...")
        print(e.__str__())

    #NOTE: this is said that Windows bug (it fails to use re module for bracket's replacement)
    #       it's said that some patch may solve this problem, but mendou
    #       please use an editor to replace them
    #l_replace_chars = [['\'', ''], ['[', ''], [']', '']]
    l_replace_chars = [['\'', '']]
    s_sql_for_access = exec_translate_functions([[replace_chars, l_replace_chars], [modify_case2switch, []]], s_sql_for_sql_server)
    print(s_sql_for_access)
