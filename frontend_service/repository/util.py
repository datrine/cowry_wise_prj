from datetime import datetime
def validate_user_filters(filters:dict):
    if  filters is None:
        return True
    if not isinstance(filters,dict) and filters is not None:
        raise Exception("Invalid filters")
    for filter in filters:
        if filter not in ["email","lastname","firstname"]:
            raise Exception(f"Invalid filter {filter}")
    return True

def validate_user_updatable_fields(filters:dict):
    if not isinstance(filters,dict):
        raise Exception("Invalid update fields")
    if  len(filters) == 0:
        raise Exception("At least a field must be updated")
    for filter in filters:
        if filter not in ["email","lastname","firstname"]:
            raise Exception(f"Invalid filter {filter}")
    return True

def validate_book_filters(filters:dict):
    if not isinstance(filters,dict) and filters is not None:
        raise Exception("Invalid filters")
    if  filters is None:
        return True
    for filter in filters:
        if filter not in ["title","category","publisher"]:
            raise Exception(f"Invalid filter {filter}")
    return True

def validate_book_updatable_fields(filters:dict):
    if not isinstance(filters,dict):
        raise Exception("Invalid update fields")
    if  len(filters) == 0:
        raise Exception("At least a field must be updated")
    for filter in filters:
        if filter not in ["title","category","publisher"]:
            raise Exception(f"Invalid filter {filter}")
    return True


def format_user_row(row):
    return {
            "id": row["rowid"],
            "email": row["email"],
            "firstname": row["firstname"],
            "lastname": row["lastname"],
            "role": row["role"],
            }



def format_book_row(row):
    return {
                "id": row["rowid"],
                "title":row["title"],
                "publisher": row["publisher"],
                "category": row["category"],
                "is_available":row["is_available"],
            }


def format_user_book_load_row(row):
    return {
                "id": row["rowid"],
                "book_id":row["book_id"],
                "user_id": row["user_id"],
                "book_id": row["book_id"],
                "user_id":row["user_id"],
                "email":row["email"],
                "firstname":row["firstname"],
                "lastname":row["lastname"],
                "title":row["title"],
                "category":row["category"],
                "publisher":row["publisher"],
                "loan_date": row["loan_date_dt"],
                "return_date":   row["return_date_dt"],
            }