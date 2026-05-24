from fastapi import APIRouter


router = APIRouter(
    prefix = '/api',
    tags = ['API Default']
)

@router.get('/')
def root():
    return { 'root': 'root' }

@router.get('/test')
def test():
    return { 'test': 'test' }