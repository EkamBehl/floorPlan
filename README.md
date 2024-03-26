<h1> Steps to Run. </h1>
<h2>1. Create and run a python virtual environment </h2>
<p>
  To create and activate a Python virtual environment in Windows, you can use the following steps:
<ul>
<h4>1.1 Open Command Prompt:</h4>

<ul>
  <li>Press Windows + R to open the "Run" dialog.</li>
  <li>Type cmd and press Enter.</li>
</ul>

<h4>1.2 Navigate to your project directory:</h4>

<ul> 
  <li> Use the cd command to navigate to the directory where you want to create your virtual environment.</li>
</ul> 


<h4>1.3 Create a virtual environment: </h4>

<ul><li>Run the following command to create a virtual environment named venv (you can replace the last venv with any name you prefer): 

```
python -m venv venv

```
</li>
</ul>
<h4>1.4 Ensure that you don't clone the files in the venv folder!! </h4>
<ul>
  
<li> Instead have a folder structure like this 

```
my_project/
│
├── venv/                   # Virtual environment directory
│
├── api/                    # Source code directory
│   └── main.py
|   └── detectionModel.py
│
└── requirements.txt  


```
</li>
</ul>
<h4>1.5 Run the Enivronment: </h4>
<ul> <li> Go into my_project(or whatever the folder is called ) and  Run the python environment by using the following: </li>


```
#Replace venv with your virtual environment folder name
source venv/bin/activate

```
</li>
</ul>
</ul>
</p>



<h2>2. Install Dependencies:</h2>
Following are the Dependencies required for the project.
<ul>
<h4>1. Fast Api</h4>
<ul><li>
  <p>FastAPI is a modern web framework for building APIs with Python. Install it using pip:</p>

```
pip install fastapi

```
</li>
</ul>
<h4>2. Uvicorn</h4>
<ul><li>
<p>Uvicorn is a lightning-fast ASGI server. Install it using pip:</p>

```
pip install uvicorn

```
</li>
</ul>

<h4>3. Python Multipart</h4>
<ul><li>
<p>python-multipart is a streaming multipart parser for Python. Install it using pip:</p>

```
pip install python-multipart

```
</li>
</ul>
<h4>Install Ultralytics</h4>
<ul><li>
<p>Ultralytics is a package for object detection, instance segmentation, and pose estimation. Install it using pip:</p>

```
pip install ultralytics

```
</li>
</ul>
</ul>

<h2>3. Run the uvicorn server </h2>
Navigate to the directory containing your main.py file and run the following command in the terminal:

```
uvicorn main:app --reload
```
<ul>
  <li>main: the file name (without the .py extension) where your app is defined.</li>
  <li>app: the variable name assigned to the FastAPI() instance.</li>
  <li>--reload: makes the server restart after code changes. This is very useful during development but should be omitted in production.</li>
  
</ul>
