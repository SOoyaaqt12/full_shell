#!/usr/bin/env python3
"""
DaffaShell Pro v2.0
A feature-rich, cross-platform terminal shell with advanced capabilities.
Author: Enhanced by Claude
"""

import os
import sys
import shlex
import subprocess
import threading
import time
import random
import glob
import shutil
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Callable

# Readline support with fallback
try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None

from colorama import init as colorama_init, Fore, Back, Style

colorama_init(autoreset=True)

# ==================== CONFIGURATION ====================
CONFIG = {
    "prompt_symbol": "λ",
    "history_file": os.path.expanduser("~/.daffashell_history"),
    "config_file": os.path.expanduser("~/.daffashell_config.json"),
    "max_history": 2000,
    "auto_suggestions": True,
    "colored_output": True,
    "safe_mode": False,
}

# Theme system
THEMES = {
    "neon": {
        "accent": Fore.CYAN,
        "muted": Fore.WHITE,
        "info": Fore.MAGENTA,
        "warn": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.GREEN,
        "prompt": Fore.CYAN,
        "dir": Fore.BLUE,
    },
    "matrix": {
        "accent": Fore.GREEN,
        "muted": Fore.LIGHTGREEN_EX,
        "info": Fore.GREEN,
        "warn": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.LIGHTGREEN_EX,
        "prompt": Fore.GREEN,
        "dir": Fore.GREEN,
    },
    "dracula": {
        "accent": Fore.MAGENTA,
        "muted": Fore.WHITE,
        "info": Fore.CYAN,
        "warn": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.GREEN,
        "prompt": Fore.MAGENTA,
        "dir": Fore.CYAN,
    },
    "classic": {
        "accent": Fore.WHITE,
        "muted": Fore.LIGHTWHITE_EX,
        "info": Fore.CYAN,
        "warn": Fore.YELLOW,
        "error": Fore.RED,
        "success": Fore.GREEN,
        "prompt": Fore.WHITE,
        "dir": Fore.BLUE,
    },
}

# ==================== GLOBAL STATE ====================
class ShellState:
    def __init__(self):
        self.aliases: Dict[str, str] = {}
        self.env_vars: Dict[str, str] = {}
        self.last_cwd = os.getcwd()
        self.last_exit_code = 0
        self.current_theme = "neon"
        self.history: List[str] = []
        self.pipelines_enabled = True
        
    def get_theme(self) -> Dict[str, str]:
        return THEMES.get(self.current_theme, THEMES["neon"])

state = ShellState()

# ==================== UTILITIES ====================
def print_colored(text: str, style: str = "muted", end: str = "\n"):
    """Print colored text using current theme."""
    theme = state.get_theme()
    color = theme.get(style, Fore.WHITE)
    print(f"{color}{text}{Style.RESET_ALL}", end=end)

def typewriter(text: str, delay: float = 0.01, style: str = "muted"):
    """Typewriter effect for dramatic output."""
    theme = state.get_theme()
    color = theme.get(style, Fore.WHITE)
    for ch in text:
        sys.stdout.write(color + ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Style.RESET_ALL + "\n")
    sys.stdout.flush()

def progress_bar(label: str, duration: float = 2.0):
    """Animated progress bar."""
    theme = state.get_theme()
    steps = max(1, int(duration / 0.05))
    for i in range(steps + 1):
        pct = int(i / steps * 100)
        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "[" + "█" * filled + "░" * (bar_len - filled) + "]"
        sys.stdout.write(f"\r{theme['info']}{label} {bar} {pct}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("\n")

def format_size(bytes_size: int) -> str:
    """Format byte size to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def splash():
    """Display startup splash screen."""
    theme = state.get_theme()
    logo = [
        "  ____   __  ______ ______ __     _____ _    _ ______ _      _      ",
        " |  _ \\ / _\\|  ____|  ____/ _\\   / ____| |  | |  ____| |    | |     ",
        " | | | | |  | |__  | |__ | |    | (___ | |__| | |__  | |    | |     ",
        " | | | | |  |  __| |  __|| |     \\___ \\|  __  |  __| | |    | |     ",
        " | |_| | |  | |    | |   | |     ____) | |  | | |____| |____| |____ ",
        " |____/|_|  |_|    |_|   |_|    |_____/|_|  |_|______|______|______|",
    ]
    for i, line in enumerate(logo):
        color = theme["accent"] if i % 2 == 0 else theme["info"]
        print(color + line)
    
    print(f"\n{theme['accent']}{'─' * 70}{Style.RESET_ALL}")
    print(f"{theme['info']}  DaffaShell Pro v2.0 - Advanced Command Line Interface{Style.RESET_ALL}")
    print(f"{theme['muted']}  Type 'help' for commands | 'exit' to quit{Style.RESET_ALL}")
    print(f"{theme['accent']}{'─' * 70}{Style.RESET_ALL}\n")

def get_prompt() -> str:
    """Generate colored prompt string."""
    theme = state.get_theme()
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]
    
    user = os.getenv("USERNAME") or os.getenv("USER") or "user"
    try:
        host = os.uname().nodename
    except:
        host = os.getenv("COMPUTERNAME", "localhost")
    
    # Show git branch if in git repo
    git_branch = get_git_branch()
    git_info = f" {theme['warn']}({git_branch})" if git_branch else ""
    
    # Exit code indicator
    exit_indicator = ""
    if state.last_exit_code != 0:
        exit_indicator = f" {theme['error']}[{state.last_exit_code}]"
    
    return (f"{theme['accent']}┌─[{theme['success']}{user}{theme['muted']}@{theme['success']}{host}"
            f"{theme['accent']}]─[{theme['dir']}{cwd}{theme['accent']}]{git_info}{exit_indicator}\n"
            f"{theme['accent']}└─{theme['prompt']}{CONFIG['prompt_symbol']}{Style.RESET_ALL} ")

def get_git_branch() -> Optional[str]:
    """Get current git branch if in a git repository."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=1
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None

# ==================== HISTORY & CONFIG ====================
def load_history():
    """Load command history from file."""
    if not readline:
        return
    try:
        if os.path.exists(CONFIG["history_file"]):
            readline.read_history_file(CONFIG["history_file"])
            readline.set_history_length(CONFIG["max_history"])
    except:
        pass

def save_history():
    """Save command history to file."""
    if not readline:
        return
    try:
        readline.write_history_file(CONFIG["history_file"])
    except:
        pass

def load_config():
    """Load configuration from JSON file."""
    try:
        if os.path.exists(CONFIG["config_file"]):
            with open(CONFIG["config_file"], 'r') as f:
                data = json.load(f)
                state.aliases = data.get("aliases", {})
                state.env_vars = data.get("env_vars", {})
                state.current_theme = data.get("theme", "neon")
                CONFIG.update(data.get("config", {}))
    except Exception as e:
        print_colored(f"Config load error: {e}", "warn")

def save_config():
    """Save configuration to JSON file."""
    try:
        data = {
            "aliases": state.aliases,
            "env_vars": state.env_vars,
            "theme": state.current_theme,
            "config": CONFIG,
        }
        with open(CONFIG["config_file"], 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print_colored(f"Config save error: {e}", "warn")

# ==================== TAB COMPLETION ====================
def completer(text: str, state_idx: int) -> Optional[str]:
    """Enhanced tab completion."""
    options = []
    
    # Get all builtin commands
    builtins = list(BUILTINS.keys())
    
    # Add aliases
    builtins.extend(state.aliases.keys())
    
    # Add commands from PATH
    if not text or not any(c in text for c in ['/', '\\', '~']):
        # Command completion
        for cmd in builtins:
            if cmd.startswith(text):
                options.append(cmd)
        
        # System commands
        if sys.platform != "win32":
            try:
                paths = os.environ.get("PATH", "").split(":")
                for path in paths[:10]:  # Limit to avoid slowdown
                    if os.path.isdir(path):
                        for item in os.listdir(path):
                            if item.startswith(text):
                                options.append(item)
            except:
                pass
    
    # File/directory completion
    try:
        pattern = os.path.expanduser(text + "*")
        matches = glob.glob(pattern)
        options.extend(matches)
    except:
        pass
    
    options = sorted(set(options))
    return options[state_idx] if state_idx < len(options) else None

# ==================== COMMAND EXECUTION ====================
def run_command(cmd: List[str], capture: bool = False) -> subprocess.CompletedProcess:
    """Execute a command and return the result."""
    try:
        if capture:
            return subprocess.run(cmd, capture_output=True, text=True)
        else:
            return subprocess.run(cmd)
    except FileNotFoundError:
        print_colored(f"Command not found: {cmd[0]}", "error")
        return subprocess.CompletedProcess(cmd, 127, "", "")
    except Exception as e:
        print_colored(f"Execution error: {e}", "error")
        return subprocess.CompletedProcess(cmd, 1, "", "")

def parse_pipeline(line: str) -> List[List[str]]:
    """Parse command line with pipes."""
    commands = []
    current = []
    tokens = shlex.split(line)
    
    for token in tokens:
        if token == "|":
            if current:
                commands.append(current)
                current = []
        else:
            current.append(token)
    
    if current:
        commands.append(current)
    
    return commands

def execute_pipeline(commands: List[List[str]]):
    """Execute a pipeline of commands."""
    if len(commands) == 1:
        result = run_command(commands[0])
        state.last_exit_code = result.returncode
        return
    
    # Pipeline execution
    processes = []
    for i, cmd in enumerate(commands):
        stdin = processes[-1].stdout if i > 0 else None
        stdout = subprocess.PIPE if i < len(commands) - 1 else None
        
        try:
            proc = subprocess.Popen(cmd, stdin=stdin, stdout=stdout)
            processes.append(proc)
            
            if i > 0:
                processes[-2].stdout.close()
        except Exception as e:
            print_colored(f"Pipeline error: {e}", "error")
            state.last_exit_code = 1
            return
    
    if processes:
        processes[-1].wait()
        state.last_exit_code = processes[-1].returncode

# ==================== BUILTIN COMMANDS ====================
def builtin_clear(args: List[str]):
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")
    state.last_exit_code = 0

def builtin_cd(args: List[str]):
    """Change directory."""
    try:
        if not args:
            target = os.path.expanduser("~")
        elif args[0] == "-":
            target, state.last_cwd = state.last_cwd, os.getcwd()
        else:
            target = os.path.expandvars(os.path.expanduser(args[0]))
        
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(os.getcwd(), target))
        
        state.last_cwd = os.getcwd()
        os.chdir(target)
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"cd: {e}", "error")
        state.last_exit_code = 1

def builtin_ls(args: List[str]):
    """Enhanced directory listing."""
    path = args[0] if args else "."
    try:
        items = sorted(os.listdir(path))
        theme = state.get_theme()
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                print(f"{theme['dir']}{item}/{Style.RESET_ALL}")
            elif os.access(full_path, os.X_OK):
                print(f"{theme['success']}{item}*{Style.RESET_ALL}")
            else:
                print(f"{theme['muted']}{item}{Style.RESET_ALL}")
        
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"ls: {e}", "error")
        state.last_exit_code = 1

def builtin_pwd(args: List[str]):
    """Print working directory."""
    print_colored(os.getcwd(), "info")
    state.last_exit_code = 0

def builtin_echo(args: List[str]):
    """Echo arguments."""
    print(" ".join(args))
    state.last_exit_code = 0

def builtin_cat(args: List[str]):
    """Display file contents."""
    if not args:
        print_colored("cat: missing file operand", "error")
        state.last_exit_code = 1
        return
    
    try:
        for file in args:
            with open(file, 'r') as f:
                print(f.read(), end='')
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"cat: {e}", "error")
        state.last_exit_code = 1

def builtin_mkdir(args: List[str]):
    """Create directories."""
    if not args:
        print_colored("mkdir: missing operand", "error")
        state.last_exit_code = 1
        return
    
    try:
        for dir in args:
            os.makedirs(dir, exist_ok=True)
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"mkdir: {e}", "error")
        state.last_exit_code = 1

def builtin_rm(args: List[str]):
    """Remove files or directories."""
    if not args:
        print_colored("rm: missing operand", "error")
        state.last_exit_code = 1
        return
    
    recursive = "-r" in args or "-rf" in args
    force = "-f" in args or "-rf" in args
    
    files = [a for a in args if not a.startswith("-")]
    
    try:
        for item in files:
            if os.path.isdir(item):
                if recursive:
                    shutil.rmtree(item)
                else:
                    print_colored(f"rm: {item} is a directory (use -r)", "error")
            else:
                os.remove(item)
        state.last_exit_code = 0
    except Exception as e:
        if not force:
            print_colored(f"rm: {e}", "error")
            state.last_exit_code = 1

def builtin_cp(args: List[str]):
    """Copy files."""
    if len(args) < 2:
        print_colored("cp: missing operand", "error")
        state.last_exit_code = 1
        return
    
    try:
        src, dst = args[0], args[1]
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"cp: {e}", "error")
        state.last_exit_code = 1

def builtin_mv(args: List[str]):
    """Move/rename files."""
    if len(args) < 2:
        print_colored("mv: missing operand", "error")
        state.last_exit_code = 1
        return
    
    try:
        shutil.move(args[0], args[1])
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"mv: {e}", "error")
        state.last_exit_code = 1

def builtin_find(args: List[str]):
    """Find files by pattern."""
    pattern = args[0] if args else "*"
    path = args[1] if len(args) > 1 else "."
    
    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                if glob.fnmatch.fnmatch(name, pattern):
                    print_colored(os.path.join(root, name), "info")
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"find: {e}", "error")
        state.last_exit_code = 1

def builtin_grep(args: List[str]):
    """Search for pattern in files."""
    if len(args) < 2:
        print_colored("grep: missing operand", "error")
        state.last_exit_code = 1
        return
    
    pattern, file = args[0], args[1]
    try:
        with open(file, 'r') as f:
            for i, line in enumerate(f, 1):
                if re.search(pattern, line):
                    print(f"{i}: {line}", end='')
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"grep: {e}", "error")
        state.last_exit_code = 1

def builtin_env(args: List[str]):
    """Display or set environment variables."""
    if not args:
        for k, v in sorted(os.environ.items()):
            print(f"{k}={v}")
    else:
        for arg in args:
            if "=" in arg:
                key, val = arg.split("=", 1)
                os.environ[key] = val
                state.env_vars[key] = val
    state.last_exit_code = 0

def builtin_export(args: List[str]):
    """Export environment variables."""
    builtin_env(args)

def builtin_alias(args: List[str]):
    """Create or list aliases."""
    if not args:
        for k, v in sorted(state.aliases.items()):
            print(f"{k}={v}")
        state.last_exit_code = 0
        return
    
    line = " ".join(args)
    if "=" in line:
        name, cmd = line.split("=", 1)
        name = name.strip()
        cmd = cmd.strip().strip("'\"")
        state.aliases[name] = cmd
        save_config()
        print_colored(f"Alias created: {name} -> {cmd}", "success")
    else:
        name = args[0]
        cmd = " ".join(args[1:])
        state.aliases[name] = cmd
        save_config()
        print_colored(f"Alias created: {name} -> {cmd}", "success")
    
    state.last_exit_code = 0

def builtin_unalias(args: List[str]):
    """Remove aliases."""
    if not args:
        print_colored("unalias: missing operand", "error")
        state.last_exit_code = 1
        return
    
    for name in args:
        if name in state.aliases:
            del state.aliases[name]
            save_config()
            print_colored(f"Alias removed: {name}", "success")
        else:
            print_colored(f"unalias: {name} not found", "warn")
    
    state.last_exit_code = 0

def builtin_history(args: List[str]):
    """Display command history."""
    if not readline:
        print_colored("History not available", "warn")
        return
    
    limit = int(args[0]) if args and args[0].isdigit() else 50
    total = readline.get_current_history_length()
    start = max(1, total - limit)
    
    for i in range(start, total + 1):
        item = readline.get_history_item(i)
        if item:
            print(f"{i:5d}  {item}")
    
    state.last_exit_code = 0

def builtin_theme(args: List[str]):
    """Change color theme."""
    if not args:
        print("Available themes:", ", ".join(THEMES.keys()))
        print(f"Current theme: {state.current_theme}")
        state.last_exit_code = 0
        return
    
    theme_name = args[0]
    if theme_name in THEMES:
        state.current_theme = theme_name
        save_config()
        print_colored(f"Theme changed to: {theme_name}", "success")
        state.last_exit_code = 0
    else:
        print_colored(f"Unknown theme: {theme_name}", "error")
        state.last_exit_code = 1

def builtin_sysinfo(args: List[str]):
    """Display system information."""
    import platform
    theme = state.get_theme()
    
    print(f"\n{theme['accent']}{'═' * 50}{Style.RESET_ALL}")
    print(f"{theme['info']}System Information{Style.RESET_ALL}")
    print(f"{theme['accent']}{'═' * 50}{Style.RESET_ALL}")
    
    info = [
        ("OS", platform.system()),
        ("Release", platform.release()),
        ("Version", platform.version()),
        ("Machine", platform.machine()),
        ("Processor", platform.processor()),
        ("Python", sys.version.split()[0]),
        ("Shell", "DaffaShell Pro v2.0"),
        ("CWD", os.getcwd()),
        ("User", os.getenv("USER") or os.getenv("USERNAME")),
        ("Home", os.path.expanduser("~")),
    ]
    
    for label, value in info:
        print(f"{theme['muted']}{label:12}: {theme['success']}{value}{Style.RESET_ALL}")
    
    print(f"{theme['accent']}{'═' * 50}{Style.RESET_ALL}\n")
    state.last_exit_code = 0

def builtin_install(args: List[str]):
    """Smart package installer."""
    cwd = os.getcwd()
    
    # Node.js
    if os.path.exists(os.path.join(cwd, "package.json")):
        if shutil.which("pnpm"):
            cmd = ["pnpm", "install"]
        elif shutil.which("yarn"):
            cmd = ["yarn", "install"]
        elif shutil.which("npm"):
            cmd = ["npm", "install"]
        else:
            print_colored("No Node.js package manager found", "error")
            return
        
        print_colored(f"Running: {' '.join(cmd)}", "info")
        result = run_command(cmd)
        state.last_exit_code = result.returncode
        return
    
    # Python
    if os.path.exists(os.path.join(cwd, "requirements.txt")):
        cmd = ["pip", "install", "-r", "requirements.txt"]
        print_colored(f"Running: {' '.join(cmd)}", "info")
        result = run_command(cmd)
        state.last_exit_code = result.returncode
        return
    
    # PHP
    if os.path.exists(os.path.join(cwd, "composer.json")):
        if shutil.which("composer"):
            cmd = ["composer", "install"]
            print_colored(f"Running: {' '.join(cmd)}", "info")
            result = run_command(cmd)
            state.last_exit_code = result.returncode
            return
    
    # Ruby
    if os.path.exists(os.path.join(cwd, "Gemfile")):
        if shutil.which("bundle"):
            cmd = ["bundle", "install"]
            print_colored(f"Running: {' '.join(cmd)}", "info")
            result = run_command(cmd)
            state.last_exit_code = result.returncode
            return
    
    if args:
        cmd = args
        result = run_command(cmd)
        state.last_exit_code = result.returncode
    else:
        print_colored("No package manifest found and no command provided", "warn")
        state.last_exit_code = 1

def builtin_git(args: List[str]):
    """Git wrapper with enhanced output."""
    if not shutil.which("git"):
        print_colored("git not found in PATH", "error")
        state.last_exit_code = 127
        return
    
    if not args:
        args = ["status"]
    
    result = run_command(["git"] + args)
    state.last_exit_code = result.returncode

def builtin_serve(args: List[str]):
    """Smart development server launcher."""
    cwd = os.getcwd()
    theme = state.get_theme()
    
    # Laravel (PHP)
    if os.path.exists(os.path.join(cwd, "artisan")):
        if not shutil.which("php"):
            print_colored("PHP not found in PATH", "error")
            state.last_exit_code = 127
            return
        
        port = args[0] if args and args[0].isdigit() else "8000"
        print_colored(f"🚀 Starting Laravel development server on port {port}...", "info")
        print_colored(f"📍 URL: http://localhost:{port}", "success")
        print_colored("Press Ctrl+C to stop\n", "muted")
        
        result = run_command(["php", "artisan", "serve", f"--port={port}"])
        state.last_exit_code = result.returncode
        return
    
    # Node.js/React/Vue/etc
    if os.path.exists(os.path.join(cwd, "package.json")):
        try:
            with open(os.path.join(cwd, "package.json"), 'r') as f:
                pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                
                # Detect dev script
                if "dev" in scripts:
                    cmd_name = "dev"
                elif "start" in scripts:
                    cmd_name = "start"
                elif "serve" in scripts:
                    cmd_name = "serve"
                else:
                    print_colored("No dev script found in package.json", "warn")
                    state.last_exit_code = 1
                    return
                
                # Detect package manager
                if shutil.which("pnpm"):
                    pm = "pnpm"
                elif shutil.which("yarn"):
                    pm = "yarn"
                else:
                    pm = "npm"
                
                print_colored(f"🚀 Starting development server with {pm} run {cmd_name}...", "info")
                print_colored("Press Ctrl+C to stop\n", "muted")
                
                result = run_command([pm, "run", cmd_name])
                state.last_exit_code = result.returncode
                return
        except:
            pass
    
    # Django (Python)
    if os.path.exists(os.path.join(cwd, "manage.py")):
        if not shutil.which("python"):
            print_colored("Python not found in PATH", "error")
            state.last_exit_code = 127
            return
        
        port = args[0] if args and args[0].isdigit() else "8000"
        print_colored(f"🚀 Starting Django development server on port {port}...", "info")
        print_colored(f"📍 URL: http://localhost:{port}", "success")
        print_colored("Press Ctrl+C to stop\n", "muted")
        
        result = run_command(["python", "manage.py", "runserver", port])
        state.last_exit_code = result.returncode
        return
    
    # Flask (Python)
    if os.path.exists(os.path.join(cwd, "app.py")) or os.path.exists(os.path.join(cwd, "main.py")):
        if not shutil.which("flask"):
            print_colored("Flask not found. Install with: pip install flask", "warn")
            state.last_exit_code = 127
            return
        
        port = args[0] if args and args[0].isdigit() else "5000"
        print_colored(f"🚀 Starting Flask development server on port {port}...", "info")
        print_colored(f"📍 URL: http://localhost:{port}", "success")
        print_colored("Press Ctrl+C to stop\n", "muted")
        
        result = run_command(["flask", "run", "--port", port])
        state.last_exit_code = result.returncode
        return
    
    # Rails (Ruby)
    if os.path.exists(os.path.join(cwd, "config.ru")) or os.path.exists(os.path.join(cwd, "Gemfile")):
        if not shutil.which("rails"):
            print_colored("Rails not found in PATH", "error")
            state.last_exit_code = 127
            return
        
        port = args[0] if args and args[0].isdigit() else "3000"
        print_colored(f"🚀 Starting Rails development server on port {port}...", "info")
        print_colored(f"📍 URL: http://localhost:{port}", "success")
        print_colored("Press Ctrl+C to stop\n", "muted")
        
        result = run_command(["rails", "server", "-p", port])
        state.last_exit_code = result.returncode
        return
    
    # Simple HTTP server (Python)
    port = args[0] if args and args[0].isdigit() else "8000"
    print_colored(f"🚀 Starting simple HTTP server on port {port}...", "info")
    print_colored(f"📍 URL: http://localhost:{port}", "success")
    print_colored("Press Ctrl+C to stop\n", "muted")
    
    result = run_command(["python", "-m", "http.server", port])
    state.last_exit_code = result.returncode

def builtin_dev(args: List[str]):
    """Quick dev server alias."""
    builtin_serve(args)

def builtin_artisan(args: List[str]):
    """Laravel Artisan wrapper."""
    if not os.path.exists("artisan"):
        print_colored("Not in a Laravel project (artisan not found)", "error")
        state.last_exit_code = 1
        return
    
    if not shutil.which("php"):
        print_colored("PHP not found in PATH", "error")
        state.last_exit_code = 127
        return
    
    result = run_command(["php", "artisan"] + args)
    state.last_exit_code = result.returncode

def builtin_npm(args: List[str]):
    """NPM wrapper with smart detection."""
    if not args:
        args = ["run", "dev"]  # Default to npm run dev
    
    # Auto-detect package manager
    if os.path.exists("pnpm-lock.yaml") and shutil.which("pnpm"):
        pm = "pnpm"
    elif os.path.exists("yarn.lock") and shutil.which("yarn"):
        pm = "yarn"
    else:
        pm = "npm"
    
    theme = state.get_theme()
    if pm != "npm":
        print(f"{theme['info']}Using {pm} instead of npm{Style.RESET_ALL}")
    
    result = run_command([pm] + args)
    state.last_exit_code = result.returncode

def builtin_composer(args: List[str]):
    """Composer wrapper."""
    if not shutil.which("composer"):
        print_colored("Composer not found in PATH", "error")
        state.last_exit_code = 127
        return
    
    result = run_command(["composer"] + args)
    state.last_exit_code = result.returncode

def builtin_python(args: List[str]):
    """Python wrapper."""
    if not shutil.which("python"):
        print_colored("Python not found in PATH", "error")
        state.last_exit_code = 127
        return
    
    result = run_command(["python"] + args)
    state.last_exit_code = result.returncode

def builtin_node(args: List[str]):
    """Node.js wrapper."""
    if not shutil.which("node"):
        print_colored("Node.js not found in PATH", "error")
        state.last_exit_code = 127
        return
    
    result = run_command(["node"] + args)
    state.last_exit_code = result.returncode

def builtin_hack(args: List[str]):
    """Simulate hacking (fun)."""
    target = args[0] if args else "127.0.0.1"
    
    typewriter(f"Initiating security audit on {target}...", 0.004, "info")
    time.sleep(0.3)
    progress_bar("Scanning ports", 2.0)
    
    ports = [22, 80, 443, 3306, 8080, 27017]
    theme = state.get_theme()
    for port in ports:
        status = random.choice(["OPEN", "FILTERED", "CLOSED"])
        color = "success" if status == "OPEN" else "muted"
        print(f"{theme[color]}{target}:{port} [{status}]{Style.RESET_ALL}")
        time.sleep(0.1)
    
    typewriter("Vulnerability scan complete.", 0.004, "success")
    state.last_exit_code = 0

def builtin_scan(args: List[str]):
    """Network scanner simulation."""
    target = args[0] if args else "192.168.1.0/24"
    
    typewriter(f"Scanning network: {target}", 0.004, "info")
    progress_bar("Discovery", 1.5)
    
    theme = state.get_theme()
    for i in range(10):
        ip = f"192.168.1.{random.randint(1, 254)}"
        port = random.choice([22, 80, 443, 8080])
        mac = ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
        print(f"{theme['success']}{ip:15} {theme['info']}:{port:5} {theme['muted']}{mac}{Style.RESET_ALL}")
        time.sleep(0.15)
    
    typewriter("Scan complete.", 0.003, "success")
    state.last_exit_code = 0

def builtin_help(args: List[str]):
    """Display help information."""
    theme = state.get_theme()
    
    commands = {
        "File Operations": [
            ("ls [path]", "List directory contents"),
            ("cd [path]", "Change directory"),
            ("pwd", "Print working directory"),
            ("mkdir <dir>", "Create directory"),
            ("rm <file>", "Remove file/directory"),
            ("cp <src> <dst>", "Copy file/directory"),
            ("mv <src> <dst>", "Move/rename file"),
            ("cat <file>", "Display file contents"),
            ("find <pattern>", "Find files by pattern"),
            ("grep <pattern> <file>", "Search in files"),
        ],
        "System": [
            ("clear/cls", "Clear screen"),
            ("echo <text>", "Print text"),
            ("env", "Show environment variables"),
            ("export VAR=val", "Set environment variable"),
            ("sysinfo", "Show system information"),
            ("history [n]", "Show command history"),
        ],
        "Shell Features": [
            ("alias [name=cmd]", "Create/list aliases"),
            ("unalias <name>", "Remove alias"),
            ("theme [name]", "Change color theme"),
            ("help", "Show this help"),
            ("exit/quit", "Exit shell"),
        ],
        "Development": [
            ("install [args]", "Smart package installer"),
            ("git <args>", "Git wrapper"),
            ("serve [port]", "Smart dev server launcher"),
            ("dev [port]", "Quick dev server (alias)"),
            ("artisan <args>", "Laravel Artisan wrapper"),
            ("npm <args>", "NPM/yarn/pnpm smart wrapper"),
            ("composer <args>", "Composer wrapper"),
            ("python <args>", "Python wrapper"),
            ("node <args>", "Node.js wrapper"),
            ("hack [target]", "Security audit simulation"),
            ("scan [target]", "Network scanner simulation"),
        ],
        "Advanced": [
            ("cmd1 | cmd2", "Pipeline commands"),
            ("!n", "Repeat history command n"),
            ("cd -", "Go to previous directory"),
            ("$VAR", "Use environment variables"),
        ],
    }
    
    print(f"\n{theme['accent']}{'═' * 70}{Style.RESET_ALL}")
    print(f"{theme['info']}DaffaShell Pro - Command Reference{Style.RESET_ALL}")
    print(f"{theme['accent']}{'═' * 70}{Style.RESET_ALL}\n")
    
    for category, cmds in commands.items():
        print(f"{theme['accent']}{category}:{Style.RESET_ALL}")
        for cmd, desc in cmds:
            print(f"  {theme['success']}{cmd:25}{theme['muted']}{desc}{Style.RESET_ALL}")
        print()
    
    print(f"{theme['info']}Themes: {', '.join(THEMES.keys())}{Style.RESET_ALL}")
    print(f"{theme['muted']}Use Tab for completion, Ctrl+C to interrupt, Ctrl+D to exit{Style.RESET_ALL}\n")
    state.last_exit_code = 0

def builtin_which(args: List[str]):
    """Locate a command."""
    if not args:
        print_colored("which: missing operand", "error")
        state.last_exit_code = 1
        return
    
    cmd = args[0]
    
    # Check builtins
    if cmd in BUILTINS:
        print_colored(f"{cmd}: shell builtin", "info")
        state.last_exit_code = 0
        return
    
    # Check aliases
    if cmd in state.aliases:
        print_colored(f"{cmd}: aliased to '{state.aliases[cmd]}'", "info")
        state.last_exit_code = 0
        return
    
    # Check system PATH
    path = shutil.which(cmd)
    if path:
        print_colored(path, "success")
        state.last_exit_code = 0
    else:
        print_colored(f"{cmd} not found", "error")
        state.last_exit_code = 1

def builtin_touch(args: List[str]):
    """Create empty file or update timestamp."""
    if not args:
        print_colored("touch: missing operand", "error")
        state.last_exit_code = 1
        return
    
    try:
        for file in args:
            Path(file).touch()
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"touch: {e}", "error")
        state.last_exit_code = 1

def builtin_tree(args: List[str]):
    """Display directory tree."""
    path = args[0] if args else "."
    max_depth = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
    
    theme = state.get_theme()
    
    def print_tree(dir_path, prefix="", depth=0):
        if depth > max_depth:
            return
        
        try:
            items = sorted(os.listdir(dir_path))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                next_prefix = "    " if is_last else "│   "
                
                full_path = os.path.join(dir_path, item)
                if os.path.isdir(full_path):
                    print(f"{prefix}{current_prefix}{theme['dir']}{item}/{Style.RESET_ALL}")
                    print_tree(full_path, prefix + next_prefix, depth + 1)
                else:
                    print(f"{prefix}{current_prefix}{theme['muted']}{item}{Style.RESET_ALL}")
        except PermissionError:
            print(f"{prefix}[Permission Denied]")
    
    print(f"{theme['accent']}{os.path.abspath(path)}{Style.RESET_ALL}")
    print_tree(path)
    state.last_exit_code = 0

def builtin_du(args: List[str]):
    """Disk usage."""
    path = args[0] if args else "."
    
    try:
        total_size = 0
        theme = state.get_theme()
        
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(filepath)
                    total_size += size
                except:
                    pass
        
        print(f"{theme['success']}{format_size(total_size)}{theme['muted']} {path}{Style.RESET_ALL}")
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"du: {e}", "error")
        state.last_exit_code = 1

def builtin_df(args: List[str]):
    """Disk free space."""
    try:
        usage = shutil.disk_usage("/")
        theme = state.get_theme()
        
        print(f"\n{theme['accent']}Disk Usage:{Style.RESET_ALL}")
        print(f"{theme['muted']}Total:     {theme['info']}{format_size(usage.total)}{Style.RESET_ALL}")
        print(f"{theme['muted']}Used:      {theme['warn']}{format_size(usage.used)}{Style.RESET_ALL}")
        print(f"{theme['muted']}Free:      {theme['success']}{format_size(usage.free)}{Style.RESET_ALL}")
        
        pct = (usage.used / usage.total) * 100
        print(f"{theme['muted']}Usage:     {theme['error' if pct > 90 else 'warn']}{pct:.1f}%{Style.RESET_ALL}\n")
        
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"df: {e}", "error")
        state.last_exit_code = 1

def builtin_ps(args: List[str]):
    """Process status (basic)."""
    try:
        import psutil
        theme = state.get_theme()
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        
        print(f"\n{theme['accent']}{'PID':<8} {'CPU%':<8} {'MEM%':<8} {'NAME':<30}{Style.RESET_ALL}")
        print(f"{theme['accent']}{'-' * 60}{Style.RESET_ALL}")
        
        for proc in processes[:20]:  # Top 20
            pid = proc.get('pid', 0)
            name = proc.get('name', 'unknown')[:30]
            cpu = proc.get('cpu_percent', 0)
            mem = proc.get('memory_percent', 0)
            
            print(f"{theme['muted']}{pid:<8} {cpu:<8.1f} {mem:<8.1f} {name}{Style.RESET_ALL}")
        
        print()
        state.last_exit_code = 0
    except ImportError:
        print_colored("ps: requires 'psutil' module (pip install psutil)", "error")
        state.last_exit_code = 1
    except Exception as e:
        print_colored(f"ps: {e}", "error")
        state.last_exit_code = 1

def builtin_kill(args: List[str]):
    """Kill process by PID."""
    if not args:
        print_colored("kill: missing PID", "error")
        state.last_exit_code = 1
        return
    
    try:
        import psutil
        pid = int(args[0])
        proc = psutil.Process(pid)
        proc.terminate()
        print_colored(f"Process {pid} terminated", "success")
        state.last_exit_code = 0
    except ImportError:
        print_colored("kill: requires 'psutil' module", "error")
        state.last_exit_code = 1
    except Exception as e:
        print_colored(f"kill: {e}", "error")
        state.last_exit_code = 1

def builtin_wget(args: List[str]):
    """Download file from URL."""
    if not args:
        print_colored("wget: missing URL", "error")
        state.last_exit_code = 1
        return
    
    try:
        import urllib.request
        url = args[0]
        filename = args[1] if len(args) > 1 else url.split('/')[-1]
        
        print_colored(f"Downloading {url}...", "info")
        
        def progress_hook(count, block_size, total_size):
            pct = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\rProgress: {pct}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filename, progress_hook)
        print()
        print_colored(f"Downloaded: {filename}", "success")
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"wget: {e}", "error")
        state.last_exit_code = 1

def builtin_curl(args: List[str]):
    """Fetch URL content."""
    if not args:
        print_colored("curl: missing URL", "error")
        state.last_exit_code = 1
        return
    
    try:
        import urllib.request
        url = args[0]
        
        with urllib.request.urlopen(url) as response:
            content = response.read()
            print(content.decode('utf-8'))
        
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"curl: {e}", "error")
        state.last_exit_code = 1

def builtin_time(args: List[str]):
    """Time command execution."""
    if not args:
        print_colored("time: missing command", "error")
        state.last_exit_code = 1
        return
    
    start = time.time()
    handle_line(" ".join(args))
    elapsed = time.time() - start
    
    theme = state.get_theme()
    print(f"\n{theme['info']}Execution time: {elapsed:.3f}s{Style.RESET_ALL}")

def builtin_calc(args: List[str]):
    """Simple calculator."""
    if not args:
        print_colored("calc: missing expression", "error")
        state.last_exit_code = 1
        return
    
    try:
        expr = " ".join(args)
        result = eval(expr, {"__builtins__": {}}, {
            "abs": abs, "round": round, "pow": pow, "min": min, "max": max,
            "sum": sum, "len": len, "int": int, "float": float,
        })
        print_colored(str(result), "success")
        state.last_exit_code = 0
    except Exception as e:
        print_colored(f"calc: {e}", "error")
        state.last_exit_code = 1

def builtin_date(args: List[str]):
    """Display current date and time."""
    theme = state.get_theme()
    now = datetime.now()
    
    if args and args[0] == "-u":
        now = datetime.utcnow()
        print(f"{theme['info']}{now.strftime('%Y-%m-%d %H:%M:%S UTC')}{Style.RESET_ALL}")
    else:
        print(f"{theme['info']}{now.strftime('%Y-%m-%d %H:%M:%S %A')}{Style.RESET_ALL}")
    
    state.last_exit_code = 0

def builtin_whoami(args: List[str]):
    """Display current user."""
    user = os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    print_colored(user, "info")
    state.last_exit_code = 0

def builtin_hostname(args: List[str]):
    """Display hostname."""
    try:
        host = os.uname().nodename
    except:
        host = os.getenv("COMPUTERNAME", "unknown")
    
    print_colored(host, "info")
    state.last_exit_code = 0

# ==================== BUILTIN REGISTRY ====================
BUILTINS: Dict[str, Callable] = {
    # File operations
    "ls": builtin_ls,
    "dir": builtin_ls,
    "cd": builtin_cd,
    "pwd": builtin_pwd,
    "mkdir": builtin_mkdir,
    "rm": builtin_rm,
    "del": builtin_rm,
    "cp": builtin_cp,
    "copy": builtin_cp,
    "mv": builtin_mv,
    "move": builtin_mv,
    "cat": builtin_cat,
    "type": builtin_cat,
    "touch": builtin_touch,
    "find": builtin_find,
    "grep": builtin_grep,
    "tree": builtin_tree,
    "du": builtin_du,
    "df": builtin_df,
    
    # System
    "clear": builtin_clear,
    "cls": builtin_clear,
    "echo": builtin_echo,
    "env": builtin_env,
    "export": builtin_export,
    "set": builtin_env,
    "sysinfo": builtin_sysinfo,
    "history": builtin_history,
    "which": builtin_which,
    "where": builtin_which,
    "ps": builtin_ps,
    "kill": builtin_kill,
    "date": builtin_date,
    "whoami": builtin_whoami,
    "hostname": builtin_hostname,
    "calc": builtin_calc,
    "time": builtin_time,
    
    # Shell
    "alias": builtin_alias,
    "unalias": builtin_unalias,
    "theme": builtin_theme,
    "help": builtin_help,
    
    # Development
    "install": builtin_install,
    "git": builtin_git,
    "serve": builtin_serve,
    "dev": builtin_dev,
    "artisan": builtin_artisan,
    "npm": builtin_npm,
    "composer": builtin_composer,
    "python": builtin_python,
    "node": builtin_node,
    "wget": builtin_wget,
    "curl": builtin_curl,
    
    # Fun
    "hack": builtin_hack,
    "scan": builtin_scan,
}

# ==================== COMMAND HANDLER ====================
def handle_line(line: str):
    """Parse and execute command line."""
    line = line.strip()
    if not line:
        return
    
    # Handle history substitution
    if line.startswith("!") and readline:
        try:
            if line == "!!":
                # Repeat last command
                idx = readline.get_current_history_length()
                line = readline.get_history_item(idx) or ""
            elif line[1:].isdigit():
                idx = int(line[1:])
                line = readline.get_history_item(idx) or ""
            
            if line:
                print_colored(f"Executing: {line}", "muted")
        except:
            pass
    
    # Handle comments
    if line.startswith("#"):
        return
    
    # Parse command
    try:
        tokens = shlex.split(line)
    except Exception as e:
        print_colored(f"Parse error: {e}", "error")
        state.last_exit_code = 2
        return
    
    if not tokens:
        return
    
    # Expand aliases
    if tokens[0] in state.aliases:
        alias_cmd = state.aliases[tokens[0]]
        line = alias_cmd + " " + " ".join(tokens[1:])
        try:
            tokens = shlex.split(line)
        except:
            tokens = [line]
    
    # Check for exit
    if tokens[0] in ("exit", "quit"):
        return "exit"
    
    # Check for builtin
    if tokens[0] in BUILTINS:
        try:
            BUILTINS[tokens[0]](tokens[1:])
        except Exception as e:
            print_colored(f"Error: {e}", "error")
            state.last_exit_code = 1
        return
    
    # Check for pipeline
    if "|" in tokens:
        commands = parse_pipeline(line)
        execute_pipeline(commands)
        return
    
    # Execute as system command
    result = run_command(tokens)
    state.last_exit_code = result.returncode

# ==================== MAIN LOOP ====================
def main():
    """Main shell loop."""
    # Load configuration
    load_config()
    load_history()
    
    # Setup readline
    if readline:
        try:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(completer)
            readline.set_completer_delims(" \t\n;")
        except:
            pass
    
    # Display splash
    splash()
    
    # Main loop
    try:
        while True:
            try:
                # Get prompt
                prompt = get_prompt()
                
                # Read input
                if readline:
                    line = input(prompt)
                else:
                    print(prompt, end="")
                    line = sys.stdin.readline().rstrip("\n")
                
                if not line:
                    continue
                
                # Add to history
                if readline and line.strip():
                    try:
                        readline.add_history(line)
                    except:
                        pass
                
                # Execute command
                result = handle_line(line)
                
                if result == "exit":
                    typewriter("Shutting down DaffaShell...", 0.004, "muted")
                    break
                
            except KeyboardInterrupt:
                print()
                print_colored("^C (Use 'exit' to quit)", "warn")
                state.last_exit_code = 130
                continue
            
            except EOFError:
                print()
                typewriter("Goodbye!", 0.004, "info")
                break
    
    finally:
        save_history()
        save_config()

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_colored(f"Fatal error: {e}", "error")
        sys.exit(1)