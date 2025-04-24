

## Libraries
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PyPDF2 import PdfMerger


## pyinstaller --onefile --windowed --add-data "<ruta_a_tkinterdnd2>\tkdnd;tkinterdnd2\tkdnd" chain_PDFs_deep.py
## pyinstaller --onefile --windowed --add-data "C:\Users\jmonti\AppData\Local\Programs\Python\Python311\Lib\site-packages\tkinterdnd2\tkdnd;tkinterdnd2\tkdnd" chain_PDFs_deep.py

#pyinstaller --onefile mi_programa.py
#pyinstaller --onefile --windowed mi_programa.py
#pyinstaller --onefile --windowed --add-data "C:\Users\Usuario\Documents\mi_programa.py;." mi_programa.py
#pyinstaller --onefile --windowed --add-data "C:\Users\Usuario\Documents\mi_programa.py;." --add-data "C:\Users\Usuario\Documents\mi_programa.py;." mi_programa.py
# pyinstaller --onefile --windowed --add-data "C:\Users\jm\AppData\Local\Programs\Python\Python311\Lib\site-packages\tkinterdnd2\tkdnd;." chain_PDFs_deep.py
# pyinstaller --onefile --windowed --add-data "C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." chain_PDFs_deep.py
# pyinstaller --onefile --windowed --add-data "C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." --add-data "C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." chain_PDFs_deep.py

# python -m nuitka --standalone --windows-disable-console --onefile chain_PDFs_deep.py --include-package=tkinterdnd2 --include-package=PyPDF2 --include-data-dir="C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." --include-data-dir="C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." --output-dir=dist chain_PDFs_deep.py
# python -m nuitka --standalone ----windows-console-mode=disable --onefile chain_PDFs_deep.py --include-package=tkinterdnd2 --include-package=PyPDF2 --include-data-dir="C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." --include-data-dir="C:\Users\jm\Documents\ChainPDFs\pys\chain_PDFs_deep.py;." --output-dir=dist chain_PDFs_deep.py
# python -m nuitka --standalone --windows-console-mode=disable --onefile --enable-plugin=tk-inter chain_PDFs_deep.py


## App in a Class
class PDFMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Combinador de PDFs")
        self.geometry("600x500")
        self.configure(bg='#f0f0f0')
        
        # Variables
        self.pdf_files = []
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5, font=('Arial', 10))
        self.style.configure('TLabel', padding=5, font=('Arial', 10))
        
        # Widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label de instrucciones
        lbl_instructions = ttk.Label(main_frame, text="Arrastra y suelta archivos PDF aquí o usa el botón 'Agregar'")
        lbl_instructions.pack(pady=(0, 10))
        
        # Listbox para mostrar los PDFs
        self.listbox = tk.Listbox(
            main_frame, 
            selectmode=tk.SINGLE, 
            height=10,
            width=60,
            bg='white',
            font=('Arial', 10),
            relief=tk.SUNKEN,
            highlightthickness=0
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configurar DnD
        self.listbox.drop_target_register('DND_Files')
        self.listbox.dnd_bind('<<Drop>>', self.drop)
        
        # Frame de botones de control
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control
        btn_add = ttk.Button(control_frame, text="Agregar PDF(s)", command=self.add_files)
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_remove = ttk.Button(control_frame, text="Eliminar", command=self.remove_file)
        btn_remove.pack(side=tk.LEFT, padx=5)
        
        btn_up = ttk.Button(control_frame, text="Subir", command=self.move_up)
        btn_up.pack(side=tk.LEFT, padx=5)
        
        btn_down = ttk.Button(control_frame, text="Bajar", command=self.move_down)
        btn_down.pack(side=tk.LEFT, padx=5)
        
        # Frame para guardar
        save_frame = ttk.Frame(main_frame)
        save_frame.pack(fill=tk.X)
        
        lbl_save = ttk.Label(save_frame, text="Archivo de salida:")
        lbl_save.pack(side=tk.LEFT, padx=(0, 5))
        
        self.output_var = tk.StringVar()
        self.entry_output = ttk.Entry(save_frame, textvariable=self.output_var, width=40)
        self.entry_output.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        btn_browse = ttk.Button(save_frame, text="Examinar", command=self.browse_output)
        btn_browse.pack(side=tk.LEFT)
        
        # Botón de combinar
        btn_merge = ttk.Button(main_frame, text="COMBINAR PDFs", command=self.merge_pdfs, style='TButton')
        btn_merge.pack(fill=tk.X, pady=(10, 0))
    
    def drop(self, event):
        # Obtener los archivos soltados
        files = self.tk.splitlist(event.data)
        for file in files:
            file_path = file.strip('{}')  # Eliminar llaves si las hay
            if file_path.lower().endswith('.pdf'):
                self.add_pdf_to_list(file_path)
            else:
                messagebox.showwarning("Archivo no válido", f"El archivo {os.path.basename(file_path)} no es un PDF.")
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        for file in files:
            self.add_pdf_to_list(file)
    
    def add_pdf_to_list(self, file_path):
        # Verificar si el archivo ya está en la lista
        if file_path in self.pdf_files:
            messagebox.showwarning(
                "Archivo duplicado",
                f"El archivo {os.path.basename(file_path)} ya está en la lista.\n\n"
                "Se agregará de todos modos, pero verifica que sea intencional."
            )
        
        # Agregar a la lista y al listbox
        self.pdf_files.append(file_path)
        self.listbox.insert(tk.END, os.path.basename(file_path))
    
    def remove_file(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.listbox.delete(index)
            self.pdf_files.pop(index)
    
    def move_up(self):
        selected = self.listbox.curselection()
        if selected and selected[0] > 0:
            index = selected[0]
            # Mover en la lista de archivos
            self.pdf_files[index], self.pdf_files[index-1] = self.pdf_files[index-1], self.pdf_files[index]
            # Mover en el listbox
            item = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index-1, item)
            self.listbox.selection_set(index-1)
    
    def move_down(self):
        selected = self.listbox.curselection()
        if selected and selected[0] < len(self.pdf_files)-1:
            index = selected[0]
            # Mover en la lista de archivos
            self.pdf_files[index], self.pdf_files[index+1] = self.pdf_files[index+1], self.pdf_files[index]
            # Mover en el listbox
            item = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index+1, item)
            self.listbox.selection_set(index+1)
    
    def browse_output(self):
        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF combinado como",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if output_file:
            self.output_var.set(output_file)
    
    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("Error", "No hay archivos PDF para combinar.")
            return
        
        output_path = self.output_var.get().strip()
        if not output_path:
            messagebox.showerror("Error", "Debes especificar un archivo de salida.")
            return
        
        try:
            merger = PdfMerger()
            
            for pdf in self.pdf_files:
                merger.append(pdf)
            
            with open(output_path, 'wb') as f:
                merger.write(f)
            
            messagebox.showinfo("Éxito", f"PDFs combinados exitosamente en:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo combinar los PDFs:\n{str(e)}")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()