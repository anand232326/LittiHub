from math import ceil


def calculate_pagination(page: int,page_size: int,total: int,) -> dict:
    total_pages = ceil(total / page_size)
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }