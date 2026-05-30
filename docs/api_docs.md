# MoMo SMS Transactions API Documentation

## Base URL
http://localhost:8000

---

# 🔐 Authentication

All endpoints require Basic Authentication.

- Username: admin  
- Password: password  

---

# 📌 1. GET /transactions

### Request
```bash
curl -u admin:password http://localhost:8000/transactions
[
  {
    "id": "1",
    "sender": "A",
    "receiver": "B",
    "amount": "2000"
  },
  {
    "id": "2",
    "sender": "C",
    "receiver": "D",
    "amount": "1500"
  }
]curl -u admin:password http://localhost:8000/transactions/1
{
  "id": "1",
  "sender": "A",
  "receiver": "B",
  "amount": "2000",
  "date": "1715351458724",
  "type": "1"
}
curl -u admin:password -X POST http://localhost:8000/transactions \
-H "Content-Type: application/json" \
-d '{
  "id":"10",
  "sender":"X",
  "receiver":"Y",
  "amount":"500",
  "date":"1715351459999",
  "type":"1"
}'
{
  "message": "Created",
  "data": {
    "id": "10",
    "sender": "X",
    "receiver": "Y",
    "amount": "500",
    "date": "1715351459999",
    "type": "1"
  }
}{
  "message": "Updated",
  "data": {
    "id": "10",
    "sender": "X",
    "receiver": "Y",
    "amount": "1000",
    "date": "1715351459999",
    "type": "1"
  }
}
curl -u admin:password -X DELETE http://localhost:8000/transactions/10
{
  "message": "Deleted",
  "id": "10"
}
