Note: All static files including some javascript files and some images were not be pushed.

(1) Available functions
---

**(A) Suppliers:**

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Upload merchandise
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Manage orders
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Download list of orders
  

**(B) Ordinary users:**

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Browse merchandise
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Add to cart
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Use Coupon
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Payment
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Receive an invoice (Email)
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Search (very simple type, using module provided by postgreSQL)
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Recommend (very simple type, using item-based CF recommendation)
 

(2) Using tools/frameworks
---
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• RabbitMQ - for arranging tasks of mail sending after purchasing some goods by users
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Celery - for making tasks of mail sending work in asynchronous
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Redis - for calculating co-occurrence matrix in recommendation process more efficiently
  
