# cURL Requests for FastAPI Routes

This document provides `curl` commands for each of the available routes in the FastAPI application.

## Main Routes

### Root

```bash
curl -X GET "http://localhost:33001/"
```

### Health Check

```bash
curl -X GET "http://localhost:33001/healthz"
```

## v1 Models (Demo)

### Demo Chat

```bash
curl -X GET "http://localhost:33001/video-1/?question=What+is+FastAPI"
```

## v2 Embeddings (Embeddings Demo)

### Convert to Embeddings

```bash
curl -X POST "http://localhost:33001/video-2/convert-to-embeddings" \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a test sentence."}'
```

### Get Embeddings from Documents

```bash
curl -X POST "http://localhost:33001/video-2/from-documents" \
     -H "Content-Type: application/json" \
     -d '{"documents": ["This is the first document.", "This is the second document."]}'
```

### Embeddings Search

```bash
curl -X POST "http://localhost:33001/video-2/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "your search query", "documents": ["doc1", "doc2"]}'
```

## v3 Prompts (Prompts Demo)

### Summarize

```bash
curl -X POST "http://localhost:33001/video-3/summarize" \
     -H "Content-Type: application/json" \
     -d '{"content": "This is a long text to summarize.", "responseLength": "short", "responseFormat": "plain_text"}'
```

## Users

### Get All Users

```bash
curl -X GET "http://localhost:33001/users/"
```

### Get User by ID

```bash
curl -X GET "http://localhost:33001/users/1"
```

### Create User

```bash
curl -X POST "http://localhost:33001/users/" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "username": "newuser", "full_name": "New User"}'
```

### Update User

```bash
curl -X PUT "http://localhost:33001/users/1" \
     -H "Content-Type: application/json" \
     -d '{"email": "updated@example.com"}'
```

### Delete User

```bash
curl -X DELETE "http://localhost:33001/users/1"
```
