"""Ponto de entrada reservado para a versão desktop com Tkinter.

A versão desktop será implementada após validarmos os casos de uso compartilhados
pela interface web. Execute com: python -m app.interfaces.desktop.main
"""
import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title('AutoTech — Oficina mecânica')
    root.geometry('760x440')
    root.minsize(640, 360)

    frame = ttk.Frame(root, padding=28)
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='AutoTech', font=('Segoe UI', 24, 'bold')).pack(anchor='w')
    ttk.Label(frame, text='Versão desktop — estrutura inicial', font=('Segoe UI', 12)).pack(anchor='w', pady=(4, 18))
    ttk.Label(
        frame,
        text=('A interface desktop será conectada à mesma camada de serviços usada pela versão web.\n'
              'Primeiro, valide os cadastros e as regras de negócio na versão web.'),
        justify='left', wraplength=650,
    ).pack(anchor='w')
    ttk.Button(frame, text='Fechar', command=root.destroy).pack(anchor='e', pady=24)
    root.mainloop()


if __name__ == '__main__':
    main()
