import sqlite3

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect('library.db', timeout=10)
            cls._instance.connection.execute('PRAGMA foreign_keys = ON')  # Ativa as restrições de chave estrangeira
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
        Database._instance = None  # Reseta a instância quando a conexão for fechada

    @staticmethod
    def create_tables():
        cursor = Database().cursor
        
        # Tabela para livros
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Tabela para usuários
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_type TEXT CHECK(user_type IN ('admin', 'librarian', 'member')) NOT NULL
            )
        ''')
        
        # Tabela para empréstimos
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        Database().commit()

# Funções para livros
def add_book(title, author, isbn):
    db = Database()
    cursor = db.cursor
    try:
        cursor.execute(''' 
            INSERT INTO books (title, author, isbn)
            VALUES (?, ?, ?)
        ''', (title, author, isbn))
        db.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: Livro com o ISBN {isbn} já existe.")

def edit_book(book_id, new_title=None, new_author=None, new_isbn=None):
    db = Database()
    cursor = db.cursor
    
    updates = []
    params = []
    
    if new_title:
        updates.append("title = ?")
        params.append(new_title)
    
    if new_author:
        updates.append("author = ?")
        params.append(new_author)
    
    if new_isbn:
        updates.append("isbn = ?")
        params.append(new_isbn)
    
    if updates:
        params.append(book_id)  # Adiciona o ID do livro no final
        cursor.execute(f'''
            UPDATE books
            SET {', '.join(updates)}
            WHERE id = ?
        ''', params)
    
    db.commit()

def remove_book(isbn):
    db = Database()
    cursor = db.cursor
    cursor.execute(''' 
        DELETE FROM books
        WHERE isbn = ?
    ''', (isbn,))
    db.commit()

def search_books(title=None, author=None, isbn=None):
    db = Database()
    cursor = db.cursor
    query = 'SELECT * FROM books WHERE 1=1'
    params = []
    if title:
        query += ' AND title LIKE ?'
        params.append(f'%{title}%')
    if author:
        query += ' AND author LIKE ?'
        params.append(f'%{author}%')
    if isbn:
        query += ' AND isbn = ?'
        params.append(isbn)
    cursor.execute(query, params)
    books = cursor.fetchall()
    return [{'id': row[0], 'title': row[1], 'author': row[2], 'isbn': row[3]} for row in books]

def list_books():
    db = Database()
    cursor = db.cursor
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return [{'id': row[0], 'title': row[1], 'author': row[2], 'isbn': row[3]} for row in books]

# Funções para usuários
def add_user(name, user_type):
    db = Database()
    cursor = db.cursor
    valid_types = ['admin', 'librarian', 'member']
    
    if user_type not in valid_types:
        print(f"Erro: Tipo de usuário '{user_type}' inválido. Deve ser um dos: {valid_types}.")
        return
    
    try:
        cursor.execute(''' 
            INSERT INTO users (name, user_type)
            VALUES (?, ?)
        ''', (name, user_type))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro: {e}")

def edit_user(user_id, new_name=None, new_user_type=None):
    db = Database()
    cursor = db.cursor
    
    updates = []
    params = []
    
    if new_name:
        updates.append("name = ?")
        params.append(new_name)
    
    if new_user_type:
        valid_types = ['admin', 'librarian', 'member']
        if new_user_type not in valid_types:
            print(f"Erro: Tipo de usuário '{new_user_type}' inválido. Deve ser um dos: {valid_types}.")
            return
        updates.append("user_type = ?")
        params.append(new_user_type)
    
    if updates:
        params.append(user_id)  # Adiciona o ID do usuário no final
        cursor.execute(f'''
            UPDATE users
            SET {', '.join(updates)}
            WHERE id = ?
        ''', params)
    
    db.commit()

def remove_user(user_id):
    db = Database()
    cursor = db.cursor
    cursor.execute(''' 
        DELETE FROM users
        WHERE id = ?
    ''', (user_id,))
    db.commit()

def list_users():
    db = Database()
    cursor = db.cursor
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return [{'id': row[0], 'name': row[1], 'user_type': row[2]} for row in users]

# Funções para empréstimos
def register_loan(book_id, user_id, loan_date, due_date):
    db = Database()
    cursor = db.cursor
    cursor.execute(''' 
        INSERT INTO loans (book_id, user_id, loan_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (book_id, user_id, loan_date, due_date))
    db.commit()

def return_loan(loan_id, return_date):
    db = Database()
    cursor = db.cursor
    cursor.execute(''' 
        UPDATE loans
        SET return_date = ?
        WHERE id = ?
    ''', (return_date, loan_id))
    db.commit()

def remove_loan(loan_id):
    db = Database()
    cursor = db.cursor
    cursor.execute(''' 
        DELETE FROM loans
        WHERE id = ?
    ''', (loan_id,))
    db.commit()

def list_loans(status=None):
    db = Database()
    cursor = db.cursor
    query = 'SELECT * FROM loans WHERE 1=1'
    if status == 'active':
        query += ' AND return_date IS NULL'
    elif status == 'returned':
        query += ' AND return_date IS NOT NULL'
    cursor.execute(query)
    loans = cursor.fetchall()
    return [{'id': row[0], 'book_id': row[1], 'user_id': row[2], 'loan_date': row[3], 'due_date': row[4], 'return_date': row[5]} for row in loans]

# Criar as tabelas ao iniciar o módulo
if __name__ == "__main__":
    Database.create_tables()
