import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import sys
import threading


class PyPackagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python打包工具")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.process = None
        self.is_running = False
        
        self.init_ui()
    
    def init_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.basic_frame = ttk.Frame(self.notebook)
        self.advanced_frame = ttk.Frame(self.notebook)
        self.log_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.basic_frame, text="基本设置")
        self.notebook.add(self.advanced_frame, text="高级设置")
        self.notebook.add(self.log_frame, text="打包日志")
        
        self.setup_basic_tab()
        self.setup_advanced_tab()
        self.setup_log_tab()
        self.setup_bottom_bar()
    
    def setup_basic_tab(self):
        main_container = ttk.Frame(self.basic_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        row = 0
        
        ttk.Label(left_frame, text="脚本路径:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.script_path_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.script_path_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        ttk.Button(left_frame, text="浏览", command=self.browse_script).grid(row=row, column=2, padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)
        row += 1
        
        ttk.Label(left_frame, text="输出目录:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.output_dir_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        ttk.Button(left_frame, text="浏览", command=self.browse_output).grid(row=row, column=2, padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)
        row += 1
        
        ttk.Label(left_frame, text="输出文件名:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.output_name_var = tk.StringVar(value="dist")
        ttk.Entry(left_frame, textvariable=self.output_name_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)
        row += 1
        
        ttk.Label(left_frame, text="图标文件:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.icon_path_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.icon_path_var, width=40).grid(row=row, column=1, sticky=tk.EW, pady=5)
        ttk.Button(left_frame, text="浏览", command=self.browse_icon).grid(row=row, column=2, padx=5, pady=5)
        left_frame.grid_columnconfigure(1, weight=1)
        row += 1
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
        row += 1
        
        ttk.Label(left_frame, text="打包模式:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar(value="onefile")
        mode_frame = ttk.Frame(left_frame)
        mode_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(mode_frame, text="单文件 (--onefile)", variable=self.mode_var, value="onefile").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="文件夹 (--onedir)", variable=self.mode_var, value="onedir").pack(side=tk.LEFT, padx=10)
        row += 1
        
        ttk.Label(left_frame, text="窗口模式:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.window_var = tk.StringVar(value="windowed")
        window_frame = ttk.Frame(left_frame)
        window_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(window_frame, text="无控制台 (--windowed)", variable=self.window_var, value="windowed").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(window_frame, text="有控制台 (--console)", variable=self.window_var, value="console").pack(side=tk.LEFT, padx=10)
        row += 1
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
        row += 1
        
        self.clean_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(left_frame, text="清理临时文件 (--clean)", variable=self.clean_var).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        self.debug_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left_frame, text="调试模式 (--debug all)", variable=self.debug_var).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        self.ascii_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left_frame, text="使用ASCII字符 (--ascii)", variable=self.ascii_var).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(right_frame, text="生成的命令:").pack(anchor=tk.W, pady=5)
        self.command_text = scrolledtext.ScrolledText(right_frame, height=15, width=50)
        self.command_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(right_frame, text="复制命令", command=self.copy_command).pack(fill=tk.X, pady=5)
        ttk.Button(right_frame, text="刷新命令", command=self.update_command).pack(fill=tk.X, pady=5)
    
    def setup_advanced_tab(self):
        main_container = ttk.Frame(self.advanced_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        row = 0
        
        ttk.Label(left_frame, text="隐藏导入 (逗号分隔):").grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        self.hidden_imports_text = scrolledtext.ScrolledText(left_frame, height=5, width=45)
        self.hidden_imports_text.grid(row=row, column=0, sticky=tk.EW, pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        row += 1
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, sticky=tk.EW, pady=10)
        row += 1
        
        ttk.Label(left_frame, text="添加数据文件 (每行一个，格式: 源路径;目标路径):").grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        self.add_data_text = scrolledtext.ScrolledText(left_frame, height=5, width=45)
        self.add_data_text.grid(row=row, column=0, sticky=tk.EW, pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        row += 1
        
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, sticky=tk.EW, pady=10)
        row += 1
        
        ttk.Label(left_frame, text="添加二进制文件 (每行一个，格式: 源路径;目标路径):").grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        self.add_binary_text = scrolledtext.ScrolledText(left_frame, height=5, width=45)
        self.add_binary_text.grid(row=row, column=0, sticky=tk.EW, pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        row += 1
        
        ttk.Label(right_frame, text="排除模块 (逗号分隔):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.exclude_text = scrolledtext.ScrolledText(right_frame, height=5, width=45)
        self.exclude_text.grid(row=1, column=0, sticky=tk.EW, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, sticky=tk.EW, pady=10)
        
        ttk.Label(right_frame, text="UPX路径:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.upx_path_var = tk.StringVar()
        ttk.Entry(right_frame, textvariable=self.upx_path_var, width=40).grid(row=4, column=0, sticky=tk.EW, pady=5)
        ttk.Button(right_frame, text="浏览", command=self.browse_upx).grid(row=4, column=1, padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        self.upx_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right_frame, text="使用UPX压缩 (--upx)", variable=self.upx_var).grid(row=6, column=0, sticky=tk.W, pady=5)
        
        self.strip_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(right_frame, text="剥离符号表 (--strip)", variable=self.strip_var).grid(row=7, column=0, sticky=tk.W, pady=5)
        
        self.noconfirm_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(right_frame, text="跳过确认 (--noconfirm)", variable=self.noconfirm_var).grid(row=8, column=0, sticky=tk.W, pady=5)
        
        self.optimize_var = tk.IntVar(value=0)
        ttk.Label(right_frame, text="优化级别:").grid(row=9, column=0, sticky=tk.W, pady=5)
        opt_frame = ttk.Frame(right_frame)
        opt_frame.grid(row=10, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(opt_frame, text="0 (无)", variable=self.optimize_var, value=0).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(opt_frame, text="1", variable=self.optimize_var, value=1).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(opt_frame, text="2", variable=self.optimize_var, value=2).pack(side=tk.LEFT, padx=5)
    
    def setup_log_tab(self):
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=30, width=100)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.config(state=tk.DISABLED)
    
    def setup_bottom_bar(self):
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(bottom_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(bottom_frame, text="检查PyInstaller", command=self.check_pyinstaller).pack(side=tk.RIGHT, padx=5)
        ttk.Button(bottom_frame, text="停止打包", command=self.stop_packaging, state=tk.DISABLED).pack(side=tk.RIGHT, padx=5)
        self.run_btn = ttk.Button(bottom_frame, text="开始打包", command=self.start_packaging)
        self.run_btn.pack(side=tk.RIGHT, padx=5)
    
    def browse_script(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python脚本", "*.py"), ("所有文件", "*.*")])
        if file_path:
            self.script_path_var.set(file_path)
            if not self.output_name_var.get() or self.output_name_var.get() == "dist":
                self.output_name_var.set(os.path.splitext(os.path.basename(file_path))[0])
            self.update_command()
    
    def browse_output(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir_var.set(dir_path)
            self.update_command()
    
    def browse_icon(self):
        file_path = filedialog.askopenfilename(filetypes=[("图标文件", "*.ico"), ("所有文件", "*.*")])
        if file_path:
            self.icon_path_var.set(file_path)
            self.update_command()
    
    def browse_upx(self):
        file_path = filedialog.askopenfilename(filetypes=[("UPX可执行文件", "upx.exe"), ("所有文件", "*.*")])
        if file_path:
            self.upx_path_var.set(file_path)
            self.update_command()
    
    def update_command(self):
        cmd = self.build_command()
        self.command_text.config(state=tk.NORMAL)
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(tk.END, cmd)
        self.command_text.config(state=tk.DISABLED)
    
    def build_command(self):
        parts = ["pyinstaller"]
        
        script = self.script_path_var.get()
        if not script:
            return "请选择要打包的Python脚本"
        parts.append(f'"{script}"')
        
        if self.mode_var.get() == "onefile":
            parts.append("--onefile")
        else:
            parts.append("--onedir")
        
        if self.window_var.get() == "windowed":
            parts.append("--windowed")
        else:
            parts.append("--console")
        
        output_dir = self.output_dir_var.get()
        if output_dir:
            parts.append(f'--distpath "{output_dir}"')
        
        output_name = self.output_name_var.get()
        if output_name:
            parts.append(f'--name "{output_name}"')
        
        icon = self.icon_path_var.get()
        if icon:
            parts.append(f'--icon="{icon}"')
        
        if self.clean_var.get():
            parts.append("--clean")
        
        if self.debug_var.get():
            parts.append("--debug all")
        
        if self.ascii_var.get():
            parts.append("--ascii")
        
        if self.noconfirm_var.get():
            parts.append("--noconfirm")
        
        if self.strip_var.get():
            parts.append("--strip")
        
        optimize = self.optimize_var.get()
        if optimize > 0:
            parts.append(f"--optimize={optimize}")
        
        hidden_imports = self.hidden_imports_text.get(1.0, tk.END).strip()
        if hidden_imports:
            imports = [i.strip() for i in hidden_imports.split(",") if i.strip()]
            for imp in imports:
                parts.append(f'--hidden-import "{imp}"')
        
        add_data = self.add_data_text.get(1.0, tk.END).strip()
        if add_data:
            lines = [l.strip() for l in add_data.split("\n") if l.strip()]
            for line in lines:
                parts.append(f'--add-data "{line}"')
        
        add_binary = self.add_binary_text.get(1.0, tk.END).strip()
        if add_binary:
            lines = [l.strip() for l in add_binary.split("\n") if l.strip()]
            for line in lines:
                parts.append(f'--add-binary "{line}"')
        
        exclude = self.exclude_text.get(1.0, tk.END).strip()
        if exclude:
            excludes = [e.strip() for e in exclude.split(",") if e.strip()]
            for exc in excludes:
                parts.append(f'--exclude-module "{exc}"')
        
        if self.upx_var.get():
            upx_path = self.upx_path_var.get()
            if upx_path:
                parts.append(f'--upx-dir "{os.path.dirname(upx_path)}"')
            parts.append("--upx")
        
        return " ".join(parts)
    
    def copy_command(self):
        cmd = self.build_command()
        self.root.clipboard_clear()
        self.root.clipboard_append(cmd)
        messagebox.showinfo("提示", "命令已复制到剪贴板")
    
    def check_pyinstaller(self):
        try:
            result = subprocess.run(["pyinstaller", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("检查结果", f"PyInstaller已安装，版本: {result.stdout.strip()}")
            else:
                messagebox.showwarning("检查结果", "PyInstaller未安装，请运行: pip install pyinstaller")
        except FileNotFoundError:
            messagebox.showwarning("检查结果", "PyInstaller未安装，请运行: pip install pyinstaller")
    
    def start_packaging(self):
        script = self.script_path_var.get()
        if not script:
            messagebox.showerror("错误", "请选择要打包的Python脚本")
            return
        
        if not os.path.exists(script):
            messagebox.showerror("错误", "指定的脚本文件不存在")
            return
        
        self.is_running = True
        self.run_btn.config(state=tk.DISABLED)
        ttk.Button(self.root, text="停止打包").config(state=tk.NORMAL)
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.append_log("=" * 50)
        self.append_log("开始打包...")
        self.append_log(f"脚本路径: {script}")
        self.append_log(f"输出目录: {self.output_dir_var.get() or '默认'}")
        self.append_log("=" * 50)
        
        cmd = self.build_command()
        self.append_log(f"\n执行命令: {cmd}\n")
        
        threading.Thread(target=self.run_packaging, args=(cmd,), daemon=True).start()
    
    def run_packaging(self, cmd):
        try:
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in self.process.stdout:
                if not self.is_running:
                    break
                self.append_log(line.rstrip())
            
            self.process.wait()
            
            if self.process.returncode == 0:
                self.append_log("\n" + "=" * 50)
                self.append_log("打包成功！")
                self.append_log("=" * 50)
                self.status_var.set("打包成功")
            else:
                self.append_log("\n" + "=" * 50)
                self.append_log(f"打包失败，返回码: {self.process.returncode}")
                self.append_log("=" * 50)
                self.status_var.set("打包失败")
        except Exception as e:
            self.append_log(f"\n错误: {str(e)}")
            self.status_var.set("发生错误")
        finally:
            self.is_running = False
            self.process = None
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: ttk.Button(self.root, text="停止打包").config(state=tk.DISABLED))
    
    def stop_packaging(self):
        if self.process and self.is_running:
            self.process.terminate()
            self.is_running = False
            self.append_log("\n打包已被用户终止")
            self.status_var.set("已终止")
    
    def append_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PyPackagerApp(root)
    root.mainloop()