# MoMo SMS REST API Documentation

## Authentication

All endpoints are protected using Basic Authentication.

### Credentials

Username: admin

Password: momo123

### Example

```bash
curl -u admin:momo123 http://localhost:8000/transactions
```

---

## GET /transactions

Returns all SMS transactions.

### Response

```json
[
  {
    "id": 1,
    "type": "Incoming Money",
    "amount": 5000,
    "sender": "Alice",
    "receiver": "Bob"
  }
]
```

### Error Codes

| Code | Meaning      |
| ---- | ------------ |
| 401  | Unauthorized |

---

## GET /transactions/{id}

Returns a single transaction.

### Error Codes

| Code | Meaning               |
| ---- | --------------------- |
| 401  | Unauthorized          |
| 404  | Transaction Not Found |

---

## POST /transactions

Creates a new transaction.

### Request Example

```json
{
  "id": 21,
  "type": "Transfer",
  "amount": 10000,
  "sender": "John",
  "receiver": "Jane"
}
```

### Error Codes

| Code | Meaning      |
| ---- | ------------ |
| 400  | Bad Request  |
| 401  | Unauthorized |

---

## PUT /transactions/{id}

Updates an existing transaction.

### Error Codes

| Code | Meaning               |
| ---- | --------------------- |
| 401  | Unauthorized          |
| 404  | Transaction Not Found |

---

## DELETE /transactions/{id}

Deletes a transaction.

### Error Codes

| Code | Meaning               |
| ---- | --------------------- |
| 401  | Unauthorized          |
| 404  | Transaction Not Found |

```
```

