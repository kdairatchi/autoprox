import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import requests
import subprocess
import threading
import os

# Function to run a command asynchronously
def run_command(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout.decode() if stdout else stderr.decode()

class AutoProxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoProx - Ultimate Privacy Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        # Banner
        banner = tk.Label(self.root, text="AutoProx - The Ultimate Proxy Management & Privacy Tool",
                          font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2980b9", pady=10)
        banner.pack(fill="x")

        # Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Adding Tabs
        self.create_scraper_tab()
        self.create_validation_tab()
        self.create_configuration_tab()
        self.create_run_command_tab()
        self.create_checker_tab()

    def create_scraper_tab(self):
        # Proxy Scraper Tab
        scraper_tab = ttk.Frame(self.notebook)
        self.notebook.add(scraper_tab, text="Proxy Scraper")

        label = tk.Label(scraper_tab, text="Scrape Proxies from Public Sources", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        self.scraped_text = scrolledtext.ScrolledText(scraper_tab, height=15, width=80)
        self.scraped_text.pack()

        scrape_button = tk.Button(scraper_tab, text="Scrape Proxies", command=self.scrape_proxies, bg="#27ae60", fg="white")
        scrape_button.pack(pady=10)

    def create_validation_tab(self):
        # Proxy Validation Tab
        validation_tab = ttk.Frame(self.notebook)
        self.notebook.add(validation_tab, text="Proxy Validation")

        label = tk.Label(validation_tab, text="Validate Scraped Proxies", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        self.valid_proxies_text = scrolledtext.ScrolledText(validation_tab, height=15, width=80)
        self.valid_proxies_text.pack()

        validate_button = tk.Button(validation_tab, text="Validate Proxies", command=self.validate_proxies, bg="#f39c12", fg="white")
        validate_button.pack(pady=10)

    def create_configuration_tab(self):
        # Proxychains Configuration Tab
        config_tab = ttk.Frame(self.notebook)
        self.notebook.add(config_tab, text="Proxychains Configuration")

        label = tk.Label(config_tab, text="Configure Proxychains with Validated Proxies", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        config_button = tk.Button(config_tab, text="Generate Configuration", command=self.generate_proxychains_conf, bg="#e74c3c", fg="white")
        config_button.pack(pady=10)

        self.config_status = tk.Label(config_tab, text="", font=("Arial", 12))
        self.config_status.pack(pady=10)

    def create_run_command_tab(self):
        # Run Command Tab
        run_tab = ttk.Frame(self.notebook)
        self.notebook.add(run_tab, text="Run with Proxychains")

        label = tk.Label(run_tab, text="Run a Command through Proxychains", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        self.command_entry = tk.Entry(run_tab, width=50)
        self.command_entry.pack(pady=5)

        run_button = tk.Button(run_tab, text="Run Command", command=self.run_command_proxychains, bg="#3498db", fg="white")
        run_button.pack(pady=10)

        self.run_output_text = scrolledtext.ScrolledText(run_tab, height=15, width=80)
        self.run_output_text.pack()

    def create_checker_tab(self):
        # IP and DNS Checker Tab
        checker_tab = ttk.Frame(self.notebook)
        self.notebook.add(checker_tab, text="Check IP/DNS")

        label = tk.Label(checker_tab, text="Check Current IP & DNS Leak", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        ip_button = tk.Button(checker_tab, text="Check Current IP", command=self.check_ip, bg="#9b59b6", fg="white")
        ip_button.pack(pady=5)

        dns_button = tk.Button(checker_tab, text="Check DNS Leak", command=self.check_dns, bg="#8e44ad", fg="white")
        dns_button.pack(pady=5)

        self.check_output_text = scrolledtext.ScrolledText(checker_tab, height=15, width=80)
        self.check_output_text.pack()

    # Proxy Scraper Functionality
    def scrape_proxies(self):
        self.scraped_text.delete(1.0, tk.END)
        sources = [
            "https://www.proxy-list.download/api/v1/get?type=https",
            "https://www.sslproxies.org/",
            "https://free-proxy-list.net/",
            "https://www.us-proxy.org/"
        ]
        proxies = set()

        for source in sources:
            try:
                response = requests.get(source)
                proxies.update(response.text.split())
            except Exception as e:
                print(f"Error fetching from {source}: {e}")

        for proxy in proxies:
            self.scraped_text.insert(tk.END, proxy + "\n")

    # Proxy Validation Functionality
    def validate_proxies(self):
        self.valid_proxies_text.delete(1.0, tk.END)
        scraped_proxies = self.scraped_text.get(1.0, tk.END).strip().split("\n")
        valid_proxies = []

        def check_proxy(proxy):
            try:
                response = requests.get("http://www.google.com", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
                if response.status_code == 200:
                    valid_proxies.append(proxy)
                    self.valid_proxies_text.insert(tk.END, proxy + "\n")
            except:
                pass

        threads = []
        for proxy in scraped_proxies:
            t = threading.Thread(target=check_proxy, args=(proxy,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # Generate Proxychains Configuration
    def generate_proxychains_conf(self):
        valid_proxies = self.valid_proxies_text.get(1.0, tk.END).strip().split("\n")
        if not valid_proxies:
            self.config_status.config(text="No valid proxies found to configure Proxychains.", fg="red")
            return

        try:
            with open("/etc/proxychains.conf", "w") as f:
                f.write("[ProxyList]\n")
                for proxy in valid_proxies:
                    ip, port = proxy.split(":")
                    f.write(f"socks5 {ip} {port}\n")

            self.config_status.config(text="Proxychains configuration updated successfully!", fg="
