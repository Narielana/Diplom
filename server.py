import uvicorn

if __name__ == 'main':
    uvicorn.run(
        'src.main:app',
        host='127.0.0.1',
        port=8080,
        reload=True,
    )
