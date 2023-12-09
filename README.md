# Fairseed

## Project Setup

Follow these steps to set up the Fairseed project:

### 1. Clone the Repository

Clone the repository from GitHub using the following command:

```bash
git clone https://github.com/azroddin123/Fairseed.git
```

### 2. Create a Virtual Environment
Navigate to the project directory and create a virtual environment:

```bash
cd Fairseed
python3 -m venv venv
```

#### Activate the virtual environment:

###### On Windows:
```bash
Copy code
venv\Scripts\activate
```
##### On Unix or MacOS:
``` bash
Copy code
source venv/bin/activate
```

### 2. Install Dependencies
Install the required dependencies from the requirements.txt file on a virtual environment:

```bash
pip install -r requirements.txt
```

### 3. Database Migrations
Navigate to the project directory and run database migrations:

```bash
cd Fairseed
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Project
Run the project using the following command:

```bash
python manage.py runserver
```











    


    

