# BookListResponse

Response danh sách sách

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[Book]**](Book.md) |  | 
**total** | **int** |  | 
**skip** | **int** |  | 
**limit** | **int** |  | 

## Example

```python
from openapi_client.models.book_list_response import BookListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BookListResponse from a JSON string
book_list_response_instance = BookListResponse.from_json(json)
# print the JSON string representation of the object
print(BookListResponse.to_json())

# convert the object into a dict
book_list_response_dict = book_list_response_instance.to_dict()
# create an instance of BookListResponse from a dict
book_list_response_from_dict = BookListResponse.from_dict(book_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


