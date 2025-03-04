from app.repository.util import validate_book_filters,validate_book_updatable_fields,validate_user_filters,validate_user_updatable_fields

from faker import Faker
fake = Faker()
def test_validate_user_filters():
    res= validate_user_filters({"email": fake.email(),"lastname": fake.email(),"firstname": fake.email()})
    assert res == True
 
def test_validate_user_filters_no_fields():
    res= validate_user_filters(None)
    assert res == True

def test_validate_user_filters_non_dict_raise():
    try:
        validate_user_filters(tuple(fake.email(),))
    except Exception as e:
        assert isinstance(e,AssertionError) == True
      
def test_validate_user_filters_non_field():
    try:
        validate_user_filters({"field": "non_field_value"})
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e,AssertionError) == True

def test_validate_user_updatable_fields():
    res= validate_user_updatable_fields({"email": fake.email(), "lastname": fake.email(), "firstname": fake.email()})
    assert res == True

def test_validate_user_updatable_fields_no_fields_raise():
    try:
        validate_user_updatable_fields(None)
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True
        
def test_validate_user_updatable_fields_empty_dict_raise():
    try:
        validate_user_updatable_fields(filters=dict())
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True
        
def test_validate_user_updatable_fields_invalid_field_raise():
    try:
        validate_user_updatable_fields(filters=dict(invalid_field="invalid_field_value"))
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True

def test_validate_book_filters():
    res= validate_book_filters({"title": fake.email(), "publisher": fake.email()})
    assert res == True  

def test_validate_book_filters_no_filters():
    res= validate_book_filters(None)
    assert res == True

def test_validate_book_filters_non_dict_filter_raise():
    try:
        validate_book_filters(filters=tuple(fake.email(), ))
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True
    
def test_validate_book_filters_invalid_field_raise():
    try:
        validate_book_filters(filters=dict(invalid_field="invalid_field_value"))
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True

def test_validate_book_updatable_fields():
    res= validate_book_updatable_fields({"title": fake.email(), "publisher": fake.email()})
    assert res == True

def test_validate_book_updatable_fields_no_fields_raise():
    try:
        validate_book_updatable_fields(filters=dict())
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True


        
def test_validate_book_updatable_fields_invalid_field_raise():
    try:
        validate_book_updatable_fields(filters=dict(invalid_field="invalid_field_value"))
        assert False, "should raise exception"
    except Exception as e:
        assert isinstance(e, AssertionError) == True