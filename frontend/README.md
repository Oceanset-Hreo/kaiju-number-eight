# How to use .env

1. run and get the .env file
```bash
make init_env
```

2. In vue file use import.meta.env.VITE_xxx to access the environment variable

```javascript
console.log(import.meta.env.VITE_API_URL)
```
