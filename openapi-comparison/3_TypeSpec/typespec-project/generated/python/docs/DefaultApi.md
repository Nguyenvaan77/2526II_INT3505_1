# openapi_client.DefaultApi

All URIs are relative to *http://localhost:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**books_api_create_book**](DefaultApi.md#books_api_create_book) | **POST** /books | 
[**books_api_delete_book**](DefaultApi.md#books_api_delete_book) | **DELETE** /books/{id} | 
[**books_api_get_all_books**](DefaultApi.md#books_api_get_all_books) | **GET** /books | 
[**books_api_get_book**](DefaultApi.md#books_api_get_book) | **GET** /books/{id} | 
[**books_api_update_book**](DefaultApi.md#books_api_update_book) | **PUT** /books/{id} | 


# **books_api_create_book**
> BookResponse books_api_create_book(create_book_request)

Tạo sách mới

### Example


```python
import openapi_client
from openapi_client.models.book_response import BookResponse
from openapi_client.models.create_book_request import CreateBookRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_book_request = openapi_client.CreateBookRequest() # CreateBookRequest | 

    try:
        api_response = api_instance.books_api_create_book(create_book_request)
        print("The response of DefaultApi->books_api_create_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_api_create_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_book_request** | [**CreateBookRequest**](CreateBookRequest.md)|  | 

### Return type

[**BookResponse**](BookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The request has succeeded and a new resource has been created as a result. |  -  |
**400** | The server could not understand the request due to invalid syntax. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_api_delete_book**
> DeleteResponse books_api_delete_book(id)

Xóa sách

### Example


```python
import openapi_client
from openapi_client.models.delete_response import DeleteResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.books_api_delete_book(id)
        print("The response of DefaultApi->books_api_delete_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_api_delete_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**DeleteResponse**](DeleteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The request has succeeded. |  -  |
**404** | The server cannot find the requested resource. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_api_get_all_books**
> BookListResponse books_api_get_all_books(books_api_get_all_books_request, skip=skip, limit=limit, sort_by=sort_by)

Lấy danh sách sách

### Example


```python
import openapi_client
from openapi_client.models.book_list_response import BookListResponse
from openapi_client.models.books_api_get_all_books_request import BooksAPIGetAllBooksRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    books_api_get_all_books_request = openapi_client.BooksAPIGetAllBooksRequest() # BooksAPIGetAllBooksRequest | 
    skip = 0 # int |  (optional) (default to 0)
    limit = 10 # int |  (optional) (default to 10)
    sort_by = created_at # str |  (optional) (default to created_at)

    try:
        api_response = api_instance.books_api_get_all_books(books_api_get_all_books_request, skip=skip, limit=limit, sort_by=sort_by)
        print("The response of DefaultApi->books_api_get_all_books:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_api_get_all_books: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **books_api_get_all_books_request** | [**BooksAPIGetAllBooksRequest**](BooksAPIGetAllBooksRequest.md)|  | 
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 10]
 **sort_by** | **str**|  | [optional] [default to created_at]

### Return type

[**BookListResponse**](BookListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The request has succeeded. |  -  |
**500** | Server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_api_get_book**
> BookResponse books_api_get_book(id)

Lấy thông tin sách theo ID

### Example


```python
import openapi_client
from openapi_client.models.book_response import BookResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    id = 'id_example' # str | 

    try:
        api_response = api_instance.books_api_get_book(id)
        print("The response of DefaultApi->books_api_get_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_api_get_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**BookResponse**](BookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The request has succeeded. |  -  |
**404** | The server cannot find the requested resource. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_api_update_book**
> BookResponse books_api_update_book(id, update_book_request)

Cập nhật sách

### Example


```python
import openapi_client
from openapi_client.models.book_response import BookResponse
from openapi_client.models.update_book_request import UpdateBookRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:5000
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    id = 'id_example' # str | 
    update_book_request = openapi_client.UpdateBookRequest() # UpdateBookRequest | 

    try:
        api_response = api_instance.books_api_update_book(id, update_book_request)
        print("The response of DefaultApi->books_api_update_book:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->books_api_update_book: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **update_book_request** | [**UpdateBookRequest**](UpdateBookRequest.md)|  | 

### Return type

[**BookResponse**](BookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The request has succeeded. |  -  |
**404** | The server cannot find the requested resource. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

