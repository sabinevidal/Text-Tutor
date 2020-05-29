# Capstone
curl http://127.0.0.1:5000/tutors  
{
  "success": true, 
  "tutors": [
    {
      "classes": [
        {
          "grade": 10, 
          "id": 1, 
          "name": "English"
        }, 
        {
          "grade": 7, 
          "id": 2, 
          "name": "Science"
        }
      ], 
      "email": "name@email.com", 
      "id": 1, 
      "name": "Bob", 
      "phone": "12323445364"
    }, 
    {
      "classes": [
        {
          "grade": 7, 
          "id": 2, 
          "name": "Science"
        }, 
        {
          "grade": 9, 
          "id": 3, 
          "name": "English"
        }
      ], 
      "email": "name1@email.com", 
      "id": 2, 
      "name": "Sally", 
      "phone": "12323445366"
    }, 
    {
      "classes": [
        {
          "grade": 7, 
          "id": 2, 
          "name": "Science"
        }, 
        {
          "grade": 9, 
          "id": 3, 
          "name": "English"
        }
      ], 
      "email": "name2@email.com", 
      "id": 3, 
      "name": "Joe", 
      "phone": "237593456"
    }
  ]
}


curl http://127.0.0.1:5000/api/tutors/create -X POST -H "Content-Type: application/json" -d '{"name": "Lizzo", "phone": "1231234123", "email": "lizzo@email.com" }'



curl http://127.0.0.1:5000/subjects/create -X POST -H "Content-Type: application/json" -d '{"name": "English", "grade": "8"}'