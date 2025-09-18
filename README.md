# kv_doc_app
## Description
This is a simple document management application built using Kivy and KivyMD.

## Features
- Login and Registration
- Document Management
- Reporting
- Settings

## Installation
1. Clone the repository
2. Install the required dependencies using pip
3. Run the application

## Usage
1. Login to the application using the provided credentials
2. Create a new document
3. View and manage existing documents
4. Reporting
5. Settings

## Contributing
Contributions are welcome!

##exe build success

pyinstaller -c --onedir --add-data "D:\it\project\kv_doc_app\app\assets\images:assets\images" --add-data "D:\it\project\kv_doc_app\app\assets\fonts:assets\fonts" --add-data "D:\it\project\kv_doc_app\app\components:components" --add-data "D:\it\project\kv_doc_app\app\screens:screens" --add-data "D:\it\project\kv_doc_app\app\models:models" --add-data "D:\it\project\kv_doc_app\app\utility:utility" main.py

pyinstaller -w --onefile --add-data "D:\it\project\kv_doc_app\app\assets\images:assets\images" --add-data "D:\it\project\kv_doc_app\app\assets\fonts:assets\fonts" --add-data "D:\it\project\kv_doc_app\app\components:components" --add-data "D:\it\project\kv_doc_app\app\screens:screens" --add-data "D:\it\project\kv_doc_app\app\models:models" --add-data "D:\it\project\kv_doc_app\app\utility:utility" main.py

![image](\\assets\images\doc\demo1.png)
![image](\\assets\images\doc\demo2.png)
![image](\\assets\images\doc\demo3.png)
![image](\\assets\images\doc\demo4.png)
