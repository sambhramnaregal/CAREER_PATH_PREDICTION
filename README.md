# Career Path Prediction System

A sophisticated AI-powered web application for predicting career paths of engineering students. This system moves beyond simple classification by using **Unsupervised Learning (K-Means Clustering)** to identify nuanced student profiles and integrates **Google Gemini AI** for personalized, context-aware career coaching and roadmap generation.

## 🌟 Why This Project is Unique

Most career prediction systems use simple supervised learning (classification) to label students into pre-defined buckets like "Placement" or "Higher Studies."  
**This project is different because:**

1.  **Unsupervised Learning (Discovery over Assumption)**: We use **K-Means Clustering** to let the data speak for itself. Instead of forcing students into boxes, the algorithm identifies *natural groupings* of students (e.g., "The Tech Innovator," "The Research Scholar," "The Corporate Leader") based on 17+ dimensions.
2.  **Context-Aware GenAI**: We don't just give a label. We use **Google Gemini AI** to act as a personalized mentor. The AI understands the *nuance* of why a student falls into a specific cluster and provides advice tailored to that specific context.
3.  **Holistic Evaluation**: We look beyond CGPA. We analyze 12+ distinct factors including *family business background*, *entrepreneurial mindset*, *soft skills*, and *leadership roles* to give a truly 360-degree view.

## 🎓 Impact on Colleges & Institutions

This system solves the "One-Size-Fits-All" mentorship problem in large institutions:

*   **📈 Improved Placement Rates**: By identifying early which students need specific interventions (e.g., high technical skills but low soft skills), colleges can run targeted training programs.
*   **� Scalable Mentorship**: Provides high-quality, personalized career guidance to thousands of students instantly, relieving pressure on limited placement cell staff.
*   **� Data-Driven Decisions**: Empowers HoDs and Placement Officers to see the "Talent Distribution" of a batch. For example, knowing that "40% of the batch are Research-Oriented" helps in planning curriculum changes or inviting specific guest speakers.
*   **🚀 Entrepreneurial Support**: Specifically identifies students with hidden entrepreneurial potential who might otherwise be lost in the placement crowd, allowing colleges to nurture them in incubation centers.

## 🚀 Key Features

## 🛠️ Technology Stack

### Backend
*   **Flask**: REST API framework.
*   **Google Gemini API**: Generative AI for chatbots and roadmaps.
*   **Scikit-learn**: K-Means Clustering, PCA, Scaling.
*   **Pandas/NumPy**: Data processing and analytics.

### Frontend
*   **React 18**: Component-based UI.
*   **Tailwind CSS**: Utility-first styling.
*   **Framer Motion**: Smooth animations.
*   **Recharts**: Data visualization.

## 📁 Project Structure

```
Career Path Prediction/
├── backend/
│   ├── app.py                 # Main Flask Application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # API Keys (Create this!)
├── frontend/
│   ├── src/                   # React Source Code
│   └── public/                # Static Assets
├── models/
│   ├── kmeans_model.pkl       # Trained K-Means Clusterer
│   ├── scaler.pkl            # Feature Scaler
│   ├── pca.pkl               # PCA Model for dimensionality reduction
│   ├── cluster_info.pkl      # Metadata for each cluster (Names, Roles)
│   └── label_encoders.pkl    # Encoders for categorical data
└── README.md
```

## ⚙️ Setup Instructions

### 1. Prerequisites
*   Node.js (v16+)
*   Python (v3.8+)
*   Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/))

### 2. Clone & Navigate
```powershell
cd "C:\Career Path Prediction"
```

### 3. Backend Setup
1.  **Navigate to backend:**
    ```powershell
    cd backend
    ```
2.  **Create Virtual Environment:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
3.  **Install Dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    Create a file named `.env` in the root (parent of `backend`) or inside `backend/` and add your key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    GEMINI_MODEL_NAME=models/gemini-pro
    ```
5.  **Run Server:**
    ```powershell
    python app.py
    ```
    *Server runs on: `http://localhost:5001`*

### 4. Frontend Setup
1.  **Open a new terminal and navigate to frontend:**
    ```powershell
    cd "C:\Career Path Prediction\frontend"
    ```
2.  **Install Dependencies:**
    ```powershell
    npm install
    ```
3.  **Start Application:**
    ```powershell
    npm start
    ```
    *App runs on: `http://localhost:3000`*

### 5. Model Setup (Critical)
The system requires trained `.pkl` files in the `models/` directory.
*   **kmeans_model.pkl**: The clustering logic.
*   **cluster_info.pkl**: Dictionary mapping Cluster IDs to Profile Names (e.g., `{0: {'name': 'Tech Innovator', 'roles': [...]}}`).
*   **scaler.pkl** & **pca.pkl**: For data preprocessing.

## 🎯 How It Works

### The AI Prediction Engine
Unlike simple classifiers that say "Placement" or "Higher Studies", our engine:
1.  **Takes 17 Inputs**: Academics, skills, projects, internships, etc.
2.  **Encodes & Scales**: Preprocesses data to match training distribution.
3.  **PCA Transformation**: Reduces dimensionality to capture core variance.
4.  **Clustering**: Assigns the student to a specific "Persona" (Cluster) based on K-Means.
5.  **Contextual Analysis**: Retrieves the specific traits, strengths, and suggested roles for that Persona.
### 🔬 The Science: How Clusters are Labelled

The core intelligence of this system lies in how it defines a student's profile. We don't just "guess"; we use rigorous mathematical modeling.

#### 1. The Basis (17-Dimensional Analysis)
Every student is evaluated on **17 distinct parameters**, not just marks. These include:
*   **Academic**: CGPA, Backlogs.
*   **Technical**: Coding skills, Hackathons, Projects.
*   **Research**: Publications, Internship Types (R&D vs Corporate).
*   **Personality**: Leadership roles, Soft skills, Entrepreneurial background.

#### 2. The Tech (PCA + K-Means)
*   **Step 1: Dimensionality Reduction (PCA)**: It is hard to visualize 17 dimensions. We use **Principal Component Analysis (PCA)** to compress these 17 features into core components that capture 95% of the variance (the "essence" of the student data).
*   **Step 2: Clustering (K-Means)**: The K-Means algorithm groups students who are mathematically similar in this multi-dimensional space. It blindly identifies "clouds" of students without knowing who they are.

#### 3. The Labeling Logic (Centroid Analysis)
Once clusters are formed, we analyze the **mathematical centroid** (average behavior) of each cluster to assign a label.
*   **Example 1**: A cluster with **High Research Papers + High CGPA + Low Projects** is labeled **"The Aspiring Academic"** (Target: PhD/Masters).
*   **Example 2**: A cluster with **High Hackathons + High Technical Skills + Avg CGPA** is labeled **"The Tech Innovator"** (Target: SDE Roles).
*   **Example 3**: A cluster with **Family Business + High Leadership + Entrepreneur Cell** is labeled **"The Future Founder"** (Target: Startup/Management).

This ensures that the career advice is partially **data-derived** (what you are good at) and partially **market-aligned** (what roles fit that profile).

### 🏆 The 5 Student Profiles (Clusters)

The system currently identifies **5 distinct student personas** through clustering:

1.  **Cluster 0: Technical Innovators**
    *   **Traits**: Strong coding ability, technical inclination, and analytical thinking.
    *   **Target Roles**: Software Engineer, Backend Developer, AI Engineer.

2.  **Cluster 1: Research & Data Learners**
    *   **Traits**: Good academic mindset, research interest, and analytical thinking.
    *   **Target Roles**: Data Analyst, Research Intern.

3.  **Cluster 2: Career Growth Oriented Learners**
    *   **Traits**: Growing skillset, quick learning mindset, consistent improvement focus.
    *   **Target Roles**: Associate Engineer, Junior Developer.

4.  **Cluster 3: Technical Specialist**
    *   **Traits**: Focuses on specialized technical infrastructure and security.
    *   **Target Roles**: DevOps Engineer, Cloud Architect, Cybersecurity Specialist.

5.  **Cluster 4: Research Innovator**
    *   **Traits**: Driven by deep innovation and advanced technical research.
    *   **Target Roles**: R&D Scientist, AI Researcher, Data Scientist.

### GenAI Integration
Once a profile is identified:
*   **Roadmap Generation**: The app sends the student's specific gaps (e.g., "Good CGPA but low practical skills") + target Persona to Gemini, which generates a week-by-week action plan.
*   **Chatbot**: The chat interface injects the Student's Profile Context into the LLM system prompt, allowing the AI to answer like a personalized mentor (e.g., "Given your strong research background, you should apply for...").

## 📄 License
Project is for educational purposes.
