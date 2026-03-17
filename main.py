import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from converter import BudgetLookup, ZR3File, Converter

law_options = [
    'п.4, ч.1, ст.93 ФЗ от 05.04.2013 N44-ФЗ',
    'п.2, ч.1, ст.93; ч.7, ст.103 ФЗ от 05.04.2013 №44-ФЗ'
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ZR3 Converter v1.1')
        self.geometry('600x400')
        self.input_file = None
        self.budget_lookup = BudgetLookup(Path('budget_lookup.csv'))
        self._build_ui()

    def _build_ui(self):
        frame_top = tk.Frame(self)
        frame_top.pack(padx=10, pady=10, fill='x')

        tk.Button(frame_top, text='Выбрать файл', command=self._pick_file).pack(side='left')

        self.lbl_file = tk.Label(frame_top, text='Файл не выбран.', anchor='w')
        self.lbl_file.pack(side='left', padx=10, fill='x', expand=True)

        tk.Button(self, text='Конвертировать', command=self._run).pack(pady=5)

        self.log_text = tk.Text(self, height=15, state='disabled')
        self.log_text.pack(padx=10, pady=5, fill='both', expand=True)

        self.lbl_status = tk.Label(self, text='', anchor='w', fg='green')
        self.lbl_status.pack(padx=10, pady=5, fill='x')

    def _pick_file(self):
        path =  filedialog.askopenfilename(
            filetypes=[('ZR3 files', '*.ZR3'), ('All files', '*.*')]
        )
        if path:
            self.input_file = Path(path)
            self.lbl_file.config(text=str(self.input_file))

    def _choose_record_dialog(self, record_number: str, recipient_name: str, candidates: list) -> dict:
        dialog = tk.Toplevel(self)
        dialog.title('Выбор КБК')
        dialog.geometry('400x200')
        dialog.grab_set()

        name = recipient_name[:50] + '...' if len(recipient_name) > 50 else recipient_name
        tk.Label(dialog, text=f'ЗКР {record_number} | {name}', wraplength=380).pack(pady=10)

        choice = tk.IntVar(value=0)
        for i, rec in enumerate(candidates):
            tk.Radiobutton(
                dialog,
                text = f'КБК {rec['kbk']} ОКТМО {rec['oktmo']}',
                variable=choice,
                value=i
            ).pack(anchor='w', padx=20)

        result = {}
        def confirm():
            result['rec'] = candidates[choice.get()]
            dialog.destroy()
        
        tk.Button(dialog, text='Выбрать', command=confirm).pack(pady=10)

        self.wait_window(dialog)

        return result.get('rec', candidates[0])

    def _choose_law_dialog(self, record_number: str, sum: str) -> str:
        dialog = tk.Toplevel(self)
        dialog.title('Выбор статьи')
        dialog.geometry('500x150')
        dialog.grab_set()

        tk.Label(dialog, text=f'ЗКР {record_number} на {sum} р. - какую статью использовать?').pack(pady=10)
        choice = tk.IntVar(value=0)
        for i, law in enumerate(law_options):
            tk.Radiobutton(
                dialog,
                text=law,
                variable=choice,
                value=i,
                wraplength=460,
                justify='left'
            ).pack(anchor='w', padx=20)

        result = {}
        def confirm():
            result['law'] = law_options[choice.get()]
            dialog.destroy()

        tk.Button(dialog, text='Выбрать', command=confirm).pack(pady=10)
        self.wait_window(dialog)

        selected = result.get('law')
        if selected is not None:
            return selected
        return law_options[0]

    def _log(self, message: str):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.see('end')  # auto-scroll to bottom
    
    def _run(self):
        if not self.input_file:
            messagebox.showwarning('Внимание', 'Сначала выберите файл.')
            return

        try:
            zr3 = ZR3File(self.input_file)
            converter = Converter(zr3, self.budget_lookup, 
                                  log_callback=self._log, choose_callback=self._choose_record_dialog,
                                  choose_law=self._choose_law_dialog)

            for line in converter.preview():
                self._log(line)

            output_lines = converter.convert()

            output_path = self.input_file.with_stem(self.input_file.stem + '_done')
            zr3.write(output_path, output_lines)

            self.lbl_status.config(text=f'Сохранено: {output_path}')
            self._log(f'✓ Готово - {output_path.name}')

        except Exception as e:
            messagebox.showerror('Ошибка', str(e))
    
if __name__ == '__main__':
    App().mainloop()