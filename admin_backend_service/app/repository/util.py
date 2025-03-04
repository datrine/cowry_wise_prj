def validate_user_filters(filters:dict):
    if  filters is None:
        return True
    if not isinstance(filters,dict) and filters is not None:
        raise AssertionError("Invalid filters")
    for filter in filters:
        if filter not in ["email","lastname","firstname"]:
            raise AssertionError(f"Invalid filter {filter}")
    return True

def validate_user_updatable_fields(filters:dict):
    if not isinstance(filters,dict):
        raise AssertionError("Invalid update fields")
    if  len(filters) == 0:
        raise AssertionError("At least a field must be updated")
    for filter in filters:
        if filter not in ["email","lastname","firstname"]:
            raise AssertionError(f"Invalid filter {filter}")
    return True

def validate_book_filters(filters:dict):
    if not isinstance(filters,dict) and filters is not None:
        raise AssertionError("Invalid filters")
    if  filters is None:
        return True
    for filter in filters:
        if filter not in ["title","category","publisher","is_available","return_date","loan_date"]:
            raise AssertionError(f"Invalid filter {filter}")
    return True

def validate_book_updatable_fields(filters:dict):
    print(filters)
    if not isinstance(filters,dict):
        raise Exception("Invalid update fields")
    if  len(filters) == 0:
        raise Exception("At least a field must be updated")
    for filter in filters:
        if filter not in ["title","category","publisher","is_available","return_date","loan_date"]:
            raise Exception(f"Invalid filter {filter}")
    print(filters)
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
                "is_available": True if row["is_available"] > 0 else False,
                "loan_date": row["loan_date_dt"],
                "return_date": row["return_date_dt"],
            }


def format_user_book_load_row(row):
    return {
                "id": row["rowid"],
                "book_id":row["book_id"],
                "user_id": row["user_id"],
                "lastname":row["lastname"],
                "firstname":row["firstname"],
                "title":row["title"],
                "category":row["category"],
                "publisher":row["publisher"],
                "loan_date": row["loan_date_dt"],
                "return_date": row["return_date_dt"],
            }