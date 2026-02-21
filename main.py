import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import csv

# --- Resource Setup ---
def download_resources():
    resources = ['punkt', 'punkt_tab', 'averaged_perceptron_tagger_eng', 'universal_tagset']
    for res in resources:
        try:
            nltk.download(res, quiet=True)
        except:
            pass

download_resources()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LinguistPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LinguistPro - Advanced POS Detector")
        self.geometry("1100x850")

        # Data storage for saving
        self.last_analysis = []

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(self, text="Advanced Parts of Speech Analyzer", font=("Helvetica", 24, "bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20)

        # Input Box
        self.textbox = ctk.CTkTextbox(self, width=800, height=200, font=("Inter", 14))
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.textbox.insert("0.0", "Apple is eating a fruit in London.")

        # Button Row
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, pady=20)

        self.upload_btn = ctk.CTkButton(self.btn_frame, text="📁 Upload File", fg_color="#3498db", command=self.upload_file)
        self.upload_btn.grid(row=0, column=0, padx=5)

        self.analyze_btn = ctk.CTkButton(self.btn_frame, text="🔍 Analyze", fg_color="#2ecc71", command=self.analyze_text)
        self.analyze_btn.grid(row=0, column=1, padx=5)

        # --- SAVE BUTTON ---
        self.save_btn = ctk.CTkButton(self.btn_frame, text="💾 Save Results", fg_color="#f39c12", state="disabled", command=self.save_results)
        self.save_btn.grid(row=0, column=2, padx=5)

        self.clear_btn = ctk.CTkButton(self.btn_frame, text="🗑️ Clear", fg_color="#e74c3c", command=lambda: self.textbox.delete("1.0", "end"))
        self.clear_btn.grid(row=0, column=3, padx=5)

        # Results Display
        self.results_area = ctk.CTkScrollableFrame(self, label_text="Detailed Analysis", width=800, height=350)
        self.results_area.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_rowconfigure(3, weight=2)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.textbox.delete("1.0", "end")
                    self.textbox.insert("1.0", file.read())
                    self.analyze_text()
            except Exception as e:
                messagebox.showerror("Error", f"Read Error: {e}")

    def save_results(self):
        """Saves the analyzed data to a CSV or TXT file."""
        if not self.last_analysis:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("Text File", "*.txt")],
            title="Save Analysis As"
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    with open(file_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Word", "Tag", "Description"])
                        writer.writerows(self.last_analysis)
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("Word | Tag | Description\n" + "-"*30 + "\n")
                        for row in self.last_analysis:
                            f.write(f"{row[0]} | {row[1]} | {row[2]}\n")
                
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Save Error: {e}")

    def get_detailed_pos(self, tag):
        tag_map = {
            'NN': 'Noun (Common/Singular)', 'NNS': 'Noun (Common/Plural)',
            'NNP': 'Noun (Proper/Singular)', 'NNPS': 'Noun (Proper/Plural)',
            'VB': 'Verb (Base Form)', 'VBD': 'Verb (Past Tense)',
            'VBG': 'Verb (Gerund/Participle)', 'VBN': 'Verb (Past Participle)',
            'VBP': 'Verb (Present)', 'VBZ': 'Verb (Present 3rd Person)',
            'PRP': 'Pronoun', 'JJ': 'Adjective', 'IN': 'Preposition',
            'CC': 'Conjunction', 'RB': 'Adverb', 'DT': 'Determiner'
        }
        return tag_map.get(tag, f"Other ({tag})")

    def analyze_text(self):
        for widget in self.results_area.winfo_children():
            widget.destroy()

        input_text = self.textbox.get("1.0", "end-1c").strip()
        if not input_text: return

        try:
            tokens = word_tokenize(input_text)
            tagged = pos_tag(tokens)
            self.last_analysis = [] # Reset storage

            # Header
            ctk.CTkLabel(self.results_area, text="WORD", font=("Arial", 12, "bold"), text_color="#3498db").grid(row=0, column=0, padx=20, pady=5, sticky="w")
            ctk.CTkLabel(self.results_area, text="DETAILED CATEGORY", font=("Arial", 12, "bold"), text_color="#3498db").grid(row=0, column=1, padx=20, pady=5, sticky="w")

            for i, (word, tag) in enumerate(tagged, start=1):
                detail = self.get_detailed_pos(tag)
                self.last_analysis.append([word, tag, detail]) # Store for saving
                
                ctk.CTkLabel(self.results_area, text=word).grid(row=i, column=0, padx=20, pady=2, sticky="w")
                ctk.CTkLabel(self.results_area, text=detail, text_color="#bdc3c7").grid(row=i, column=1, padx=20, pady=2, sticky="w")
            
            self.save_btn.configure(state="normal") # Enable saving

        except Exception as e:
            ctk.CTkLabel(self.results_area, text=f"Error: {e}", text_color="red").pack()

if __name__ == "__main__":
    app = LinguistPro()
    app.mainloop()