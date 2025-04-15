from colorama import Fore,Style,Back   
import itertools
import sys
import time

class Palette:
    
    @staticmethod
    def pickme(var):
        if not isinstance(var,str):
            raise Exception(f"Senpai <3 it's must be a string not {type(var)}")
        colors = [Fore.RED,'\033[38;5;206m','\033[38;5;214m', Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA,Fore.WHITE]

        color_cycle = itertools.cycle(colors)
        for i in range(len(var)):
            colored_text = ''.join(next(color_cycle) + char for char in var[:i]) + next(color_cycle) + var[i] + var[i+1:]
            sys.stdout.write('\r' + colored_text)  
            sys.stdout.flush() 
            time.sleep(0.1)
        sys.stdout.write(Style.RESET_ALL + '\n')
        sys.stdout.flush()

    @staticmethod
    def red(*vars):
        var = " ".join(map(str, vars))
        print(f"{Fore.RED}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def pink(*vars):
        var = " ".join(map(str, vars))
        print(f"\033[38;5;206m{var}\033[0m")
    
    @staticmethod
    def cyan(*vars):
        var = " ".join(map(str, vars))
        print(f"{Fore.CYAN}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def yellow(*vars):
        var = " ".join(map(str, vars))
        print(f"{Fore.YELLOW}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def blue(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Fore.BLUE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def green(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Fore.GREEN}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def white(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def redBack(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Back.RED}{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def pickmeBack(var):
        if not isinstance(var,str):
            raise Exception(f"Senpai <3 it's must be a string not {type(var)}")
        colors = [Back.RED, Back.YELLOW, Back.GREEN, Back.CYAN, Back.BLUE, Back.MAGENTA,Back.WHITE]

        color_cycle = itertools.cycle(colors)
        for i in range(len(var)):
            colored_text = ''.join(next(color_cycle) + char for char in var[:i]) + next(color_cycle) + var[i] + var[i+1:]
            sys.stdout.write('\r' + colored_text)  
            sys.stdout.flush() 
            time.sleep(0.1)
        sys.stdout.write(Style.RESET_ALL + '\n')
        sys.stdout.flush()

    
    @staticmethod
    def pinkBack(*vars):
        var = " ".join(map(str, vars))
        print(f"\033[48;5;206m{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def cyanBack(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Back.CYAN}{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def yellowBack(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Back.YELLOW}{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def blueBack(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Back.BLUE}{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def greenBack(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Back.GREEN}{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def whiteBack(*vars):
        var = " ".join(map(str, vars))
        
        print(f"{Back.WHITE}{Fore.BLACK}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def redTag(tag,var):
        print(f"[{tag}] {Fore.RED}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def pinkTag(tag,var):
        print(f"[{tag}] \033[38;5;206m{var}\033[0m")
    
    @staticmethod
    def cyanTag(tag,var):
        print(f"[{tag}] {Fore.CYAN}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def yellowTag(tag,var):
        print(f"[{tag}] {Fore.YELLOW}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def blueTag(tag,var):
        print(f"[{tag}] {Fore.BLUE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def greenTag(tag,var):
        print(f"[{tag}] {Fore.GREEN}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def whiteTag(tag,var):
        print(f"[{tag}] {Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def redFatTag(tag,var):
        print(f"{Back.RED}[{tag}]{Style.RESET_ALL} {Fore.RED}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def pinkFatTag(tag, var):
        print(f"\033[48;5;206m[{tag}]\033[0m \033[38;5;206m{var}\033[0m")
    
    @staticmethod
    def cyanFatTag(tag,var):
        print(f"{Back.CYAN}[{tag}]{Style.RESET_ALL} {Fore.CYAN}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def yellowFatTag(tag,var):
        print(f"{Back.YELLOW}[{tag}]{Style.RESET_ALL} {Fore.YELLOW}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def blueFatTag(tag,var):
        print(f"{Back.BLUE}[{tag}]{Style.RESET_ALL} {Fore.BLUE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def greenFatTag(tag,var):
        print(f"{Back.GREEN}[{tag}]{Style.RESET_ALL} {Fore.GREEN}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def whiteFatTag(tag,var):
        print(f"{Back.WHITE}[{tag}]{Style.RESET_ALL} {Fore.WHITE}{var}{Style.RESET_ALL}")
    
        
    ## return
    @staticmethod
    def redReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Fore.RED}{var}{Style.RESET_ALL}"
     
    @staticmethod
    def pinkReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"\033[38;5;206m{var}\033[0m"
    
    @staticmethod
    def cyanReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Fore.CYAN}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def yellowReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Fore.YELLOW}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def blueReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Fore.BLUE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def greenReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Fore.GREEN}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def whiteReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def redBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Back.RED}{Fore.WHITE}{var}{Style.RESET_ALL}"
     
    @staticmethod
    def pinkBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"\033[48;5;206m{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def cyanBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Back.CYAN}{Fore.WHITE}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def yellowBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Back.YELLOW}{Fore.WHITE}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def blueBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Back.BLUE}{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def greenBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Back.GREEN}{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def whiteBackReturn(*vars):
        var = " ".join(map(str, vars))
        
        return f"{Back.WHITE}{Fore.BLACK}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def redTagReturn(tag,var):
        return f"[{tag}] {Fore.RED}{var}{Style.RESET_ALL}"
     
    @staticmethod
    def pinkTagReturn(tag,var):
        return f"[{tag}] \033[38;5;206m{var}\033[0m"
    
    @staticmethod
    def cyanTagReturn(tag,var):
        return f"[{tag}] {Fore.CYAN}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def yellowTagReturn(tag,var):
        return f"[{tag}] {Fore.YELLOW}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def blueTagReturn(tag,var):
        return f"[{tag}] {Fore.BLUE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def greenTagReturn(tag,var):
        return f"[{tag}] {Fore.GREEN}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def whiteTagReturn(tag,var):
        return f"[{tag}] {Fore.WHITE}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def redFatTagReturn(tag,var):
        return f"{Back.RED}[{tag}]{Style.RESET_ALL} {Fore.RED}{var}{Style.RESET_ALL}"
   
    @staticmethod
    def pinkFatTagReturn(tag, var):
        return f"\033[48;5;206m[{tag}]\033[0m \033[38;5;206m{var}\033[0m"
    
    @staticmethod
    def cyanFatTagReturn(tag,var):
        return f"{Back.CYAN}[{tag}]{Style.RESET_ALL} {Fore.CYAN}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def yellowFatTagReturn(tag,var):
        return f"{Back.YELLOW}[{tag}]{Style.RESET_ALL} {Fore.YELLOW}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def blueFatTagReturn(tag,var):
        return f"{Back.BLUE}[{tag}]{Style.RESET_ALL} {Fore.BLUE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def greenFatTagReturn(tag,var):
        return f"{Back.GREEN}[{tag}]{Style.RESET_ALL} {Fore.GREEN}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def whiteFatTagReturn(tag,var):
        return f"{Back.WHITE}[{tag}]{Style.RESET_ALL} {Fore.WHITE}{var}{Style.RESET_ALL}"