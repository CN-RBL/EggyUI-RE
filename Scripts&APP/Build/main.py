# -*- coding: utf-8 -*-
import rich.console
from rich.logging import RichHandler
import argparse
import warnings
import logging
import subprocess as sp

warnings.filterwarnings("ignore")

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
eure_build = """
  _____   _   _           ____    _____     ____    _   _   ___   _       ____  
 | ____| | | | |         |  _ \  | ____|   | __ )  | | | | |_ _| | |     |  _ \ 
 |  _|   | | | |  _____  | |_) | |  _|     |  _ \  | | | |  | |  | |     | | | |
 | |___  | |_| | |_____| |  _ <  | |___    | |_) | | |_| |  | |  | |___  | |_| |
 |_____|  \___/          |_| \_\ |_____|   |____/   \___/  |___| |_____| |____/ 
                                                                                
"""


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        datefmt="%Y/%m/%d %I:%M:%S",
        handlers=[RichHandler(locals_max_length=None, locals_max_string=None)]
    )
    log = logging.getLogger("rich")

    console = rich.console.Console()
    console.print(eu_logo)
    console.print(eure_build)

    log.debug("初始化console完成")

    parser = argparse.ArgumentParser(description="Eggy UI RE Build Tool")
    parser.add_argument("build_config", help="编译配置")
    args = parser.parse_args()

    log.debug(f"获取参数：build_config，参数值为{args.build_config}")
