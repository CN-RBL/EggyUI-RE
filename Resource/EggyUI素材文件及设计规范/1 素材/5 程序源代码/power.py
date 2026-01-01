from win11toast import toast
import os
rt1 = toast('电源选项', '请保存好个人文件，然后选择下列选项', selection=['关机', '重启', '休眠',], button='确定', duration='long')
if str(rt1) == "{'arguments': 'http:确定', 'user_input': {'selection': '关机'}}":
    os.system("shutdown -s -t 0")
elif str(rt1) == "{'arguments': 'http:确定', 'user_input': {'selection': '重启'}}":
    os.system("shutdown -r -t 0")
elif str(rt1) == "{'arguments': 'http:确定', 'user_input': {'selection': '休眠'}}":
    os.system("shutdown -h")