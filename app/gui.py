import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

# Uvozimo obstoječo logiko iz našega projekta
from pipeline.analyzer import Analyzer
from reporting.report import generate_report
from app.config import SUPPORTED_LANGUAGES, SUPPORTED_DATABASES

class SecurityAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Security Code Analyzer")
        self.root.geometry("800x800")
        
        # Ustvarimo glavno instanco našega analizatorja
        self.analyzer = Analyzer()
        
        self.build_gui()

    def build_gui(self):
        """Zgradi vse grafične elemente na zaslonu."""
        
        # --- ZGORNJI DEL: Nastavitve (Jezik in Baza podatkov) ---
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10, fill=tk.X, padx=20)
        
        # Izbira jezika
        tk.Label(settings_frame, text="Language:").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value=SUPPORTED_LANGUAGES[0])
        lang_dropdown = tk.OptionMenu(settings_frame, self.lang_var, *SUPPORTED_LANGUAGES)
        lang_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Izbira podatkovne baze
        tk.Label(settings_frame, text="Database:").pack(side=tk.LEFT)
        self.db_var = tk.StringVar(value=SUPPORTED_DATABASES[0])
        db_dropdown = tk.OptionMenu(settings_frame, self.db_var, *SUPPORTED_DATABASES)
        db_dropdown.pack(side=tk.LEFT, padx=10)
        
        # --- SREDNJI DEL: Vnos kode (Prilepi ali naloži iz datoteke) ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(input_frame, text="Source Code (Paste here or load from file):").pack(anchor=tk.W)
        
        # Gumb za nalaganje datoteke
        btn_load = tk.Button(input_frame, text="Load File", command=self.load_file)
        btn_load.pack(anchor=tk.W, pady=(0, 5))
        
        # Tekstovno polje za vnos kode
        self.code_input = scrolledtext.ScrolledText(input_frame, height=15, width=80)
        self.code_input.pack(fill=tk.BOTH, expand=True)
        
        # --- GUMB ZA ANALIZO ---
        btn_analyze = tk.Button(self.root, text="Analyze Code", command=self.run_analysis, bg="lightblue", font=("Arial", 12, "bold"))
        btn_analyze.pack(pady=15)
        
        # --- SPODNJI DEL: Prikaz rezultatov ---
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=20)
        
        tk.Label(output_frame, text="Analysis Results:").pack(anchor=tk.W)
        
        # Tekstovno polje za prikaz poročila (samo za branje)
        self.result_output = scrolledtext.ScrolledText(output_frame, height=15, width=80, state=tk.DISABLED, bg="#f4f4f4")
        self.result_output.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    def load_file(self):
        """Odpre pogovorno okno za izbiro datoteke in prikaže njeno vsebino."""
        filepath = filedialog.askopenfilename(
            title="Select a code file",
            filetypes=(("All files", "*.*"), ("Python files", "*.py"), ("PHP files", "*.php"), ("JavaScript files", "*.js"))
        )
        
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    
                # Počistimo trenutni vnos in vstavimo novo kodo
                self.code_input.delete("1.0", tk.END)
                self.code_input.insert(tk.END, content)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file:\n{e}")

    def run_analysis(self):
        """Prebere kodo in zažene analizator. (Zažene se v novem thread-u, da ne zamrzne GUIja)."""
        code = self.code_input.get("1.0", tk.END).strip()
        
        if not code:
            messagebox.showwarning("Warning", "Please provide some code to analyze.")
            return
            
        language = self.lang_var.get()
        database = self.db_var.get()
        
        # Očistimo star rezultat in prikažemo "Analyzing..."
        self.update_result("Analyzing...\nThis might take a moment.", clear=True)
        
        # Analizo izvedemo v ločenem threadu, da GUI ostane odziven
        analysis_thread = threading.Thread(target=self._perform_analysis, args=(code, language, database))
        analysis_thread.start()

    def _perform_analysis(self, code, language, database):
        """Sam postopek analize, ki teče v ozadju."""
        try:
            # 1. Klic analizatorja, točno tako kot dela v cli.py
            result = self.analyzer.analyze(code=code, language=language, database=database)
            
            # 2. Generiramo testno poročilo
            report_text = generate_report(result)
            
            # 3. Prikažemo rezultat v glavnem threadu
            self.root.after(0, self.update_result, report_text, True)
            
        except Exception as e:
            error_msg = f"An error occurred during analysis:\n{str(e)}"
            self.root.after(0, self.update_result, error_msg, True)

    def update_result(self, text, clear=False):
        """Varno posodobi rezultatsko tekstovno polje."""
        self.result_output.config(state=tk.NORMAL)
        if clear:
            self.result_output.delete("1.0", tk.END)
        self.result_output.insert(tk.END, text)
        self.result_output.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityAnalyzerApp(root)
    root.mainloop()
