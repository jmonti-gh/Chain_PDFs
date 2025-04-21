import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.pdf_files = []

        # Frame principal
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Lista de archivos
        self.file_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=50, height=15)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        # Botones
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.add_button = tk.Button(self.button_frame, text="Agregar PDF", command=self.add_pdf)
        self.add_button.grid(row=0, column=0, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Eliminar PDF", command=self.remove_pdf)
        self.remove_button.grid(row=0, column=1, padx=5)

        self.up_button = tk.Button(self.button_frame, text="Mover Arriba", command=self.move_up)
        self.up_button.grid(row=0, column=2, padx=5)

        self.down_button = tk.Button(self.button_frame, text="Mover Abajo", command=self.move_down)
        self.down_button.grid(row=0, column=3, padx=5)

        self.merge_button = tk.Button(root, text="Unir PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=10)

        # Habilitar arrastrar y soltar
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_files)

    def add_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.add_file_to_list(file)

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.endswith(".pdf"):
                self.add_file_to_list(file)

    def add_file_to_list(self, file):
        if file in self.pdf_files:
            messagebox.showwarning("Advertencia", f"El archivo '{file}' ya está en la lista.")
        self.pdf_files.append(file)
        self.file_listbox.insert(tk.END, file)

    def remove_pdf(self):
        selected = self.file_listbox.curselection()
        if selected:
            index = selected[0]
            self.file_listbox.delete(index)
            del self.pdf_files[index]

    def move_up(self):
        selected = self.file_listbox.curselection()
        if selected:
            index = selected[0]
            if index > 0:
                self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
                self.update_listbox()

    def move_down(self):
        selected = self.file_listbox.curselection()
        if selected:
            index = selected[0]
            if index < len(self.pdf_files) - 1:
                self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
                self.update_listbox()

    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.pdf_files:
            self.file_listbox.insert(tk.END, file)

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("Error", "No hay archivos para unir.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_file:
            return

        merger = PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)

        try:
            merger.write(output_file)
            merger.close()
            messagebox.showinfo("Éxito", f"Archivos unidos en '{output_file}'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo unir los archivos: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFMergerApp(root)
    root.mainloop()