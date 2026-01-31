# -*- coding: utf-8 -*-
import rich.console
from PyQt6.QtWidgets import QApplication
from tray import Tray
from pet import Pet
import sys

# TODO: 信仰之蛋
eu_logo = r"""[bold]
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

rich.console.Console().print(eu_logo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    pet.show()
    tray = Tray(parent=pet)
    tray.show()
    app.exec()
    tray = None
