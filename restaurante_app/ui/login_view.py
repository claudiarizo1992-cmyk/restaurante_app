import tkinter as tk    
from tkinter import ttk, messagebox

class   LoginView(tk.Tk):
    def __init__(self, servicio, on_login_success):
        super().__init__()
        self.servicio = servicio
        self.on_login_success = on_login_success

        self.title("Restaurante App - Inicio de Sesion")
        self.geometry("380x300")
        self.resizable(False, False)

        self._crear_componentes()

    def _crear_componentes(self):
        frame_login = ttk.LabelFrame(self, text=" Acceso al Sistema ", padding=20)
        frame_login.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(frame_login, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.ent_user = ttk.Entry(frame_login, width=25)
        self.ent_user.grid(row=0, column=1, pady=8) 

        ttk.Label(frame_login, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.ent_pass = ttk.Entry(frame_login, width=25, show="*")
        self.ent_pass.grid(row=1, column=1, pady=8)

        btn_ingresar = ttk.Button(frame_login, text="Iniciar Sesion", command=self._ejecutar_login)
        btn_ingresar.grid(row=2, column=0, columnspan=2, pady=15)

    def _ejecutar_login(self):
        user = self.ent_user.get().strip()
        pwd = self.ent_pass.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Atencion", "Ingrese usuario y contraseña.")
            return

        usuario_autenticado = self.servicio.autenticar(user, pwd)
        if usuario_autenticado:
            self.destroy()
            self.on_login_success(usuario_autenticado)
        else: 
            messagebox.showerror("Error", "Credenciales incorrectas.")

