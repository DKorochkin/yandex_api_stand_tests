import sender_stand_request
import data

# Функция для изменения параметра firstName
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Функция для позитивной проверки
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

#Функция для негативной проверки
def negative_assert(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

# Функция для проверки передачи invalid firstName
def negative_assert_no_first_name(user_boby):
    user_body = get_user_body(user_boby)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 1
# Параметр firstName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2
# Параметр firstName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


# Тест 3
# Параметр firstName включает в себя 1 символ
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert("A")

# Тест 4
# Параметр firstName включает в себя 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert("Aaaaaaaaaaaaaaaa")

# Тест 5
# Параметр firstName включает в себя английские символы
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("NN")

# Тест 6
# Параметр firstName включает в себя русские символы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Апр")

# Тест 7
# Параметр firstName включает в себя пробел
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert("Апр е")

# Тест 8
# Параметр firstName включает в себя спец символы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert("Апр%")

# Тест 9
# Параметр firstName включает в себя цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert("Апр001")

# Тест 10
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)

# Тест 11
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)

# Тест 12
# Тип параметра firstName число
def test_create_user_number_type_first_name_get_error_response():
        user_body = get_user_body(12)
        response = sender_stand_request.post_new_user(user_body)
        assert response.status_code == 400

