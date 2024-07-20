from fastapi import APIRouter

router = APIRouter(prefix=("/products"), 
                   tags=["products"],
                   responses={404 : {"message": "No encontrado"}})

products_list = ["products 1","products 2", "products 3", "products 4", "products 5" ]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]
