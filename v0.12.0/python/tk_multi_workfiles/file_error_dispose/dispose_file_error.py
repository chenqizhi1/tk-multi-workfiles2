# -*- coding:utf-8 -*-
#coding=gbk
import os
import sys

import maya.cmds as cmds
def dispose_file_error(path):
    by_deleteing_lines = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for i in lines:
            if u'currentUnit' in i:
                break
            else:
                if u'requires "' in i:
                    by_deleteing_lines.append(i)
    for d_line in by_deleteing_lines:
        if d_line in lines:
            lines.remove(d_line)
    with open(path, 'w') as f1:
        f1.writelines(lines)
    return True
            
                    
                    

