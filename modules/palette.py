from colorama import Fore,Style,Back   


class Palette:
    
    @staticmethod
    def red(var):
        print(f"{Fore.RED}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def pink(var):
        print(f"\033[38;5;206m{var}\033[0m")
    
    @staticmethod
    def cyan(var):
        print(f"{Fore.CYAN}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def yellow(var):
        print(f"{Fore.YELLOW}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def blue(var):
        print(f"{Fore.BLUE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def green(var):
        print(f"{Fore.GREEN}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def white(var):
        print(f"{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def redBack(var):
        print(f"{Back.RED}{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def pinkBack(var):
        print(f"\033[48;5;206m{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def cyanBack(var):
        print(f"{Back.CYAN}{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def yellowBack(var):
        print(f"{Back.YELLOW}{Fore.WHITE}{var}{Style.RESET_ALL}")
        
    @staticmethod
    def blueBack(var):
        print(f"{Back.BLUE}{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def greenBack(var):
        print(f"{Back.GREEN}{Fore.WHITE}{var}{Style.RESET_ALL}")
    
    @staticmethod
    def whiteBack(var):
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
    def redReturn(var):
        return f"{Fore.RED}{var}{Style.RESET_ALL}"
     
    @staticmethod
    def pinkReturn(var):
        return f"\033[38;5;206m{var}\033[0m"
    
    @staticmethod
    def cyanReturn(var):
        return f"{Fore.CYAN}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def yellowReturn(var):
        return f"{Fore.YELLOW}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def blueReturn(var):
        return f"{Fore.BLUE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def greenReturn(var):
        return f"{Fore.GREEN}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def whiteReturn(var):
        return f"{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def redBackReturn(var):
        return f"{Back.RED}{Fore.WHITE}{var}{Style.RESET_ALL}"
     
    @staticmethod
    def pinkBackReturn(var):
        return f"\033[48;5;206m{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def cyanBackReturn(var):
        return f"{Back.CYAN}{Fore.WHITE}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def yellowBackReturn(var):
        return f"{Back.YELLOW}{Fore.WHITE}{var}{Style.RESET_ALL}"
        
    @staticmethod
    def blueBackReturn(var):
        return f"{Back.BLUE}{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def greenBackReturn(var):
        return f"{Back.GREEN}{Fore.WHITE}{var}{Style.RESET_ALL}"
    
    @staticmethod
    def whiteBackReturn(var):
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
