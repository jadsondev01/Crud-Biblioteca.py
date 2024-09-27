import tkinter as tk
from tkinter import messagebox, ttk
from controllers.library_controller import LibraryController

class LibraryView:
    def __init__(self, root):
        self.root = root
        self.controller = LibraryController(self)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.root.geometry("800x600")

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TEntry", font=("Arial", 10))
        self.style.configure("TTreeview", background="#f9f9f9", foreground="black", rowheight=25)
        self.style.configure("TTreeview.Heading", background="#007bff", foreground="white", font=("Arial", 11, 'bold'))

        # Configurar abas
        self.tab_control = ttk.Notebook(self.root)

        self.books_tab = ttk.Frame(self.tab_control)
        self.users_tab = ttk.Frame(self.tab_control)
        self.loans_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.books_tab, text='Livros')
        self.tab_control.add(self.users_tab, text='Usuários')
        self.tab_control.add(self.loans_tab, text='Empréstimos')

        self.tab_control.pack(expand=1, fill='both')

        self.create_books_tab()
        self.create_users_tab()
        self.create_loans_tab()

    def create_books_tab(self):
        input_frame = ttk.LabelFrame(self.books_tab, text='Adicionar Livro', padding=(10, 10))
        input_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(input_frame, text='Título:').grid(row=0, column=0, sticky='w')
        self.book_title_entry = tk.Entry(input_frame)
        self.book_title_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(input_frame, text='Autor:').grid(row=1, column=0, sticky='w')
        self.book_author_entry = tk.Entry(input_frame)
        self.book_author_entry.grid(row=1, column=1, sticky='ew')

        ttk.Label(input_frame, text='ISBN:').grid(row=2, column=0, sticky='w')
        self.book_isbn_entry = tk.Entry(input_frame)
        self.book_isbn_entry.grid(row=2, column=1, sticky='ew')

        # Botões de Ação para Adicionar Livro
        action_frame = ttk.Frame(input_frame)
        action_frame.grid(row=3, columnspan=2, pady=5)

        add_button = tk.Button(action_frame, text='Adicionar Livro', command=self.add_book, bg='green', fg='white')
        add_button.grid(row=0, column=0)

        list_button = tk.Button(action_frame, text='Listar Livros', command=self.controller.list_books, bg='blue', fg='white')
        list_button.grid(row=0, column=1, padx=5)

        remove_button = tk.Button(action_frame, text='Remover Livro', command=self.controller.remove_book, bg='red', fg='white')
        remove_button.grid(row=0, column=2, padx=5)

        edit_button = tk.Button(action_frame, text='Editar Livro', command=self.controller.edit_book, bg='yellow', fg='black')
        edit_button.grid(row=0, column=3, padx=5)

        # Seção de Pesquisa de Livros
        search_frame = ttk.LabelFrame(self.books_tab, text='Pesquisar Livro', padding=(10, 10))
        search_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(search_frame, text='Título:').grid(row=0, column=0, sticky='w')
        self.search_title_entry = tk.Entry(search_frame)
        self.search_title_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(search_frame, text='Autor:').grid(row=1, column=0, sticky='w')
        self.search_author_entry = tk.Entry(search_frame)
        self.search_author_entry.grid(row=1, column=1, sticky='ew')

        ttk.Label(search_frame, text='ISBN:').grid(row=2, column=0, sticky='w')
        self.search_isbn_entry = tk.Entry(search_frame)
        self.search_isbn_entry.grid(row=2, column=1, sticky='ew')

        # Botões de Pesquisa
        action_search_frame = ttk.Frame(search_frame)
        action_search_frame.grid(row=3, columnspan=2, pady=5)

        search_by_title_button = tk.Button(action_search_frame, text='Pesquisar por Título', command=self.search_book_by_title, bg='blue', fg='white')
        search_by_title_button.grid(row=0, column=0, padx=5)

        search_by_author_button = tk.Button(action_search_frame, text='Pesquisar por Autor', command=self.search_book_by_author, bg='blue', fg='white')
        search_by_author_button.grid(row=0, column=1, padx=5)

        search_by_isbn_button = tk.Button(action_search_frame, text='Pesquisar por ISBN', command=self.search_book_by_isbn, bg='blue', fg='white')
        search_by_isbn_button.grid(row=0, column=2, padx=5)

        self.books_tree = ttk.Treeview(self.books_tab, columns=('ID', 'Título', 'Autor', 'ISBN'), show='headings')
        self.books_tree.pack(padx=10, pady=10, fill='both', expand=True)
        for col in self.books_tree['columns']:
            self.books_tree.heading(col, text=col)

    def create_users_tab(self):
        input_frame = ttk.LabelFrame(self.users_tab, text='Adicionar Usuário', padding=(10, 10))
        input_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(input_frame, text='Nome:').grid(row=0, column=0, sticky='w')
        self.user_name_entry = tk.Entry(input_frame)
        self.user_name_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(input_frame, text='Tipo:').grid(row=1, column=0, sticky='w')
        self.user_type_combobox = ttk.Combobox(input_frame, values=["admin", "librarian", "member"])
        self.user_type_combobox.grid(row=1, column=1, sticky='ew')

        # Botões de Ação
        action_frame = ttk.Frame(input_frame)
        action_frame.grid(row=2, columnspan=2, pady=5)

        add_user_button = tk.Button(action_frame, text='Adicionar Usuário', command=self.add_user, bg='green', fg='white')
        add_user_button.grid(row=0, column=0)

        list_user_button = tk.Button(action_frame, text='Listar Usuários', command=self.controller.list_users, bg='blue', fg='white')
        list_user_button.grid(row=0, column=1, padx=5)

        remove_user_button = tk.Button(action_frame, text='Remover Usuário', command=self.controller.remove_user, bg='red', fg='white')
        remove_user_button.grid(row=0, column=2, padx=5)

        edit_user_button = tk.Button(action_frame, text='Editar Usuário', command=self.controller.edit_user, bg='yellow', fg='black')
        edit_user_button.grid(row=0, column=3, padx=5)

        self.users_tree = ttk.Treeview(self.users_tab, columns=('ID', 'Nome', 'Tipo'), show='headings')
        self.users_tree.pack(padx=10, pady=10, fill='both', expand=True)
        for col in self.users_tree['columns']:
            self.users_tree.heading(col, text=col)

    def create_loans_tab(self):
        input_frame = ttk.LabelFrame(self.loans_tab, text='Registrar Empréstimo', padding=(10, 10))
        input_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(input_frame, text='ID do Livro:').grid(row=0, column=0, sticky='w')
        self.loan_book_id_entry = tk.Entry(input_frame)
        self.loan_book_id_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(input_frame, text='ID do Usuário:').grid(row=1, column=0, sticky='w')
        self.loan_user_id_entry = tk.Entry(input_frame)
        self.loan_user_id_entry.grid(row=1, column=1, sticky='ew')

        ttk.Label(input_frame, text='Data do Empréstimo (YYYY-MM-DD):').grid(row=2, column=0, sticky='w')
        self.loan_date_entry = tk.Entry(input_frame)
        self.loan_date_entry.grid(row=2, column=1, sticky='ew')

        ttk.Label(input_frame, text='Data de Devolução (YYYY-MM-DD):').grid(row=3, column=0, sticky='w')
        self.due_date_entry = tk.Entry(input_frame)
        self.due_date_entry.grid(row=3, column=1, sticky='ew')

        # Botões de Ação
        action_frame = ttk.Frame(input_frame)
        action_frame.grid(row=4, columnspan=2, pady=5)

        register_loan_button = tk.Button(action_frame, text='Registrar Empréstimo', command=self.register_loan, bg='green', fg='white')
        register_loan_button.grid(row=0, column=0)

        list_loan_button = tk.Button(action_frame, text='Listar Empréstimos', command=self.controller.list_loans, bg='blue', fg='white')
        list_loan_button.grid(row=0, column=1, padx=5)

        return_loan_button = tk.Button(action_frame, text='Registrar Devolução', command=self.controller.return_loan, bg='green', fg='white')
        return_loan_button.grid(row=0, column=2, padx=5)

        remove_loan_button = tk.Button(action_frame, text='Excluir Empréstimo', command=self.controller.remove_loan, bg='red', fg='white')
        remove_loan_button.grid(row=0, column=3, padx=5)

        self.loans_tree = ttk.Treeview(self.loans_tab, columns=('ID', 'ID Livro', 'ID Usuário', 'Data do Empréstimo', 'Data de Devolução'), show='headings')
        self.loans_tree.pack(padx=10, pady=10, fill='both', expand=True)
        for col in self.loans_tree['columns']:
            self.loans_tree.heading(col, text=col)

    def add_book(self):
        title = self.book_title_entry.get().strip()
        author = self.book_author_entry.get().strip()
        isbn = self.book_isbn_entry.get().strip()

        if not title or not author or not isbn:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        self.controller.add_book(title, author, isbn)
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_isbn_entry.delete(0, tk.END)

    def add_user(self):
        name = self.user_name_entry.get().strip()
        user_type = self.user_type_combobox.get()

        if not name or not user_type:
            messagebox.showerror("Erro", "Nome e tipo de usuário devem ser preenchidos.")
            return

        self.controller.add_user(name, user_type)
        self.user_name_entry.delete(0, tk.END)
        self.user_type_combobox.set('')

    def register_loan(self):
        book_id = self.loan_book_id_entry.get().strip()
        user_id = self.loan_user_id_entry.get().strip()
        loan_date = self.loan_date_entry.get().strip()
        due_date = self.due_date_entry.get().strip()

        if not book_id or not user_id or not loan_date or not due_date:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        self.controller.register_loan(book_id, user_id, loan_date, due_date)
        self.loan_book_id_entry.delete(0, tk.END)
        self.loan_user_id_entry.delete(0, tk.END)
        self.loan_date_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

    def search_book_by_title(self):
        title = self.search_title_entry.get().strip()
        if not title:
            messagebox.showerror("Erro", "Por favor, insira um título.")
            return
        self.controller.search_book_by_title(title)

    def search_book_by_author(self):
        author = self.search_author_entry.get().strip()
        if not author:
            messagebox.showerror("Erro", "Por favor, insira um autor.")
            return
        self.controller.search_book_by_author(author)

    def search_book_by_isbn(self):
        isbn = self.search_isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Erro", "Por favor, insira um ISBN.")
            return
        self.controller.search_book_by_isbn(isbn)

    def display_message(self, title, message):
        messagebox.showinfo(title, message)

    def update_books_tree(self, books):
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)
        for book in books:
            self.books_tree.insert("", tk.END, values=(book['id'], book['title'], book['author'], book['isbn']))

    def update_users_tree(self, users):
        for row in self.users_tree.get_children():
            self.users_tree.delete(row)
        for user in users:
            self.users_tree.insert("", tk.END, values=(user['id'], user['name'], user['user_type']))

    def update_loans_tree(self, loans):
        for row in self.loans_tree.get_children():
            self.loans_tree.delete(row)
        for loan in loans:
            self.loans_tree.insert("", tk.END, values=(loan['id'], loan['book_id'], loan['user_id'], loan['loan_date'], loan['due_date']))


# O código deve ser executado a partir deste ponto, por exemplo:
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryView(root)
    root.mainloop()
