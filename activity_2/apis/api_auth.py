from fastapi import APIRouter


router = APIRouter(
    prefix = '/auth',
    tags = ['API Auth']
)

@router.post('/login')
def root():
    return { 'login': 'login' }

@router.post('/reset')
def test():
    return { 'reset': 'reset' }