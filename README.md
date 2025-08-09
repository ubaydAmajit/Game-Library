# Game Library Web Application

A comprehensive Flask-based web application for managing and exploring a game library. This application allows users to browse, search, review, and manage their personal game collections with features like wishlists, user profiles, and game reviews.

## 🎮 Features

### Core Functionality
- **Game Library**: Browse and explore a comprehensive collection of games from Steam
- **User Authentication**: Secure user registration and login system
- **Game Search**: Search games by title, genre, publisher, or other criteria
- **Game Details**: View detailed information about games including descriptions, genres, publishers, and release dates
- **User Reviews**: Read and write reviews for games with rating system
- **Personal Wishlist**: Add games to your personal wishlist for future reference
- **User Profiles**: Manage user accounts and view gaming preferences

### Technical Features
- **Responsive Design**: Modern, mobile-friendly web interface
- **Database Support**: SQLAlchemy ORM with support for multiple database backends
- **Repository Pattern**: Clean architecture with repository pattern for data access
- **Comprehensive Testing**: Full test suite with pytest
- **Form Validation**: Secure form handling with WTForms and CSRF protection

## 🏗️ Architecture

This application follows a clean architecture pattern with clear separation of concerns:

- **Domain Model**: Core business entities (Game, User, Review, Wishlist, Publisher, Genre)
- **Repository Layer**: Data access abstraction supporting both memory and database storage
- **Web Layer**: Flask blueprints for different functional areas
- **Adapters**: Data readers and ORM mappings for external data sources

### Project Structure
```
games/
├── auth/           # User authentication
├── home/           # Home page and navigation
├── gamelibrary/    # Game browsing and library
├── search/         # Game search functionality
├── description/    # Game details and descriptions
├── reviews/        # Game reviews and ratings
├── wishlist/       # User wishlist management
├── profile/        # User profile management
├── domainmodel/    # Core business entities
├── adapters/       # Data access and repositories
├── static/         # CSS, JavaScript, images
├── templates/      # HTML templates
└── utilities/      # Helper functions and utilities
```

## 📊 Data Source

The application uses a comprehensive game dataset containing thousands of games with information including:
- Game titles and descriptions
- Publishers and developers
- Genres and categories
- Release dates and pricing
- Game screenshots and media

Data sourced from: [Steam Games Dataset](https://huggingface.co/datasets/FronkonGames/steam-games-dataset)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

**1. Clone the repository**
```bash
git clone <repository-url>
cd Game-Library
```

**2. Create and activate virtual environment**

**Windows:**
```bash
py -3 -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Environment Configuration**
Create a `.env` file in the project root with the following variables:
```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
TESTING=False
WTF_CSRF_SECRET_KEY=your-csrf-secret-key
REPOSITORY=database
ALCHEMY_URI=sqlite:///games.db
```

## 🎯 Running the Application

### Development Server
```bash
flask run
```

The application will be available at `http://localhost:5000`

### Production Deployment
```bash
python wsgi.py
```

## 🧪 Testing

### Running Tests
**Using PyCharm:**
1. Configure pytest as the testing tool (File → Settings → Tools → Python Integrated Tools → Testing)
2. Right-click the `tests` folder and select "Run pytest in tests"

**Using Terminal:**
```bash
python -m pytest tests
```

**Run specific test files:**
```bash
python -m pytest tests/unit/test_model.py
```

### Test Coverage
The application includes comprehensive tests for:
- Domain model entities and business logic
- Repository implementations (memory and database)
- Web routes and form handling
- Authentication and authorization
- Data validation and error handling

## 🛠️ Technologies Used

- **Backend**: Flask 2.3.2, Python 3.8+
- **Database**: SQLAlchemy 1.4.41 with SQLite (configurable)
- **Forms**: Flask-WTF 1.1.1, WTForms 3.0.1
- **Security**: Werkzeug 2.3.7, password-validator 1.0
- **Testing**: pytest 7.4.0
- **Configuration**: python-dotenv 1.0.0

## 📝 Configuration Options

The application supports various configuration options through environment variables:

- `FLASK_APP`: Entry point of the application (should be `wsgi.py`)
- `FLASK_ENV`: Environment mode (`development` or `production`)
- `SECRET_KEY`: Secret key for session encryption
- `TESTING`: Enable/disable testing mode
- `WTF_CSRF_SECRET_KEY`: CSRF protection secret key
- `REPOSITORY`: Repository type (`memory` or `database`)
- `ALCHEMY_URI`: Database connection string


**Happy Gaming! 🎮**



