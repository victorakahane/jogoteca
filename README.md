
# 🎮 Game Catalog CRUD
This project is a simple CRUD (Create, Read, Update, Delete) application built with Flask, allowing users to manage a catalog of games. Users can add new games, view details about existing games, edit their information, and delete them from the catalog.

## ⚒️ Adjustments and improvements
The Game Catalog CRUD is still under development and the next updates will focus on the following tasks:
- [ ] Register new users.
- [ ] User authentication for editing and deleting games.

## 🕹️ Features
-  **Create**: Add a new game to the catalog with details like name, category, console and game cover.
-  **Read**: View the list of games in the catalog.
-  **Update**: Edit the information of an existing game, including uploading a custom image for the game cover.
-  **Delete**: Remove a game from the catalog.

### 💻 Prerequisites
- Python 3.10+ installed
- pip (Python package installer) installed
- MySql 9.1.0

##  ⌨️ Tech Stack

-  **Backend**: Flask (Python)
-  **Database**: MySQL
-  **Frontend**: HTML, CSS, Javascript, Bootstrap
-  **Libraries/Packages**:
- Flask-WTF for form handling
- SQLAlchemy for ORM (Object Relational Mapping)
- Flask-Bcrypt for user password encryption

## 🚀 Installation
1. Clone the repository:
```bash
git clone https://github.com/victorakahane/jogoteca
```
2. Navigate into the project folder:
```bash
cd jogoteca
```
3. Create and activate a virtual environment:

On windows:
```bash
python -m venv .venv 
.\.venv\Scripts\activate
```

On Linux/MacOS:
```bash
python3 -m venv .venv source .venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Start MySql
6. Set .env file:
```txt
HOST=localhost
USER=YOUR_MYSQL_USER
PASSWORD=YOUR_MYSQL_PASSWORD
SGBD=mysql+mysqlconnector
DATABASE=jogoteca
SECRET_KEY=YOUR_SECRET_KEY_HERE
 ```
7. Run prepara_banco.py:
```py
python prepara_banco.py
```
8. Run server: 
```py
python main.py
```

## ☕ Usage

-   Navigate to the home page to see the list of games.
-   You can add a new game using the "Add Game" form.
-   Edit or delete games by clicking on the corresponding buttons next to each game entry.

## 📫 Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -am 'Add new feature'`).
4.  Push to your branch (`git push origin feature/your-feature-name`).
5.  Open a pull request on homolog branch.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
