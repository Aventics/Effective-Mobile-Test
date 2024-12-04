import json
from datetime import date

# Создаем класс книги
class Book:
        def __init__(self, book_id, title, author, year, status='в наличии'):
            self.book_id = book_id
            self.title = title
            self.author = author
            self.year = year
            self.status = status

        # Отображение экзкмпляра книги
        def __repr__(self):
            return f"{self.book_id}: {self.title} - {self.author} ({self.year}) - {self.status}"


# Функции для загрузки данных из JSON файла:
def load_books(filename='books.json'):
    # Если файл существует получаем список книг, если нет, возвращаем пустой список
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [Book(**book) for book in json.load(f)]
    except FileNotFoundError:
        return []

# Сохраняем книгу в JSON файл
def save_books(books, filename='books.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        # Сохраняем книгу из класса в JSON используя ensure_ascii=False для сохранения в удобочитаемом формате
        # и с отступом в 4 пробела (indent=4).
        json.dump([book.__dict__ for book in books], f, ensure_ascii=False, indent=4)


# Добавление новой книги в библиотеку
def add_book(books, title, author, year):
    # Для нескольких файлов проще всего было бы сделать так:
    # book_id = len(books) + 1 
    # Но в случае удаления книги из середины библиотеки новая книга допишется с уже существующим ID
    book_id = id(title) 
    new_book = Book(book_id, title, author, year)
    books.append(new_book)
    save_books(books)


# Удаление книги
def remove_book(books, book_id):
    for book in books:
        # Если искомый id существует - книга удаляется
        if book.book_id == book_id:
            books.remove(book)
            save_books(books)
            return
    print('Книга не найдена.')



# Поиск
def search_books(books, query):
    # Если в списке есть книга удовлетворяющая запрос пользователя, то она добавляется в список найденых книг
    results = [book for book in books if query.lower() in book.title.lower() or 
            query.lower() in book.author.lower() or 
            str(book.year) == query]
    return results
       


# Показать все книги
def display_books(books):
    if not books:
        print('Библиотека пуста.')
    for book in books:
        print(book)


# Изменение статуса книги
def change_status(books, book_id, status):
    for book in books:
        if book.book_id == book_id:
            book.status = status
            save_books(books)
            return
    print('Книга не найдена.')




# Взаимодействие с пользователем
def main():
    # Получаем список сохраненных книг
    books = load_books()
    # Меню
    while True:
        print('\n1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Поиск книги')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('0. Выйти\n')
        choice = input('Выберите действие: ')
        
        if choice == '1':           
            title = input('Введите название книги: ')
            author = input('Введите автора книги: ')
            try:
                year = int(input('Введите год издания: '))                
            except(ValueError):
                print('Неверный ввод.')
            else:
                today = date.today()
                if 0 < year <= int(today.strftime('%Y')):
                    add_book(books, title, author, year)
                else:
                    print('Дата указана неверно.')
            
        elif choice == '2':
            book_id = int(input('Введите ID книги для удаления: '))
            remove_book(books, book_id)

        elif choice == '3':
            query = input('Введите название, автора или год издания книги для поиска: ')
            results = search_books(books, query)
            if results:
                for book in results:
                    print(book) 
            else:
                print('\nКнига не найдена.')

        elif choice == '4':
            display_books(books)

        elif choice == '5':
            try:
                book_id = int(input('Введите ID книги: '))
            except(ValueError):
                print('Неверный ввод.')
            else:    
                new_status = input('Введите новый статус (1 - в наличии; 2 - выдана): ')
                if new_status == '1':
                    status = 'в наличии'
                    change_status(books, book_id, status)
                elif new_status == '2':
                    status = 'выдана'
                    change_status(books, book_id, status)
                else:
                    print('Неверный ввод.')
                

        elif choice == '0':
            print('\nДо свидания')
            break
        
        else:
            print('\nНеверный выбор, попробуйте снова.')


if __name__ == '__main__':
    main()





