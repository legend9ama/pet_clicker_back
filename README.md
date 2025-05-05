# Coursework Report: [Telegram Clicker Game](https://t.me/pet_clicker_game_bot)
---

## 1. Introduction  
### Purpose and Objectives  
The application is a **Telegram-based clicker game** where users:  
- Earn "Pet coins" through manual interaction or passive income through farms
- Buy/upgrade farms using in-game currency
- Compete via leaderboards
**Objectives**:  
- Implement core clicker game mechanics in Python  
- Design using OOP principles and patterns
- Integrate with Telegram's API
- Ensure scalability

### Project Overview  
- **Backend**: Python + FastAPI + SQLAlchemy + GCP(Cloud Run + Cloud SQL)  
- **Database**: PostgreSQL with async support hosted on Cloud SQL
- **Frontend**: React + Google Firebase(for hosting)
- **Auth**: Telegram WebApp validation
- **Key Features**:
  - Click accumulation system  
  - Leaderboard 
  - Passive income calculation
---

## 2. Problem Definition & Requirements  
### Problem Statement  
Traditional clicker games lack:  
- Seamless mobile integration  
- Real-time multiplayer features  
- Customizable progression systems  

### Requirements  
| **Functional** | **Non-Functional** |  
|----------------|--------------------|  
| User auth via Telegram | <1s API response time |  
| Farm purchase/upgrade | Data should persist between sessions |  
| Click tracking | Secure data validation |  
| Leaderboards | Handling multiple users concurrently |  

---

## 3. Design & Implementation  
### Architectural Patterns & OOP Principles  

#### 1. **Service-Repository Pattern**  
**Implementation**:  
```python  
# Abstraction via Base Classes  
class BaseRepository(ABC):
    def __init__(self, db: AsyncSession):
        self._db = db # Encapsulation

class UserRepository(BaseRepository):  # Inheritance
    ...

```
```python
# Abstraction via Base Classes
class BaseService(ABC):
    def __init__(self, repo: BaseRepository): # Composition
        self.repo = repo # Dependency Injection  

class UserService(BaseService): # Inheritance
    ...
```
**OOP Principles**:

 - **Abstraction**: BaseRepository defines interface

 - **Encapsulation**: Session/db details hidden in repository

 - **Composition**: Service contains repository

 - **Polymorphism**: Any BaseRepository implementation can be used

 - **Dependancy Injection**


#### 2. **Strategy Pattern for validation**
**Implementation**:  
```python  
# Strategy Abstraction  
class ValidationStrategy(ABC):  
    @abstractmethod  
    def validate(data): pass  

# Concrete Strategies  
class TelegramValidator(ValidationStrategy):  # Inheritance  
    def validate(self, data):  
        ...

class AdminKeyValidator(ValidationStrategy):  
    def validate(self, data):  
        ...
```  

#### **Database Models Diagram**
![db_diagram](docs/images/db_Diagram.png)

#### **Architecture Diagram**
![Architecture_diagram](docs/images/Architecture_Overview.png)

### **Key Algorithms and Data Structures**

#### **Alghorithms**
 - **Calculating passive income based on time passed from last collection**
 ```python
 collected = int(farm.current_income / 3600 * (time.mktime(datetime.timetuple(datetime.now())) - farm.last_collected))
 ```
 - **Exponential income and upgrade cost Growth Formula**
 ```python
 farm.current_income = template.base_income*(template.income_multiplier**farm.level)
 farm.current_upgrade_cost = template.base_price*(template.price_multiplier**farm.level)
 ```

 #### **Critical Data Structures**
 - **Composite Key Structure**

---

# Development Process

## 🛠️ Tools & Environment
- **Backend**: 
  - Python 3.12 + FastAPI
  - Cloud Run (Serverless Deployment)
  - Cloud SQL (PostgreSQL)
  - Docker 
- **Frontend**:
  - React
  - Firebase Hosting
  - Firestore (Optional for real-time features)
- **CI/CD**: 
  - Cloud Build
- **Monitoring**:
  - Cloud Logging
  - Cloud Monitoring

# Project Development Process

## 🛠️ Initial Stages
1. **Project Initialization & GitHub Setup**  
   - Created a GitHub repository for version control.  
   - Configured the environment: Python 3.12, virtual environment (`venv`), `requirements.txt`.  
   - Installed core dependencies: FastAPI, SQLAlchemy, asyncpg, Pydantic.

2. **Database Models & Connection**  
   - Implemented data models:  
     ```python
     class User(Base):
         __tablename__ = "users"
         telegram_id = Column(Integer, primary_key=True)
         # ... other fields
     ```
   - Configured async PostgreSQL connection via SQLAlchemy:  
     ```python
     DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
     engine = create_async_engine(DATABASE_URL)
     ```

3. **Docker Configuration**  
   - Created a `Dockerfile` for containerization.  
   - Configured environment variables for database connectivity.

## 📦 Core Application Development
4. **Repositories & Schemas**  
   - Built database repositories:  
     ```python
     class UserRepository:
         async def get_user(self, telegram_id: int) -> User:
             # ...
     ```
   - Designed Pydantic schemas for data validation:  
     ```python
     class UserResponse(BaseModel):
         telegram_id: int
         username: str
         # ...
     ```

5. **Services & Routers**  
   - Implemented business logic in services:  
     ```python
     class UserService:
         def __init__(self, repo: UserRepository):
             self.repo = repo
     ```
   - Configured FastAPI routers:  
     ```python
     @router.post("/users")
     async def create_user(user_data: UserCreate):
         # ...
     ```

6. **Telegram Integration**  
   - Studied Telegram Web Apps documentation.  
   - Implemented HMAC-SHA256 data validation:  
     ```python
     def validate_telegram_data(data: str) -> bool:
         # Signature verification
     ```

7. **Frontend Development**  
   - Built React interface: 
     - Home page  
     - Shop page 
     - Profile page  
     - Farm management panel 
     - Leaderboard 
   - Configured API client for backend communication.
   - Used DevTools to debug requests

## Deployment & Integration
8. **Initial Deployment**  
   - Deployed backend to Google Cloud Run.  
   - Hosted frontend on Firebase.  
---

# Results and Demonstration

### 1. Core Features Demonstration

**Main Clicker Interface**  
![Main Screen](docs/images/home_page.jpg)  
- Real-time click counter updates  
- Visual click animation  

**Farm Purchase**  
![Store](docs/images/Store_page.jpg)  
- Farm cards with price/income details  
- Purchase confirmation dialog  

**Farm Upgrading and Collecting**  
![Store](docs/images/Store_page.jpg)  
- Collect passive income  
- Upgrade Farms  

**Profile Page**  
![Profile](docs/images/profile_page.jpg)   
- Telegram synced username  
- Stats: Account info  

**Leaderboard**  
![Leaderboard](docs/images/leaderboard_page.jpg)   
- Global ranking based on amount of coins

---

# Testing and Validation

## Testing Procedures

### 1. **Unit Testing (Click Module)**
**Schemas Validation and Click repository testing**
- Fixed minor issues with validation

### 2. **Telegram Environment Testing**
- Verified data validation accuracy.  
- Fixed critical issues:  
    - Telegram Desktop Coins and Farms Display Issues (307 Error)
    - Fake requests for coins incrementing

---

# Conclusion and Future Work  

## Achievements Summary  
✅ **Fully Functional Core Product**:  
- Complete implementation of core clicker mechanics with real-time synchronization  
- Intuitive user interface for farm management and progression  
- Stable leaderboard system tracking top 5 global players  
- Robust Telegram data validation and profile synchronization  

✅ **Technical Implementation**:  
- Asynchronous PostgreSQL architecture 
- Anti-cheat protection for click/farm interactions

---

## Future Development Roadmap  

### 1. Enhanced Gameplay Mechanics  
- **Unique Farm Mechanics**: Implement specialized logic for each farm type including:  
  - Time-based production bonuses  
  - Resource synergies between different farms  
  - Random event triggers affecting farm output  
- **Advanced Progression System**:  
  - Prestige mechanics with permanent upgrades  
  - Skill trees for personalized playstyles  
  - Limited-time seasonal events  

### 2. Interface Improvements  
- **Dynamic Visual Feedback**:  
  - Animated farm environments reflecting upgrade levels  
  - Interactive progress visualizations  
  - Customizable UI themes and layouts  

### 3. Security & Administration  
- **Advanced Validation Systems**:   
  - Multi-layer request verification  
- **Comprehensive Admin Tools**:  
  - Real-time player activity monitoring  
  - Economy balancing interface  
  - Remote issue resolution system  

### 4. Community Features  
- **Social Gameplay Elements**:  
  - Cooperative farm alliances  
  - Resource trading marketplace  
  - Player-created challenges  
  - Farm customization toolkit  

---
