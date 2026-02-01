# -*- coding: utf-8 -*-
import rich.console
from rich.logging import RichHandler
import argparse
import warnings
import logging
import subprocess as sp
import json
import os
from threading import Thread

warnings.filterwarnings("ignore")

# TODO: 信仰之蛋
eu_logo = """[bold]
[yellow]                                                     .+:        
                                                     +%#:       
                                                    :#[white]@[yellow]%#-      
       ..                                          .*%[white]@@[yellow]%#*:    
     :*%%#-                                       .*%[white]@@@@@[yellow]%#.   
    :%%%%%%-         .-+*#####*+-.                +%[white]@@@@@@[yellow]%+    
    #%%%%%%%       -*%%%%%@[white]@@@@@@[yellow]@*:              -#%[white]@@@@[yellow]#= .   
   .%%%%%%%%-    -#%%%%@[white]@@@@@@@@@@@[yellow]@#:             .=#%[white]@[yellow]%+ +#-  
   :%%%%%%%%:  .*%%#%[white]@@@@@@@@@@@@@@@@@[yellow]*              -#%%..#%#= 
   .%#%%%%%%= :#%%%%[white]@@@@@@@@@@@@@@@@[yellow]##[white]@[yellow]%.    -==:     -#=.*%[white]@@[yellow]%+
    =%###%%%%+#%%%%[white]@@@@@[yellow]%##%[white]@@@@@@[yellow]%*#[white]@@@%[yellow]: :#%%%%+     . -%[white]%@@[yellow]#=
     +%%%%%%%%%%%%[white]@@@@@@@[yellow]%###*[white]@@@@[yellow]####[white]@@@%:[yellow]#%%%%%%=       =#[white]%%[yellow]= 
      :=+:.*%#%%%[white]@@@@@@@@@@[yellow]##%[white]@@@@@@[yellow]@%[white]@@@@[yellow]%%%%%%%%%        :##. 
           +%#%%[white]@@@@@@@@[yellow]@#*%[white]@@@@@@[yellow]%[white]@@@@@@@@[yellow]%%%%%%%%:        :.  
          :%%%#%[white]@@@@@@@@@[yellow]@@[white]@@@@[yellow]#%%#[white]@@@@@@@[yellow]%%%%%%%%%-            
          *%%%#[white]@@@@@@@@@@@@@@@@@[yellow]##[white]@@@@@@@@@[yellow]%%%%%%%%-            
         :%#%%%[white]@@@@@@@@@@@@@@@@@@@@@@@@@@@@[yellow]%%%%%%%%-            
         +%#%#%[white]@@@@@@@@@@@@@@@@@@@@@@@@@@@@@[yellow]%%%%%%%-            
         #%#%#%[white]@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@[yellow]%%%%%%:            
        -%%%%#%[white]@@@@@@@@@@@@[yellow]%%%%%%[white]@@@@@@@@@@@@[yellow]%%%%%#             
       =%%%%%#%[white]@@@@@@@@@@[yellow]%%%%%%%%%[white]@@@@@@@@@@@[yellow]%%%%%=             
     :#%#%%%%#%[white]@@@@@@@@@[yellow]%%%%%%%%%%%[white]@@@@@@@@@@[yellow]%%%%#              
    -%####%%%#%[white]@@@@@@@@[yellow]%%%%%%%%%%%%[white]@@@@@@@@@[yellow]%%%%#.              
   +%#####%%%%#[white]@@@@@@@[yellow]%%%%%%%%%%%%%[white]@@@@@@@@@[yellow]%%%#.               
  =%######%%%%#%[white]@@@@@[yellow]%%%%%%%%%%%%%%[white]@@@@@@@@@[yellow]%%+                 
 -%###%%%%%###%#[white]@@@@@[yellow]%%%%%%%%%%%%%%[white]@@@@@@@@[yellow]%%%.                 
 ###%%%%%%%###%%%[white]@@@[yellow]%%%%%%%%%%%%%%%[white]@@@@@@@[yellow]%%%#                  
:%#%%%%%%######%#%[white]@@[yellow]%%%%%%%%%%%%%%[white]@@@@@@@@[yellow]%%%+                  
.%%######%%#######%[white]@[yellow]%%%%%%%%%%%%%%[white]@@@@@@@[yellow]%%%%:                  
 =%%%%%%%########%#%%%%%%%%%%%%%#[white]@@@@@@@[yellow]%%%%#                   
  .-==-:. =%########%%%%%%%%%%%#%[white]@@@@@[yellow]%%%%%%-                   
           ########%%%%%%%%%%%%%[white]@@@@[yellow]%%%%%%%#                    
           :%######%%%%%%%%%%%%%[white]@[yellow]%%##%%%%%%:                    
            =%#####%%%%%%%%%%%%%###%%%%%%%-                     
             =%###%%%%%%%%%%%%%#%%%%%%%%%=                      
              =%##%#%%%%%%%%%%%%%%%%%#%%=                       
               -#%###%%%%%%%%%%%%%%%#%%-                        
                +#%%###%########%%#%%+.                         
              :*= :*%%%#########%#%#:                           
             =#-    .-*%#######%##%.                            
           :*#:       *%#########%:                             
          -#+        +%#########%=                              
          *=       [green].[yellow] ##########%=                               
                 [green].+#:[yellow]#########%=                                
           [red]:=[green]   -*#+.[yellow]%###%##%%-                                 
          [red]-#+[green]  =**=[yellow]  +%###%%*.                                  
         [red]=*- [green].+**:[yellow]    *%%%#-                                    
       [red]:++. [green]=#*+.[yellow]    -*#*:                                      
     [red].=*=  [green]=**-[yellow]     +##+                                        
    [red].++-  [green].*+[yellow]     :*##=                                         
    [red].-:[yellow]          -##*:                                          
                .##+                                            
                  .                                             
                                                                
                                                                                                                                                                                         
"""
eure_build = r"""
  _____   _   _           ____    _____     ____    _   _   ___   _       ____  
 | ____| | | | |         |  _ \  | ____|   | __ )  | | | | |_ _| | |     |  _ \ 
 |  _|   | | | |  _____  | |_) | |  _|     |  _ \  | | | |  | |  | |     | | | |
 | |___  | |_| | |_____| |  _ <  | |___    | |_) | | |_| |  | |  | |___  | |_| |
 |_____|  \___/          |_| \_\ |_____|   |____/   \___/  |___| |_____| |____/ 
                                                                                
"""


def build_main(name: str, tool: str, args: list, log: logging.Logger) -> None:
    with sp.Popen([f"python -m {tool}"]+args, encoding="utf-8", ) as p:
        for t in p.stdout:
            log.info(f"[{name}] [{tool.capitalize()}构建中] {t}")

def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        datefmt="%Y/%m/%d %I:%M:%S",
        handlers=[RichHandler(locals_max_length=None, locals_max_string=None)]
    )
    log: logging.Logger = logging.getLogger("rich")

    console: rich.console.Console = rich.console.Console()
    console.print(eu_logo)
    console.print(eure_build)

    log.debug("初始化console完成")

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Eggy UI RE Build Tool")
    parser.add_argument("build_config", help="编译配置")
    args: argparse.Namespace = parser.parse_args()

    log.debug(f"获取参数：build_config，参数值为{args.build_config}")
    log.info("准备编译...")

    # 编译文件需放在同级目录下
    config_path: str = f"{os.path.dirname(os.path.realpath(__file__))}/{args.build_config}.json"
    with open(config_path, "rt", encoding="utf-8") as f:
        log.debug(f"编译配置文件路径：{config_path}")
        config: dict = json.load(f)
        mxs: list[str] = []  # 存放配置项
        log.info(f"编译配置文件加载完成")
        log.info(f"名称：{config["config_name"]}\n"
                 f"描述：{config["config_description"]}\n"
                 f"异步编译：{"是" if config["async"] else "否"}")
        try:
            _: int = 1
            while True:
                log.info(f"第{_}个配置项：\n"
                         f"名称：{config[f"M{_}"]["name"]}\n"
                         f"描述：{config[f"M{_}"]["description"]}\n")
                mxs.append(f"M{_}:{config[f"M{_}"]["name"]}:{config[f"M{_}"]["tool"]}:{config[f"M{_}"]["cmd"]}")
                _ += 1
        except KeyError:
            log.debug(f"MXS: {mxs}")
        log.debug("完成遍历，准备编译...")
        for mx in mxs:
            mx = mx.strip(":")
            build_main(f"{mx[1]} ({mx[0]})", mx[2], mx[3], log)
