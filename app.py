# ===========> DON'T CHANGE THIS
# SCRIPT : VALIDATOR EMAIL APPLEID
# VERSION : 2.5
# TELEGRAM AUTHOR : https://t.me/zlaxtert
# SITE : https://darkxcode.site/
# TEAM : DARKXCODE
# ================> END

import requests
import threading
import time
import os
import json
import configparser
from colorama import Fore, Back, Style, init
from queue import Queue
from urllib.parse import quote

# Initialize colorama
init(autoreset=True)

# Colors
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
kuning = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX
cyan = Fore.CYAN
reset = Fore.RESET
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
res = Style.RESET_ALL
yl = Fore.YELLOW
cy = Fore.CYAN
mg = Fore.MAGENTA
bc = Back.GREEN
fr = Fore.RED
sr = Style.RESET_ALL
fb = Fore.BLUE
fc = Fore.LIGHTCYAN_EX
fg = Fore.GREEN
br = Back.RED

# Banner
banner = f"""{hijau}
                                 /           /                          
                                /' .,,,,  ./ \\                           
                               /';'     ,/  \\                                
                              / /   ,,//,'''                         
                             ( ,, '_,  ,,,' ''                 
                             |    /{merah}@{hijau}  ,,, ;' '               
                            /    .   ,''/' ',''       
                           /   .     ./, ',, ' ;                      
                        ,./  .   ,-,',' ,,/''\\,'                 
                       |   /; ./,,'',,'' |   |                                               
                       |     /   ','    /    |                                               
                        \\___/'   '     |     |                                               
                         ',,'  |      /     '\\                                              
                              /  (   |   )    ~\\            
                             '   \\   (    \\     \\~            
                             :    \\                \\                                                 
                              ; .         \\--                                                  
                               :   \\         ; {magenta}                                                 
,------.    ,---.  ,------. ,--. ,--.,--.   ,--. ,-----.  ,-----. ,------.  ,------. 
|  .-.  \\  /  O  \\ |  .--. '|  .'   / \\  `.'  / '  .--./ '  .-.  '|  .-.  \\ |  .---' 
|  |  \\  :|  .-.  ||  '--'.'|  .   '   .'    \\  |  |     |  | |  ||  |  \\  :|  `--,  
|  '--'  /|  | |  ||  |\\  \\ |  |\\   \\ /  .'.  \\ '  '--'\\ '  '-'  '|  '--'  /|  `---. 
`-------' `--' `--'`--' '--'`--' '--''--'   '--' `-----'  `-----' `-------' `------' {reset}
{fr}       ===================================================================={reset}
                  |{fb} SCRIPT{reset}  :{fg} VALIDATOR EMAIL APPLE          {reset} |
                  |{fb} VERSION{reset} :{fg} 2.5{reset}                             |
                  |{fb} AUTHOR {reset} :{fg} https://t.me/zlaxtert{reset}           |
{fr}       ===================================================================={reset}
"""


class AppleIDValidator:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.load_config()
        self.lists_queue = Queue()
        self.proxies = []
        self.live_count = 0
        self.die_count = 0
        self.error_count = 0
        self.retry_count = 0
        self.total_count = 0
        self.checked_count = 0
        self.lock = threading.Lock()
        self.threads_count = 0
        
    def load_config(self):
        """Reading configuration from settings.ini"""
        if not os.path.exists('settings.ini'):
            self.create_default_config()
        self.config.read('settings.ini')
        
        # Validate required settings
        if self.config['SETTINGS']['APIKEY'] == 'PASTE_YOUR_API_KEY_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API key in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        elif self.config['SETTINGS']['API'] == 'PASTE_YOUR_API_HERE':
            print(f"{res}[{yl}!{res}]{fb} Please configure your API in {yl}settings.ini{fb} {res}[{yl}!{res}]{fb}\n\n")
            exit()
        
    def create_default_config(self):
        """Creating a default configuration file"""
        self.config['SETTINGS'] = {
            'APIKEY': 'PASTE_YOUR_API_KEY_HERE',
            'API': 'PASTE_YOUR_API_HERE',
            'PATCH': '/validator/apple/',
            'PROXY_AUTH': 'PASTE_YOUR_PROXY_AUTH_HERE',
            'TYPE_PROXY': 'http'
        }
        
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
            
        # Create a results folder
        os.makedirs('result', exist_ok=True)
    
    def load_lists(self, filename):
        """Loading email list from file"""
        if not os.path.exists(filename):
            print(f"{res}[{yl}!{res}]{fb} File {fg}{filename}{res}{fb} not found {res}[{yl}!{res}]{fb}")
            return False
            
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    item = line.strip()
                    if item and '@' in item:  # Basic email validation
                        self.lists_queue.put(item)
        except Exception as e:
            print(f"{res}[{yl}!{res}]{fb} Error reading file {fg}{filename}{res}{fb}: {str(e)} {res}[{yl}!{res}]{fb}")
            return False
                    
        self.total_count = self.lists_queue.qsize()
        if self.total_count == 0:
            print(f"{res}[{yl}!{res}]{fb} No valid email addresses found in {fg}{filename}{res}{fb} {res}[{yl}!{res}]{fb}")
            return False
            
        print(f"{res}[{yl}!{res}]{fb} Successfully loaded {fg}{self.total_count}{res}{fb} lists from {fc}{filename} {res}[{yl}!{res}]{fb}")
        return True
        
    def load_proxies(self, filename):
        """Loading proxy list from file"""
        if not os.path.exists(filename):
            print(f"{res}[{yl}!{res}]{fb} File {fg}{filename}{res}{fb} not found {res}[{yl}!{res}]{fb}")
            return False
            
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    proxy = line.strip()
                    if proxy:
                        self.proxies.append(proxy)
        except Exception as e:
            print(f"{res}[{yl}!{res}]{fb} Error reading proxy file {fg}{filename}{res}{fb}: {str(e)} {res}[{yl}!{res}]{fb}")
            return False
                    
        print(f"{res}[{yl}!{res}]{fb} Successfully loaded {fg}{len(self.proxies)}{res}{fb} proxies {res}[{yl}!{res}]{fb}")
        return True
        
    def validate_item(self, item, proxy_index=0):
        """Validate a single item using the API"""
        apikey = self.config['SETTINGS']['APIKEY']
        api_url = self.config['SETTINGS']['API']
        patch_url = self.config['SETTINGS']['PATCH']
        proxy_auth = self.config['SETTINGS']['PROXY_AUTH']
        type_proxy = self.config['SETTINGS']['TYPE_PROXY']
        
        endpoint = api_url.rstrip('/') + '/' + patch_url.lstrip('/')
        
        # Set up parameters
        params = {
            'list': item,
            'apikey': apikey,
        }
        
        # Headers 
        headers = {
            'Accept': 'text/plain',
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        }
        
        # Add proxy if available
        proxies_dict = None
        if self.proxies:
            proxy = self.proxies[proxy_index % len(self.proxies)]
            params['proxy'] = proxy
            params['type_proxy'] = type_proxy
            
            # Add auth proxy if available
            if proxy_auth and proxy_auth != 'PASTE_YOUR_PROXY_AUTH_HERE':
                params['proxyAuth'] = proxy_auth
        
        try:        
            time.sleep(0.5)  # Reduced sleep time for better performance
            response = requests.get(endpoint, params=params, headers=headers, timeout=50)
            
            
            # Check if response is valid JSON
            try:
                data = response.json()
            except json.JSONDecodeError:
                with self.lock:
                    self.error_count += 1
                    self.checked_count += 1
                    
                self.save_result('result/ERROR.txt', f"{item} | INVALID JSON RESPONSE")
                print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}INVALID JSON RESPONSE{res}")
                return
            
            if 'data' in response.text:
                info = data['data']
                
                type_val = info.get('type', 'EMAIL')
                status = info.get('status', '')
                msg = info.get('msg', 'UNKNOWN')
                    
                if status.upper() == "LIVE":
                    val = f"{hijau}True{reset}"
                    with self.lock:
                        self.live_count += 1
                    self.save_result('result/LIVE.txt', item)
                    stats = f"{hijau}LIVE{reset}"
                elif status.upper() == "DIE":
                    val = f"{merah}False{reset}"
                    with self.lock:
                        self.die_count += 1
                    self.save_result('result/DIE.txt', item)
                    stats = f"{merah}DIE{reset}"
                elif status.upper() == "RETRY":
                    val = f"{cyan}Retry{reset}"
                    with self.lock:
                        self.retry_count += 1
                    self.save_result('result/RETRY.txt', item)
                    stats = f"{cyan}RETRY{reset}"
                else:
                    val = f"{white}Unknown{reset}"
                    with self.lock:
                        self.error_count += 1
                    self.save_result('result/ERROR.txt', item)
                    stats = f"{white}ERROR{reset}"
                        
                # Show results
                with self.lock:
                    self.checked_count += 1
                        
                # Display progress
                progress = f" {yl}Checked{res} | {hijau}LIVE: {self.live_count}{res} | {merah}DIE: {self.die_count}{res} | {white}RETRY: {self.retry_count}{res} | {magenta}ERROR: {self.error_count}{res} | {res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]"
                print(f"{progress}{res} -{yl} {item}{res} -> {stats} | {magenta}VALID{reset} : {val} | {yl}MSG{reset} : {msg}")
                          
            else:
                # Handle case where data structure is different
                with self.lock:
                    self.error_count += 1
                    self.checked_count += 1
                    
                self.save_result('result/ERROR.txt', f"{item} | INVALID RESPONSE STRUCTURE")
                print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}INVALID RESPONSE STRUCTURE{res}")
                
        except requests.exceptions.Timeout:
            with self.lock:
                self.error_count += 1
                self.checked_count += 1
                    
            self.save_result('result/ERROR.txt', f"{item} | REQUEST TIMEOUT")
            print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}REQUEST TIMEOUT{res}")
            
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.error_count += 1
                self.checked_count += 1
                    
            self.save_result('result/ERROR.txt', f"{item} | REQUEST ERROR: {str(e)}")
            print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}NETWORK ERROR{res}")
            
        except Exception as e:
            with self.lock:
                self.error_count += 1
                self.checked_count += 1
                    
            self.save_result('result/ERROR.txt', f"{item} | VALIDATION ERROR: {str(e)}")
            print(f"{res}[{fr}{self.checked_count}{res}/{fg}{self.total_count}{res}]{res} -{yl} {item}{res} -> {white}ERROR{reset} | {merah}VALIDATION ERROR{res}")
            
    def save_result(self, filename, data):
        """Save results to file"""
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(data + '\n')
        except Exception as e:
            print(f"{res}[{yl}!{res}]{fb} Error saving to {filename}: {str(e)} {res}[{yl}!{res}]{fb}")
            
    def worker(self):
        """Worker thread to process validation"""
        proxy_index = 0
        while True:
            try:
                item = self.lists_queue.get_nowait()
            except:
                break
                
            self.validate_item(item, proxy_index)
            proxy_index += 1
            self.lists_queue.task_done()
            
    def print_stats(self):
        """Print statistics during execution"""
        while not self.lists_queue.empty() or threading.active_count() > 1:
            time.sleep(2)
            # Stats are now printed in real-time in validate_item method
            
    def run(self):
        """Running validation process"""
        # Input file lists
        lists_file = input(f"{res}[{yl}+{res}]{fb} Enter Email lists file{fg} >> {fb}").strip()
        if not self.load_lists(lists_file):
            return
            
        # Input proxy file
        proxy_file = input(f"{res}[{yl}+{res}]{fb} Enter Proxy lists file (press Enter to skip){fg} >> {fb}").strip()
        if proxy_file and not self.load_proxies(proxy_file):
            return
            
        # Input number of threads
        try:
            self.threads_count = int(input(f"{res}[{yl}+{res}]{fb} Enter number of Threads (5-25) (Recommended 5-10){fg} >> {fb}").strip() or "5")
            self.threads_count = max(5, min(25, self.threads_count))  # Limit between 5-25
        except ValueError:
            print(f"{res}[{yl}!{res}]{fb} Invalid number of threads, using default 5 threads {res}[{yl}!{res}]{fb}")
            self.threads_count = 5
            
        # Make sure the result folder exists
        os.makedirs('result', exist_ok=True)
        print(f"\n{yl}RUNNING API FROM {fg}{self.config['SETTINGS']['API']}{res}")
        print(f"{yl}USE PATCH API {fg}{self.config['SETTINGS']['PATCH']}{res}")
        print(f"{fr}={res}" * 60)
        print(f"{yl}Starting validation with {fg}{self.threads_count}{yl} threads{res}")
        print(f"{fr}={res}" * 60)
        
        start_time = time.time()
        
        # Create and run threads
        threads = []
        for i in range(self.threads_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Start stats thread
        stats_thread = threading.Thread(target=self.print_stats)
        stats_thread.daemon = True
        stats_thread.start()
            
        # Wait for all threads to finish
        self.lists_queue.join()
        
        # Small delay to ensure all threads complete
        time.sleep(2)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n{fr}={res}" * 60)
        print(f"{hijau}Checking completed!{reset}")
        print(f"{yl}Live: {fg}{self.live_count}{reset} | {yl}Die: {fr}{self.die_count}{reset} | {yl}Retry: {white}{self.retry_count}{reset} | {yl}Error: {fr}{self.error_count}{reset}")
        print(f"{yl}Time taken: {elapsed_time:.2f} seconds{reset}")
        print(f"{res}[{yl}!{res}]{fb} Results saved in 'result' folder {res}[{yl}!{res}]{fb}")
        print(f"{fr}={res}" * 60)


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    validator = AppleIDValidator()
    validator.run()