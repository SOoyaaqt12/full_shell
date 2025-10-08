# DaffaShell Pro v2.0 🚀

<div align="center">

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Downloads](https://img.shields.io/github/downloads/SOoyaaqt12/full_shell/total?label=Downloads)

**A feature-rich, cross-platform terminal shell with advanced capabilities**

*Beautiful • Powerful • Developer-Friendly*

**[⬇️ Download for Windows](https://github.com/SOoyaaqt12/full_shell/raw/main/output/DaffaShellInstaller.exe)** • [📖 Documentation](#-command-reference) • [🐛 Report Bug](https://github.com/SOoyaaqt12/full_shell/issues)

</div>

---

## ✨ Features

### 🎨 **Beautiful Interface**
- **4 Built-in Themes**: Neon, Matrix, Dracula, Classic
- **Colored Output**: Syntax-highlighted directory listings and command outputs
- **Smart Prompt**: Git branch detection, exit code indicators, and elegant design
- **Typewriter Effects**: Dramatic output for special commands

### 🛠️ **Developer Tools**
- **Smart Package Installer**: Auto-detects and installs dependencies for Node.js, Python, PHP, Ruby projects
- **Intelligent Dev Server**: Automatically launches the right development server (Laravel, Django, Flask, Node.js, Rails, etc.)
- **Git Integration**: Enhanced git wrapper with colored output
- **Package Manager Detection**: Automatically uses pnpm/yarn/npm based on lock files

### 💻 **Built-in Commands**
Over 50+ built-in commands including file operations, system utilities, and developer tools

### 🔧 **Advanced Features**
- **Command Aliases**: Create custom shortcuts for frequently used commands
- **Command History**: Persistent history with readline support
- **Tab Completion**: Intelligent auto-completion for commands and file paths
- **Pipeline Support**: Chain commands with Unix-style pipes
- **Environment Variables**: Manage and use environment variables
- **Configuration Persistence**: Saves your settings, aliases, and theme preferences

### 🎮 **Fun Commands**
- **Hack Simulator**: Security audit simulation with port scanning effects
- **Network Scanner**: Network discovery simulation with visual effects
- **Progress Bars**: Beautiful animated progress indicators

---

## 📦 Installation

### Option 1: Download Executable (Windows - Easiest!)

**For Windows users**, you can download the pre-built executable directly:

📥 **[Download DaffaShellInstaller.exe](https://github.com/SOoyaaqt12/full_shell/raw/main/output/DaffaShellInstaller.exe)**

Or alternatively:
1. Navigate to the [`output`](https://github.com/SOoyaaqt12/full_shell/tree/main/output) folder in this repository
2. Click on `DaffaShellInstaller.exe`
3. Click the "Download" button
4. Run the executable - no Python installation required!
5. Start using DaffaShell Pro immediately

> **Note**: The executable is standalone and includes all dependencies. Windows may show a security warning on first run - this is normal for unsigned executables.

### Option 2: Run from Source (Cross-Platform)

#### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

#### Required Dependencies

```bash
pip install colorama
```

#### Optional Dependencies (Recommended)

```bash
# For readline support on Windows
pip install pyreadline3

# For process management commands (ps, kill)
pip install psutil
```

#### Quick Install

1. Clone the repository:
```bash
git clone https://github.com/SOoyaaqt12/full_shell.git
cd full_shell
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Linux/macOS):
```bash
chmod +x full_shell.py
```

4. Run the shell:
```bash
python full_shell.py
# or on Linux/macOS
./full_shell.py
```

---

## 🚀 Quick Start

### Windows Users (Recommended)

1. **[Download DaffaShellInstaller.exe](https://github.com/SOoyaaqt12/full_shell/raw/main/output/DaffaShellInstaller.exe)**
2. Double-click to run (allow if Windows SmartScreen appears)
3. Enjoy DaffaShell Pro! 🎉

### All Platforms (Python)

```bash
# Start the shell
python full_shell.py

# Change directory
cd /path/to/directory

# List files with colors
ls

# Create directories
mkdir my_project

# Copy files
cp file.txt backup.txt

# Display file contents
cat README.md
```

### Developer Workflow

```bash
# Clone a project
git clone https://github.com/user/repo.git
cd repo

# Install dependencies (auto-detects package manager)
install

# Start development server (auto-detects framework)
serve
# or
dev

# Run specific commands
npm run build
composer update
python manage.py migrate
```

---

## 📚 Command Reference

### File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `ls [path]` | List directory contents with colors | `ls`, `ls /home` |
| `cd [path]` | Change directory | `cd projects`, `cd -` |
| `pwd` | Print working directory | `pwd` |
| `mkdir <dir>` | Create directory | `mkdir new_folder` |
| `rm <file>` | Remove file/directory | `rm file.txt`, `rm -rf folder` |
| `cp <src> <dst>` | Copy file/directory | `cp file.txt backup.txt` |
| `mv <src> <dst>` | Move/rename file | `mv old.txt new.txt` |
| `cat <file>` | Display file contents | `cat README.md` |
| `touch <file>` | Create empty file | `touch newfile.txt` |
| `find <pattern>` | Find files by pattern | `find "*.py"` |
| `grep <pattern> <file>` | Search in files | `grep "TODO" app.py` |
| `tree [path] [depth]` | Display directory tree | `tree . 2` |
| `du [path]` | Show disk usage | `du /home/user` |
| `df` | Show disk free space | `df` |

### System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `clear` / `cls` | Clear screen | `clear` |
| `echo <text>` | Print text | `echo "Hello World"` |
| `env` | Show environment variables | `env` |
| `export VAR=val` | Set environment variable | `export PATH=/usr/bin` |
| `sysinfo` | Display system information | `sysinfo` |
| `history [n]` | Show command history | `history 20` |
| `which <cmd>` | Locate command | `which python` |
| `ps` | Show running processes | `ps` |
| `kill <pid>` | Terminate process | `kill 1234` |
| `date` | Show current date/time | `date`, `date -u` |
| `whoami` | Show current user | `whoami` |
| `hostname` | Show hostname | `hostname` |
| `calc <expr>` | Simple calculator | `calc 2 + 2 * 3` |
| `time <cmd>` | Time command execution | `time ls -la` |

### Shell Features

| Command | Description | Example |
|---------|-------------|---------|
| `alias [name=cmd]` | Create/list aliases | `alias ll="ls -la"` |
| `unalias <name>` | Remove alias | `unalias ll` |
| `theme [name]` | Change color theme | `theme matrix` |
| `help` | Show help information | `help` |
| `exit` / `quit` | Exit shell | `exit` |

### Development Tools

| Command | Description | Example |
|---------|-------------|---------|
| `install [args]` | Smart package installer | `install` |
| `git <args>` | Git wrapper | `git status`, `git commit -m "fix"` |
| `serve [port]` | Smart dev server launcher | `serve`, `serve 3000` |
| `dev [port]` | Quick dev server alias | `dev` |
| `artisan <args>` | Laravel Artisan wrapper | `artisan make:controller` |
| `npm <args>` | Smart npm/yarn/pnpm wrapper | `npm run dev` |
| `composer <args>` | Composer wrapper | `composer require package` |
| `python <args>` | Python wrapper | `python script.py` |
| `node <args>` | Node.js wrapper | `node app.js` |

### Network & Utilities

| Command | Description | Example |
|---------|-------------|---------|
| `wget <url>` | Download file | `wget https://example.com/file.zip` |
| `curl <url>` | Fetch URL content | `curl https://api.github.com` |
| `hack [target]` | Security audit simulation | `hack 192.168.1.1` |
| `scan [target]` | Network scanner simulation | `scan 192.168.1.0/24` |

### Advanced Features

| Feature | Description | Example |
|---------|-------------|---------|
| Pipelines | Chain commands | `ls \| grep ".py"` |
| History | Repeat commands | `!!` (last), `!123` (command 123) |
| Previous Dir | Return to last directory | `cd -` |
| Variables | Use environment variables | `echo $HOME` |

---

## 🎨 Themes

DaffaShell Pro comes with 4 beautiful themes:

### Available Themes
- **neon** (default) - Cyan and vibrant colors
- **matrix** - Green terminal hacker style
- **dracula** - Purple and dark theme
- **classic** - Traditional terminal colors

### Changing Themes

```bash
# List available themes
theme

# Change theme
theme matrix
theme dracula
theme classic
theme neon
```

Your theme preference is automatically saved!

---

## 🔧 Smart Features

### 1. Smart Package Installer

The `install` command automatically detects your project type and runs the appropriate installer:

```bash
# Automatically detects and runs:
# - pnpm install (if pnpm-lock.yaml exists)
# - yarn install (if yarn.lock exists)
# - npm install (if package.json exists)
# - pip install -r requirements.txt (if requirements.txt exists)
# - composer install (if composer.json exists)
# - bundle install (if Gemfile exists)

install
```

### 2. Smart Development Server

The `serve` or `dev` command automatically detects your framework and starts the appropriate server:

```bash
# Automatically detects and runs:
# - php artisan serve (Laravel)
# - npm/yarn/pnpm run dev (Node.js/React/Vue/etc)
# - python manage.py runserver (Django)
# - flask run (Flask)
# - rails server (Rails)
# - python -m http.server (fallback)

serve
# or
dev
```

### 3. Smart Package Manager Detection

Commands like `npm` automatically use the right package manager:

```bash
# Automatically uses pnpm if pnpm-lock.yaml exists
# or yarn if yarn.lock exists
# or npm as fallback

npm run dev
npm install package-name
```

### 4. Git Branch in Prompt

The prompt automatically shows your current git branch when inside a git repository:

```
┌─[user@hostname]─[~/projects/my-app] (main)
└─λ 
```

### 5. Exit Code Indicator

Failed commands show their exit code in the prompt:

```
┌─[user@hostname]─[~/projects] [1]
└─λ 
```

---

## 📝 Configuration

DaffaShell Pro automatically saves your configuration to `~/.daffashell_config.json`:

```json
{
  "aliases": {
    "ll": "ls -la",
    "gs": "git status"
  },
  "env_vars": {
    "MY_VAR": "value"
  },
  "theme": "neon",
  "config": {
    "prompt_symbol": "λ",
    "max_history": 2000,
    "auto_suggestions": true,
    "colored_output": true
  }
}
```

### Configuration Files

- **Config**: `~/.daffashell_config.json` - Settings, aliases, theme
- **History**: `~/.daffashell_history` - Command history

---

## 💡 Tips & Tricks

### Creating Useful Aliases

```bash
# Quick navigation
alias ..="cd .."
alias ...="cd ../.."
alias home="cd ~"

# Git shortcuts
alias gs="git status"
alias ga="git add"
alias gc="git commit -m"
alias gp="git push"

# Development
alias dev="serve"
alias fresh="rm -rf node_modules && install"
```

### Using History

```bash
# Repeat last command
!!

# Repeat command number 42
!42

# Search history
history | grep "git"
```

### Tab Completion

Press `Tab` to auto-complete:
- Command names
- File and directory paths
- Aliases

### Keyboard Shortcuts

- `Ctrl+C` - Interrupt current command
- `Ctrl+D` - Exit shell
- `Tab` - Auto-complete
- `↑/↓` - Navigate command history

---

## 🛠️ Development

### Project Structure

```
full_shell/
├── full_shell.py              # Main shell implementation
├── output/
│   └── DaffaShellInstaller.exe # Pre-built Windows executable
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── .daffashell_config.json    # User configuration (auto-generated)
```

### Building Executable

To build your own executable using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --name DaffaShellInstaller full_shell.py

# The executable will be in the dist/ folder
```

### Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding Custom Built-in Commands

To add a new built-in command, follow this pattern:

```python
def builtin_mycommand(args: List[str]):
    """Description of my command."""
    # Your implementation here
    print_colored("Hello from my command!", "success")
    state.last_exit_code = 0

# Register in BUILTINS dictionary
BUILTINS = {
    # ... existing commands
    "mycommand": builtin_mycommand,
}
```

---

## 🐛 Known Issues

- Tab completion may be slow on systems with large PATH directories
- Some features require optional dependencies (`psutil` for process commands)
- Windows users may need `pyreadline3` for full readline support

---

## 📋 Requirements

### Required
- Python 3.6+
- colorama

### Optional
- pyreadline3 (Windows readline support)
- psutil (process management commands)
- git (for git integration)
- Node.js, PHP, Python, etc. (for respective development commands)

---

## 📄 License

This project is licensed under the MIT License - feel free to use it for personal or commercial projects.

---

## 👤 Author

**SOoyaaqt12**

- GitHub: [@SOoyaaqt12](https://github.com/SOoyaaqt12)

---

## 🙏 Acknowledgments

- Inspired by popular Unix shells (bash, zsh, fish)
- Built with Python and love ❤️
- Thanks to the open-source community

---

## 🚀 Future Plans

- [ ] Command syntax highlighting
- [ ] Auto-suggestions based on history
- [ ] Plugin system
- [ ] Configuration wizard
- [ ] More built-in commands
- [ ] Job control (bg, fg, jobs)
- [ ] Shell scripting support
- [ ] Remote shell capabilities
- [ ] Better Windows support

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ by SOoyaaqt12

</div>
