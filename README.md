# clothing_website

Note: All static files including some javascript files and some images were not be pushed.

(1) Available function:
---

**(A) Suppliers:**

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Upload merchandise
  
  • Manage orders
  
  • Download list of orders
  

**(B) Ordinary users:**

  • Browse merchandise
  
  • Add to cart
  
  • Use Coupon
  
  • Payment
  
  • Receive an invoice (Email)
  
  • Search (very simple type, using module provided by postgreSQL)
  
  • Recommend (very simple type, using item-based CF recommendation)
 

(2) Using tools/frameworks: 
---
  • RabbitMQ - for arranging tasks of mail sending after purchasing some goods by users
  
  • Celery - for making tasks of mail sending work in asynchronous
  
  • Redis - for calculating co-occurrence matrix in recommendation process more efficiently
  
