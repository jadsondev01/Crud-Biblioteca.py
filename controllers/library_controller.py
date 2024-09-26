from db.database import (
    add_book, edit_book, remove_book, list_books,
    add_user, edit_user, remove_user, list_users,
    register_loan, return_loan, remove_loan, list_loans
)
from tkinter import simpledialog

class LibraryController:
    def __init__(self, view):
        self.view = view

    def add_book(self, title, author, isbn):
        add_book(title, author, isbn)
        self.view.display_message("Info", "Livro adicionado com sucesso!")
        self.list_books()  # Atualiza a lista após adicionar

    def list_books(self):
        books = list_books()
        self.view.update_books_tree(books)

    def remove_book(self):
        selected_item = self.view.books_tree.selection()
        if not selected_item:
            self.view.display_message("Warning", "Selecione um livro para remover.")
            return
        isbn = self.view.books_tree.item(selected_item)['values'][3]  # Obtem o ISBN
        remove_book(isbn)
        self.view.display_message("Info", "Livro removido com sucesso!")
        self.list_books()

    def edit_book(self):
        selected_item = self.view.books_tree.selection()
        if not selected_item:
            self.view.display_message("Warning", "Selecione um livro para editar.")
            return
        book_data = self.view.books_tree.item(selected_item)['values']
        new_title = simpledialog.askstring("Input", "Novo Título:", initialvalue=book_data[1])
        new_author = simpledialog.askstring("Input", "Novo Autor:", initialvalue=book_data[2])
        new_isbn = simpledialog.askstring("Input", "Novo ISBN:", initialvalue=book_data[3])
        if new_title and new_author and new_isbn:
            edit_book(book_data[0], new_title, new_author, new_isbn)
            self.view.display_message("Info", "Livro editado com sucesso!")
            self.list_books()

    def add_user(self, name, user_type):
        add_user(name, user_type)
        self.view.display_message("Info", "Usuário adicionado com sucesso!")
        self.list_users()  # Atualiza a lista após adicionar

    def list_users(self):
        users = list_users()
        self.view.update_users_tree(users)

    def remove_user(self):
        selected_item = self.view.users_tree.selection()
        if not selected_item:
            self.view.display_message("Warning", "Selecione um usuário para remover.")
            return
        user_id = self.view.users_tree.item(selected_item)['values'][0]
        remove_user(user_id)
        self.view.display_message("Info", "Usuário removido com sucesso!")
        self.list_users()

    def edit_user(self):
        selected_item = self.view.users_tree.selection()
        if not selected_item:
            self.view.display_message("Warning", "Selecione um usuário para editar.")
            return
        user_data = self.view.users_tree.item(selected_item)['values']
        new_name = simpledialog.askstring("Input", "Novo Nome:", initialvalue=user_data[1])
        new_type = simpledialog.askstring("Input", "Novo Tipo:", initialvalue=user_data[2])
        if new_name and new_type:
            edit_user(user_data[0], new_name, new_type)
            self.view.display_message("Info", "Usuário editado com sucesso!")
            self.list_users()

    def register_loan(self, book_id, user_id, loan_date, due_date):
        register_loan(book_id, user_id, loan_date, due_date)
        self.view.display_message("Info", "Empréstimo registrado com sucesso!")
        self.list_loans()  # Atualiza a lista após registrar

    def list_loans(self):
        loans = list_loans()
        self.view.update_loans_tree(loans)

    def return_loan(self):
        selected_item = self.view.loans_tree.selection()
        if not selected_item:
            self.view.display_message("Warning", "Selecione um empréstimo para devolver.")
            return
        loan_id = self.view.loans_tree.item(selected_item)['values'][0]
        return_date = simpledialog.askstring("Input", "Data de Devolução:")
        if return_date:
            return_loan(loan_id, return_date)
            self.view.display_message("Info", "Empréstimo devolvido com sucesso!")
            self.list_loans()

    def remove_loan(self):
        selected_item = self.view.loans_tree.selection()
        if not selected_item:
            self.view.display_message("Warning", "Selecione um empréstimo para remover.")
            return
        loan_id = self.view.loans_tree.item(selected_item)['values'][0]
        remove_loan(loan_id)
        self.view.display_message("Info", "Empréstimo removido com sucesso!")
        self.list_loans()
