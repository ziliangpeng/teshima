docker run --name redis -p 6379:6379 -d redis redis-server --appendonly no --save "" --maxmemory 2gb --maxmemory-policy allkeys-lru
