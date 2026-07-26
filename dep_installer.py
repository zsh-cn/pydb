import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ast
import sys
import subprocess
import threading
import os
import locale
import importlib.util
import shutil

IMPORT_TO_PIP = {
    'cv2': 'opencv-python',
    'bs4': 'beautifulsoup4',
    'PIL': 'Pillow',
    'sklearn': 'scikit-learn',
    'skimage': 'scikit-image',
    'tensorflow': 'tensorflow',
    'keras': 'keras',
    'matplotlib.pyplot': 'matplotlib',
    'matplotlib': 'matplotlib',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'torch': 'torch',
    'torchvision': 'torchvision',
    'tqdm': 'tqdm',
    'requests': 'requests',
    'selenium': 'selenium',
    'pygame': 'pygame',
    'pyqt5': 'PyQt5',
    'pyqt6': 'PyQt6',
    'scipy': 'scipy',
    'jinja2': 'Jinja2',
    'flask': 'Flask',
    'django': 'Django',
    'pytest': 'pytest',
    'pytest_cov': 'pytest-cov',
    'sqlalchemy': 'SQLAlchemy',
    'beautifulsoup4': 'beautifulsoup4',
    'xlrd': 'xlrd',
    'xlwt': 'xlwt',
    'openpyxl': 'openpyxl',
    'xlsxwriter': 'XlsxWriter',
    'pydantic': 'pydantic',
    'aiohttp': 'aiohttp',
    'yaml': 'PyYAML',
    'dateutil': 'python-dateutil',
    'Crypto': 'pycryptodome',
    'cryptography': 'cryptography',
    'pymongo': 'pymongo',
    'redis': 'redis',
    'mysql': 'mysql-connector-python',
    'psycopg2': 'psycopg2-binary',
    'httpx': 'httpx',
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'websockets': 'websockets',
    'click': 'click',
    'colorama': 'colorama',
    'pytz': 'pytz',
    'arrow': 'arrow',
    'faker': 'faker',
    'pytest_asyncio': 'pytest-asyncio',
    'pandas_datareader': 'pandas-datareader',
    'lxml': 'lxml',
    'html5lib': 'html5lib',
    'chardet': 'chardet',
    'idna': 'idna',
    'urllib3': 'urllib3',
    'certifi': 'certifi',
    'six': 'six',
    'python_dotenv': 'python-dotenv',
    'argparse': None,
    'asyncio': None,
    'base64': None,
    'bisect': None,
    'collections': None,
    'datetime': None,
    'decimal': None,
    'hashlib': None,
    'json': None,
    'logging': None,
    'math': None,
    'os': None,
    'pathlib': None,
    'random': None,
    're': None,
    'string': None,
    'sys': None,
    'time': None,
    'typing': None,
    'unittest': None,
    'urllib': None,
    'xml': None,
}

STDLIB_MODULES = {
    'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio',
    'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binhex', 'bisect',
    'builtins', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath',
    'cmd', 'code', 'codecs', 'codeop', 'collections', 'collections.abc',
    'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib',
    'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses',
    'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils',
    'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler',
    'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions',
    'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob',
    'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http',
    'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress',
    'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging',
    'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap',
    'modulefinder', 'msilib', 'multiprocessing', 'netrc', 'nis', 'nntplib',
    'numbers', 'operator', 'optparse', 'os', 'pathlib', 'pdb', 'pickle',
    'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib',
    'posix', 'pprint', 'profile', 'pstats', 'pty', 'py_compile', 'pycparser',
    'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'resource',
    'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors',
    'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib',
    'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat',
    'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau',
    'symbol', 'symtable', 'sys', 'sysconfig', 'tabnanny', 'tarfile',
    'telnetlib', 'tempfile', 'textwrap', 'threading', 'time', 'timeit',
    'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc',
    'tty', 'turtle', 'types', 'typing', 'unicodedata', 'unittest', 'urllib',
    'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser',
    'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp',
    'zipfile', 'zlib'
}


def get_system_python():
    if getattr(sys, 'frozen', False):
        python_exe = shutil.which('python')
        if python_exe and os.path.exists(python_exe):
            return python_exe
        python_exe = shutil.which('python3')
        if python_exe and os.path.exists(python_exe):
            return python_exe
        for path in os.environ.get('PATH', '').split(os.pathsep):
            candidate = os.path.join(path, 'python.exe')
            if os.path.exists(candidate):
                return candidate
        return sys.executable
    return sys.executable


def get_stdlib_modules():
    try:
        return set(sys.stdlib_module_names)
    except AttributeError:
        return STDLIB_MODULES


def extract_imports(file_path):
    imports = set()
    stdlib = get_stdlib_modules()

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

    content = content.lstrip('\ufeff')

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        raise ValueError(f"Python语法错误: {e}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod_name = alias.name.split('.')[0]
                if mod_name and mod_name not in stdlib:
                    imports.add(mod_name)
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                continue
            if node.module:
                mod_name = node.module.split('.')[0]
                if mod_name and mod_name not in stdlib:
                    imports.add(mod_name)

    return imports


def map_to_pip(import_names):
    pip_packages = []
    for name in import_names:
        pip_name = IMPORT_TO_PIP.get(name, name)
        if pip_name:
            pip_packages.append(pip_name)
    return pip_packages


def is_package_installed(package_name):
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            return True
    except ModuleNotFoundError:
        pass
    except ValueError:
        pass

    try:
        python_exe = get_system_python()
        cmd = [python_exe, '-m', 'pip', 'show', package_name]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


class DepInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python库安装工具")
        self.root.geometry("800x650")
        self.root.resizable(True, True)

        self.selected_file = tk.StringVar()
        self.detected_packages = []
        self.checkboxes = []
        self.cancel_event = threading.Event()
        self.pip_source = tk.StringVar(value="")
        self.installing = False

        self.create_widgets()

    def create_widgets(self):
        frame_top = ttk.Frame(self.root, padding=10)
        frame_top.pack(fill=tk.X)

        ttk.Label(frame_top, text="选择Python文件:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame_top, textvariable=self.selected_file, width=50, state='readonly').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(frame_top, text="浏览", command=self.browse_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="解析依赖", command=self.parse_dependencies).pack(side=tk.LEFT, padx=5)

        frame_source = ttk.Frame(self.root, padding=(10, 0))
        frame_source.pack(fill=tk.X)

        ttk.Label(frame_source, text="Pip源 (可选):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(frame_source, textvariable=self.pip_source, width=60).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Label(frame_source, text="例: https://pypi.tuna.tsinghua.edu.cn/simple").pack(side=tk.LEFT, padx=5)

        frame_list = ttk.Frame(self.root, padding=10)
        frame_list.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_list, text="检测到的依赖库:").pack(anchor=tk.W, padx=5)

        self.list_frame = ttk.Frame(frame_list)
        self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.scrollbar = ttk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.list_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        frame_buttons = ttk.Frame(self.root, padding=10)
        frame_buttons.pack(fill=tk.X)

        ttk.Button(frame_buttons, text="全选", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="取消全选", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="反选", command=self.toggle_select).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_buttons, text="取消已安装", command=self.deselect_installed).pack(side=tk.LEFT, padx=5)

        self.install_btn = ttk.Button(frame_buttons, text="安装选中库", command=self.install_packages, style='Accent.TButton')
        self.install_btn.pack(side=tk.RIGHT, padx=5)

        self.cancel_btn = ttk.Button(frame_buttons, text="取消安装", command=self.cancel_install, state='disabled')
        self.cancel_btn.pack(side=tk.RIGHT, padx=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame_buttons, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)

        frame_output = ttk.Frame(self.root, padding=10)
        frame_output.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_output, text="安装日志:").pack(anchor=tk.W, padx=5)
        self.output_text = tk.Text(frame_output, height=12, state='disabled', font=('Consolas', 9))
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)

        frame_log = ttk.Frame(self.root, padding=(10, 0))
        frame_log.pack(fill=tk.X)

        ttk.Button(frame_log, text="保存日志", command=self.save_log).pack(side=tk.RIGHT, padx=5)

        style = ttk.Style()
        style.configure('Accent.TButton', foreground='white', background='#0078d7')
        style.configure('Success.TLabel', foreground='green')
        style.configure('Warning.TLabel', foreground='orange')
        style.configure('Error.TLabel', foreground='red')

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="选择Python文件",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if file_path:
            self.selected_file.set(file_path)

    def parse_dependencies(self):
        file_path = self.selected_file.get()
        if not file_path:
            messagebox.showwarning("提示", "请先选择一个Python文件")
            return

        if not os.path.exists(file_path):
            messagebox.showerror("错误", "文件不存在")
            return

        try:
            imports = extract_imports(file_path)
            packages = map_to_pip(imports)

            self.detected_packages = sorted(packages)
            self.update_package_list()

            if not packages:
                messagebox.showinfo("提示", "未检测到需要安装的第三方库")
            else:
                installed_count = sum(1 for pkg in packages if is_package_installed(pkg))
                messagebox.showinfo("提示", f"检测到 {len(packages)} 个库，其中 {installed_count} 个已安装")

        except ValueError as e:
            messagebox.showerror("错误", str(e))
        except Exception as e:
            messagebox.showerror("错误", f"解析失败: {str(e)}")

    def update_package_list(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.checkboxes.clear()

        for i, package in enumerate(self.detected_packages):
            var = tk.BooleanVar(value=True)
            cb_frame = ttk.Frame(self.inner_frame)
            cb_frame.pack(anchor=tk.W, pady=1, fill=tk.X)

            cb = ttk.Checkbutton(cb_frame, text=package, variable=var)
            cb.pack(side=tk.LEFT)

            if is_package_installed(package):
                status_label = ttk.Label(cb_frame, text="[已安装]", style='Success.TLabel')
            else:
                status_label = ttk.Label(cb_frame, text="[未安装]", style='Warning.TLabel')
            status_label.pack(side=tk.RIGHT)

            self.checkboxes.append((var, package))

    def select_all(self):
        for var, _ in self.checkboxes:
            var.set(True)

    def deselect_all(self):
        for var, _ in self.checkboxes:
            var.set(False)

    def toggle_select(self):
        for var, _ in self.checkboxes:
            var.set(not var.get())

    def deselect_installed(self):
        for var, package in self.checkboxes:
            if is_package_installed(package):
                var.set(False)

    def install_packages(self):
        selected = [pkg for var, pkg in self.checkboxes if var.get()]

        if not selected:
            messagebox.showwarning("提示", "请至少选择一个库进行安装")
            return

        self.installing = True
        self.cancel_event.clear()
        self.install_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.progress_var.set(0)

        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, f"开始安装以下库: {', '.join(selected)}\n")
        self.output_text.insert(tk.END, "=" * 60 + "\n")
        self.output_text.config(state='disabled')

        thread = threading.Thread(target=self.run_install, args=(selected,))
        thread.daemon = True
        thread.start()

    def cancel_install(self):
        self.cancel_event.set()
        self.append_output("\n⚠️ 正在取消安装...\n")

    def run_install(self, packages):
        success_count = 0
        fail_count = 0
        total = len(packages)

        for i, package in enumerate(packages, 1):
            if self.cancel_event.is_set():
                self.append_output("\n⚠️ 安装已取消\n")
                break

            progress = (i - 1) / total * 100
            self.root.after(0, lambda p=progress: self.progress_var.set(p))

            self.append_output(f"\n[{i}/{total}] 正在安装 {package}...\n")
            self.append_output("-" * 50 + "\n")

            try:
                python_exe = get_system_python()
                cmd = [python_exe, '-m', 'pip', 'install', package]
                if self.pip_source.get():
                    cmd.extend(['-i', self.pip_source.get()])

                encoding = locale.getpreferredencoding(False) or 'utf-8'

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding=encoding,
                    errors='replace'
                )

                for line in iter(process.stdout.readline, ''):
                    if self.cancel_event.is_set():
                        try:
                            process.terminate()
                        except Exception:
                            pass
                        break
                    self.append_output(line)

                process.wait(timeout=300)

                if process.returncode == 0:
                    self.append_output(f"\n✅ {package} 安装成功!\n")
                    success_count += 1
                else:
                    self.append_output(f"\n❌ {package} 安装失败，返回码: {process.returncode}\n")
                    fail_count += 1

            except subprocess.TimeoutExpired:
                self.append_output(f"\n❌ {package} 安装超时!\n")
                fail_count += 1
            except Exception as e:
                self.append_output(f"\n❌ {package} 安装异常: {str(e)}\n")
                fail_count += 1

        progress = 100
        self.root.after(0, lambda: self.progress_var.set(progress))

        self.append_output("\n" + "=" * 60 + "\n")
        self.append_output(f"安装完成! 成功: {success_count}, 失败: {fail_count}\n")

        self.root.after(0, self.on_install_complete)

    def on_install_complete(self):
        self.installing = False
        self.install_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')

    def append_output(self, text):
        def update_text():
            self.output_text.config(state='normal')
            self.output_text.insert(tk.END, text)
            self.output_text.see(tk.END)
            self.output_text.config(state='disabled')

        self.root.after(0, update_text)

    def save_log(self):
        log_content = self.output_text.get('1.0', tk.END)
        if not log_content.strip():
            messagebox.showwarning("提示", "日志为空")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存日志",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                messagebox.showinfo("提示", "日志保存成功")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DepInstallerApp(root)
    root.mainloop()