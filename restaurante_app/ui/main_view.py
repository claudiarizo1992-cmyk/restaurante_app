import tkinter as tk    
from tkinter import ttk, messagebox

class MainView(tk.Tk):
    def __init__(self, servicio, usuario):
        super().__init__()
        self.servicio = servicio
        self.usuario = usuario

        self.title(f"Restaurante App - Usuario: {self.usuario.nombre} ({self.usuario.rol})")
        self.geometry("850x550")
        self.minsize(800, 500)

        self._crear_estructura_principal()

    def _crear_estructura_principal(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text="Consulta de Usuarios")
        self._construir_pestana_usuarios()

    def _construir_pestana_productos(self):
        frame_top = ttk.LabelFrame(self.tab_productos, text=" Formulario de Producto ", padding=10)
        frame_top.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_top, text="ID Producto:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_prod_nombre = ttk.Entry(frame_top, width=25)
        self.ent_prod_nombre.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        ttk.Label(frame_top, text="Precio ($):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.ent_prod_precio = ttk.Entry(frame_top, width=15)
        self.ent_prod_precio.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(frame_top, text="Categoria:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.cmb_prod_cat = ttk.Combobox(frame_top, values=["Platos Fuertes", "Bebidas", "Postres", "Enmtrada"], width=22, state="readonly")
        self.cmb_prod_cat.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)

        frame_botones = ttk.Frame(frame_top)
        frame_botones.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(frame_botones, text="Registrar", command=self._cmd_registrar)
        ttk.Button(frame_botones, text="Cargar / Consultar", command=self._cmd_consultar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Actualizar", command=self.cmd_actualizar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self._cmd_eliminar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Limpiar Formulario",command=self._limpiar_formulario).pack(side=tk.LEFT, padx=5)

        frame_bottom = ttk.LabelFrame(self.tab_productos, text=" Catalogo de Productos ", padding=10)
        frame_bottom.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("id", "nombre", "precio", "categoria")
        self.tree_prod = ttk.Treeview(frame_bottom, columns=columns, show="headings")
        self.tree_prod.heading("id", text="ID")
        self.tree_prod.heading("nombre", text="Nombre del Producto")
        self.tree_prod.heading("precio", text="Precio ($)")
        self.tree_prod.heading("categoria", text="Categoria")

        self.tree_prod.column("id", width=100, anchor=tk.CENTER)
        self.tree_prod.column("nombre", width=300)
        self.tree_prod.column("precio", width=120, anchor=tk.E)
        self.tree_prod.column("categoria", width=180)

        scrollbar = ttk.Scrollbar(frame_bottom, orient=tk.VERTICAL, command=self.tree_prod.yview)
        self.tree_prod.configure(yscroll=scrollbar.set)

        self.tree_prod.pack(side=tk.LEFT, fill=tk.BOTH, expand= True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._refrescar_tabla_productos()

    def _cmd_registrar(self):
        try:
            self.servicio.registrar_producto(
                self.ent_prod_id.get().strip(),
                self.ent_prod_nombre.get().strip(),
                self.ent_prod_precio.get().strip(),
                self.cmb_prod_cat.get().strip()
            )
            messagebox.showinfo("Exito", "Producto registado correctamente.")
            self._limpiar_formulario()
            self._refrescar_tabla_productos()
        except ValueError as e:
            messagebox.showerror("Error de Validacion", str(e))

    def _cmd_consultar(self):
        id_prod = self.ent_prod_id.get().strip()
        if not id_prod:
            messagebox.showwarning("Atencion", "Ingrese un ID de producto para consultar.")
            return

        producto = self.servicio.buscar_producto(id_prod)
        if producto:
            self.ent_prod_nombre.delete(0, tk.END)
            self.ent_prod_nombre.insert(0, producto.nombre)
            self.ent_prod_precio.delete(0, tk.END)
            self.ent_prod_precio.insert(0, str(producto.precio))
            self.cmb_prod_cat.set(producto.categoria)
            messagebox.showinfo("Informacion", f"Producto '{id_prod}' cargado en el formulario.")
        else:
            messagebox.showerror("Error", f"No existe un producto con ID '{id_prod}'.")

    def _cmd_actualizar(self):
        try:
            self.servicio.actualizar_producto( 
            self.ent_prod_id.get().strip(),
            self.ent_prod_nombre.get().strip(),
            self.ent_prod_precio.get().strip(),
            self.cmb_prod_cat.get().strip()
            )
            messagebox.showinfo("Exito", "Producto actualizado correctamente.")
            self._limpiar_formulario()
            self._refrescar_tabla_productos()
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 

    def _cmd_eliminar(self):
        id_prod = self.ent_prod_id.get().strip()
        if not id_prod:
            messagebox.showwarning("Atencion", "Ingrese el ID del producto que desea eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Esta seguro de eliminar el producto {id_prod}?"):
            try:
                self.servicio.eliminar_producto (id_prod)
                messagebox.showinfo("Exito", "Producto eliminado correctamente.")
                self._limpiar_formulario()
                self._refrescar_tabla_producto()
            except ValueError as e:
                messagebox.showerror("Error", str(e))    

    def _limpiar_formulario(self):
        self.ent_prod_id.delete(0, tk.END)
        self.ent_prod_nombre.delete(0, tk.END)
        self.ent_prod_precio.delete(0,tk.END)
        self.cmb_prod_cat.set("") 

    def _refrescar_tabla_productos(self):
        for item in self.tree_prod.get_children():
            self.tree_prod.delete(item)
            productos = self.servicio.obtener_productos()
            for p in productos:
                self.tree_prod.insert("", tk.END, values=(p.id_producto, p.nombre, f"{p.precio:2.f}", p.categoria)) 

    def _construir_pestana_usuarios(self):
        frame_user = ttk.LabelFrame(self.tab_usuarios, text=" Usuarios Registrados ", padding=10)
        frame_user.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Username", "nombre", "rol")
        tree_user = ttk.Treeview(frame_user, columns=columns, show="headings")
        tree_user.heading("username", text="Usuario")
        tree_user.heading("nombre", text="Nombre Completo")
        tree_user.heading("rol", text="Rol de Sistema")

        tree_user.column("username", width=150)
        tree_user.column("nombre", width=300)
        tree_user.column("rol", width=150)

        tree_user.pack(fill=tk.BOTH, expand=True)

        usuarios = self.servicio.obtener_usuarios()
        for u in usuarios:
            tree_user.insert("", tk.END, values=(u.username, u.nombre, u.rol))

