from fastapi import APIRouter

router = APIRouter()


@router.get('/api/ping')
async def ping():
    return {'message': 'OK'}
