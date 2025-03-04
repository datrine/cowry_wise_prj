# Queues
## Books
- queue_books
- queue_new_books
- queue_updated_books
- queue_deleted_books

## Users
- queue_users
- queue_new_users
- queue_updated_users

## Borrow List
- queue_borrow_list_items
- queue_new_borrow_list_items
- queue_updated_borrow_list_items


# Exchanges
## Users
- topic_users

## Books
- topic_books

## Borrow List
- topic_borrow_list_items


# Routing Keys
## To User Queues
- users.*
- users.new_user
- users.updated_user

## To Book Queues
- books.*
- books.new_book
- books.updated_book
- books.deleted_book

## To Borrow List Queues
- borrow_list_items.*
- borrow_list_items.new_borrow_list_item
- borrow_list_items.updated_borrow_list_item