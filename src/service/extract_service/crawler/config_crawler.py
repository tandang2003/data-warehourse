import json

config_crawler_source_A_1 = json.loads(""" 
{
  "src": { "method": "url"},
  "subject": {
    "method": "text",
    "quantity": 1,
    "selector": "//*[contains(@class, 'pr-title')]"
  },
  "area": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-short-info-item')]/*[text()='Diện tích']/following-sibling::*[1]"
  },
  "address": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-address')]"
  },
  "price": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-short-info-item')]/*[text()='Mức giá']/following-sibling::*[1]"
  },
  "description": {                                   
    "method"  : "description",                                       
    "selector": "//*[contains(@class, 're__detail-content')]"
  },
  "image": {
    "quantity" : null,                                     
    "method"   : "get_attribute",                           
    "attribute": "src",                                     
    "selector" : "//*[contains(@class, 'slick-track')]//img"
  },
  "natural_id": {
    "quantity": 1,
    "attribute": "prid",
    "method": "get_attribute",
    "selector": "//*[@id='product-detail-web']"
  },
  "orientation": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Hướng nhà']/following-sibling::*[1]"
  },
  "bedroom": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Số phòng ngủ']/following-sibling::*[1]"
  },
  "bathroom": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Số toilet']/following-sibling::*[1]"
  },
  "legal": {
    "quantity": 1,
    "method": "text",
    "selector": "//*[contains(@class, 're__pr-specs-content-item')]/*[text()='Pháp lý']/following-sibling::*[1]"
  },
  "email": {
    "quantity": 1,
    "method": "get_attribute",
    "selector": "//*[@id='email']",
    "attribute": "data-email"
  },
  "full_name": {
    "quantity": 1,
    "attribute": "title",
    "method": "get_attribute",
    "selector": "//*[contains(@class, 'js_contact-name')][1]"
  },
  "avatar": {                                                 
    "method"  : "text",                                                       
    "selector": "//*[contains(@class, 'js__agent-contact-avatar')]//img/@src"
  },
  "start_date": {
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-config-item')]/*[text()='Ngày đăng']/following-sibling::*[1]"
  },
  "end_date": {
    "method": "text",
    "selector": "//*[contains(@class, 'js__pr-config-item')]/*[text()='Ngày hết hạn']/following-sibling::*[1]"
  },
  "create_at": {
    "method": "time"
  }
}
""")

