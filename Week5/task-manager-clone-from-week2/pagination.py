def offset_pagination(data, offset=0, limit=5):
    total = len(data)

    result = data[offset: offset + limit]

    return {
        "offset": offset,
        "limit": limit,
        "total": total,
        "data": result
    }

def page_pagination(data, page=1, size=5):

    start = (page - 1) * size
    end = start + size

    total = len(data)

    return {
        "page": page,
        "size": size,
        "total": total,
        "data": data[start:end]
    }

def cursor_pagination(data, cursor=None, limit=5):

    start_index = 0

    if cursor:
        for i, item in enumerate(data):
            if item["id"] == cursor:
                start_index = i + 1
                break

    result = data[start_index:start_index + limit]

    next_cursor = None
    if result:
        next_cursor = result[-1]["id"]

    return {
        "cursor": cursor,
        "next_cursor": next_cursor,
        "limit": limit,
        "data": result
    }