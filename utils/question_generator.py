import random

TOPIC_QUESTIONS = {
    'python': [
        ('What is Python and what are its key features?', 'Python is a high-level, interpreted, general-purpose programming language known for its simplicity, readability, dynamic typing, and extensive standard library. Key features include easy syntax, object-oriented support, and large community.'),
        ('Explain the difference between a list and a tuple in Python.', 'Lists are mutable sequences defined with square brackets. Tuples are immutable sequences defined with parentheses. Lists support modification after creation while tuples do not, making tuples faster and safer for constant data.'),
        ('What are Python decorators?', 'Decorators are functions that modify the behavior of another function or class without changing its source code. They use the @symbol syntax and wrap the target function to add extra functionality like logging, timing, or access control.'),
        ('What is the difference between shallow copy and deep copy?', 'A shallow copy creates a new object but inserts references to the objects found in the original. A deep copy creates a new object and recursively copies all objects inside it, so changes to the copy do not affect the original.'),
        ('How does Python manage memory?', 'Python uses automatic memory management through reference counting and a cyclic garbage collector. When an object has no more references pointing to it, the memory is freed automatically by the garbage collector.'),
        ('What is the difference between __str__ and __repr__ in Python?', '__str__ is used for creating a human-readable string representation of an object, intended for end users. __repr__ is used for an unambiguous representation mainly for developers and debugging. If __str__ is not defined, Python falls back to __repr__.'),
        ('What are Python generators and how do they work?', 'Generators are functions that use the yield keyword to return values one at a time, pausing execution between each yield. They are memory efficient because they produce values lazily on demand rather than storing all values in memory at once.'),
        ('Explain list comprehension in Python with an example.', 'List comprehension provides a concise way to create lists. For example: squares = [x**2 for x in range(10)] creates a list of squares from 0 to 81. It can also include conditions like [x for x in range(20) if x % 2 == 0] for even numbers.'),
        ('What is the GIL in Python?', 'The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously. This limits true multi-core parallel execution in CPython but does not affect multiprocessing.'),
        ('What is the difference between *args and **kwargs?', '*args allows a function to accept any number of positional arguments as a tuple. **kwargs allows a function to accept any number of keyword arguments as a dictionary. Both can be used together to create highly flexible functions.'),
        ('What are Python lambda functions?', 'Lambda functions are small anonymous functions defined using the lambda keyword. They can have any number of arguments but only one expression. Example: add = lambda x, y: x + y. They are often used with map(), filter(), and sorted() functions.'),
        ('What is the difference between is and == in Python?', 'The == operator checks if two objects have the same value. The is operator checks if two variables point to the exact same object in memory. For example, two lists with same content are == but not is unless they reference the same list object.'),
        ('Explain exception handling in Python.', 'Python uses try-except-else-finally blocks. Code that might raise an exception goes in try. Specific exceptions are caught in except blocks. The else block runs if no exception occurred. Finally always runs for cleanup like closing files or database connections.'),
        ('What are Python modules and packages?', 'A module is a single Python file containing functions, classes, and variables. A package is a directory containing multiple modules with an __init__.py file. Modules are imported using the import statement to organize and reuse code across projects.'),
        ('What is the difference between append() and extend() in Python lists?', 'append() adds a single element to the end of a list. extend() adds all elements from an iterable to the end of the list. For example, list.append([1,2]) adds the entire list as one element, while list.extend([1,2]) adds 1 and 2 as separate elements.'),
    ],
    'java': [
        ('What is Java and explain OOP concepts?', 'Java is a strongly-typed, object-oriented programming language. OOP concepts include Encapsulation (hiding data), Inheritance (reusing code), Polymorphism (many forms), and Abstraction (hiding implementation details).'),
        ('What is the difference between JDK, JRE, and JVM?', 'JVM (Java Virtual Machine) executes bytecode. JRE (Java Runtime Environment) includes JVM plus libraries to run Java programs. JDK (Java Development Kit) includes JRE plus development tools like compiler for writing Java programs.'),
        ('What are Java interfaces and abstract classes?', 'An interface defines a contract with abstract methods that implementing classes must fulfill. An abstract class can have both abstract and concrete methods. A class can implement multiple interfaces but extend only one abstract class.'),
        ('Explain exception handling in Java.', 'Java uses try-catch-finally blocks to handle exceptions. Try block contains code that might throw an exception. Catch block handles specific exceptions. Finally block always executes for cleanup. Throws keyword declares exceptions a method may throw.'),
        ('What is multithreading in Java?', 'Multithreading allows concurrent execution of multiple threads within a program. Threads share memory and resources. Java provides Thread class and Runnable interface. Synchronization is used to prevent race conditions when multiple threads access shared data.'),
        ('What is the difference between String, StringBuilder, and StringBuffer in Java?', 'String is immutable so each modification creates a new object. StringBuilder is mutable and not thread-safe, best for single-threaded use. StringBuffer is mutable and thread-safe due to synchronized methods, making it slower than StringBuilder.'),
        ('What are Java Collections? Explain List, Set, and Map.', 'Java Collections Framework provides data structures. List (ArrayList, LinkedList) allows duplicates in order. Set (HashSet, TreeSet) stores unique elements. Map (HashMap, TreeMap) stores key-value pairs. Each has different performance characteristics.'),
        ('What is Java inheritance and method overriding?', 'Inheritance allows a class to inherit properties and methods from a parent class using the extends keyword. Method overriding allows a subclass to provide a specific implementation of a method already defined in the parent class using @Override annotation.'),
        ('What is the difference between == and .equals() in Java?', '== compares object references (memory addresses) for objects and values for primitives. .equals() compares the actual content of objects. For String comparison always use .equals() because == checks if they are the exact same object in memory.'),
        ('What is Java garbage collection?', 'Garbage collection is the automatic process of reclaiming memory occupied by objects no longer referenced by the program. The JVM garbage collector runs automatically, identifies unreachable objects, and frees their memory. Developers cannot control exactly when it runs.'),
        ('What are access modifiers in Java?', 'Java has four access modifiers: public (accessible everywhere), protected (accessible within same package and subclasses), default/package-private (accessible within same package only), and private (accessible only within the same class).'),
        ('What is the difference between ArrayList and LinkedList?', 'ArrayList uses a dynamic array and provides O(1) access by index but O(n) for insertion/deletion in middle. LinkedList uses doubly-linked nodes providing O(1) insertion/deletion but O(n) for index access. ArrayList is preferred for random access, LinkedList for frequent insertions.'),
        ('Explain the concept of polymorphism in Java.', 'Polymorphism means an object can take many forms. Compile-time polymorphism is achieved through method overloading (same method name, different parameters). Runtime polymorphism is achieved through method overriding where the correct method is determined at runtime based on actual object type.'),
        ('What is a Java constructor?', 'A constructor is a special method with the same name as the class used to initialize new objects. It has no return type. Java provides a default no-arg constructor if none is defined. Constructors can be overloaded. The this() call can invoke another constructor in the same class.'),
        ('What is static keyword in Java?', 'Static members belong to the class rather than any instance. Static variables are shared among all objects of the class. Static methods can be called without creating an object. Static blocks run once when the class is loaded. Static inner classes do not need an instance of the outer class.'),
    ],
    'hr': [
        ('Tell me about yourself.', 'A good answer covers your educational background, relevant skills, work experience, and why you are interested in this role. Keep it professional, concise (2-3 minutes), and relevant to the job you are applying for.'),
        ('What are your strengths and weaknesses?', 'For strengths, mention skills relevant to the job backed by examples. For weaknesses, mention a real weakness you are actively working to improve, showing self-awareness and growth mindset without mentioning anything critical to the role.'),
        ('Where do you see yourself in 5 years?', 'A good answer shows ambition aligned with the company. Mention growing your skills, taking on more responsibility, and contributing to the organization. Show commitment and a desire to advance within the company.'),
        ('Why do you want to work for our company?', 'Research the company beforehand. Mention specific things like company culture, products, reputation, growth opportunities, or mission that genuinely appeal to you. Relate it to your own career goals and values.'),
        ('How do you handle pressure and stress?', 'Describe specific strategies like prioritizing tasks, breaking large problems into smaller ones, staying organized, and maintaining work-life balance. Give a real example of a stressful situation you handled successfully.'),
        ('Describe a time you worked in a team and faced a conflict.', 'Use the STAR method: Situation (describe the conflict), Task (your role), Action (steps you took like communicating openly and finding common ground), Result (positive outcome). Show your conflict resolution and communication skills.'),
        ('What motivates you?', 'Be honest and align with the job. Common motivators include challenging work, learning opportunities, making an impact, recognition, or collaboration. Avoid mentioning only salary. Give a specific example of when you felt highly motivated.'),
        ('Why are you leaving your current job?', 'Keep it positive. Focus on growth, new opportunities, or seeking challenges that align with your career goals. Avoid criticizing your previous employer. If you are a fresher, explain your reasons for choosing this role and company.'),
        ('How do you prioritize your work?', 'Describe a systematic approach: listing tasks, assessing urgency and importance (like Eisenhower Matrix), setting deadlines, and communicating with stakeholders when priorities conflict. Give a real example of managing multiple deadlines.'),
        ('What is your greatest professional achievement?', 'Use the STAR method to describe a specific accomplishment. Quantify results where possible (increased efficiency by 30%, reduced errors by 50%). Choose an achievement relevant to the role you are applying for.'),
        ('Are you a team player or do you prefer working alone?', 'Show flexibility by explaining you can do both effectively. Give examples of successful teamwork and also times you worked independently. Emphasize that you adapt your style based on what the project or situation requires.'),
        ('How do you handle criticism?', 'Show that you welcome constructive feedback as an opportunity to grow. Explain that you listen carefully, ask clarifying questions if needed, thank the person, and take concrete steps to improve. Give an example if possible.'),
        ('What are your salary expectations?', 'Research industry standards beforehand. Give a range based on your experience, skills, and market data. Express flexibility while stating your minimum expectation. Mention that compensation includes the full package including growth opportunities and benefits.'),
        ('Describe your leadership style.', 'Describe how you motivate and guide others. Mention qualities like leading by example, empowering team members, being decisive, communicating clearly, and adapting your style to team needs. Support with a specific leadership example.'),
    ],
    'sql': [
        ('What is SQL and what are its main types of commands?', 'SQL (Structured Query Language) is used to manage relational databases. Main types: DDL (CREATE, ALTER, DROP), DML (SELECT, INSERT, UPDATE, DELETE), DCL (GRANT, REVOKE), and TCL (COMMIT, ROLLBACK).'),
        ('Explain the difference between WHERE and HAVING clause.', 'WHERE filters rows before grouping and cannot use aggregate functions. HAVING filters groups after GROUP BY and can use aggregate functions like COUNT, SUM, AVG. WHERE works on individual rows, HAVING works on grouped results.'),
        ('What are SQL joins? Explain types.', 'Joins combine rows from multiple tables. INNER JOIN returns matching rows from both tables. LEFT JOIN returns all rows from left table and matching rows from right. RIGHT JOIN is opposite. FULL JOIN returns all rows from both tables.'),
        ('What is normalization in databases?', 'Normalization organizes a database to reduce redundancy and improve data integrity. 1NF removes duplicate columns. 2NF removes partial dependencies. 3NF removes transitive dependencies. Higher normal forms provide even stricter rules.'),
        ('What is an index in SQL?', 'An index is a database object that speeds up data retrieval operations on a table. It creates a separate data structure that allows the database to find rows quickly without scanning the entire table. However indexes slow down write operations.'),
        ('What is the difference between DELETE, TRUNCATE, and DROP?', 'DELETE removes specific rows and can be rolled back, supports WHERE clause. TRUNCATE removes all rows quickly without logging individual row deletions, cannot be rolled back in most databases. DROP removes the entire table structure and data permanently.'),
        ('What are primary keys and foreign keys?', 'A primary key uniquely identifies each record in a table. It cannot be NULL and must be unique. A foreign key is a column that references the primary key of another table, establishing a relationship between tables and enforcing referential integrity.'),
        ('Explain the difference between UNION and UNION ALL.', 'UNION combines results of two SELECT statements and removes duplicate rows. UNION ALL combines results and keeps all duplicate rows. UNION ALL is faster because it skips the deduplication step. Both require the same number of columns with compatible data types.'),
        ('What are stored procedures?', 'Stored procedures are precompiled SQL code stored in the database that can be executed repeatedly. They accept input parameters and can return output. Benefits include better performance due to precompilation, code reusability, security through encapsulation, and reduced network traffic.'),
        ('What is a subquery in SQL?', 'A subquery is a query nested inside another query. It can appear in SELECT, FROM, WHERE, or HAVING clauses. Subqueries can be correlated (referencing the outer query) or non-correlated (independent). They are used to perform operations that require multiple steps.'),
        ('What is the difference between INNER JOIN and LEFT JOIN?', 'INNER JOIN returns only the rows where there is a match in both tables. LEFT JOIN returns all rows from the left table and the matching rows from the right table. If no match exists in the right table, NULL values are returned for right table columns.'),
        ('What are aggregate functions in SQL?', 'Aggregate functions perform calculations on multiple rows and return a single value. Common ones: COUNT() counts rows, SUM() adds numeric values, AVG() calculates average, MAX() finds maximum, MIN() finds minimum. They are often used with GROUP BY clause.'),
        ('What is a view in SQL?', 'A view is a virtual table based on the result set of an SQL query. It does not store data physically but provides a saved query that can be used like a table. Views simplify complex queries, provide security by hiding sensitive columns, and present data in different ways.'),
        ('What is the difference between CHAR and VARCHAR?', 'CHAR is a fixed-length character data type that always uses the defined length, padding with spaces. VARCHAR is variable-length and only uses the space needed plus a small overhead. CHAR is faster for fixed-length data; VARCHAR saves space for variable-length data.'),
        ('Explain transactions in SQL and ACID properties.', 'A transaction is a unit of work that is either fully completed or fully rolled back. ACID properties: Atomicity (all or nothing), Consistency (data remains valid), Isolation (concurrent transactions do not interfere), Durability (committed transactions are permanent).'),
    ],
    'data science': [
        ('What is data science and its key components?', 'Data science extracts insights from structured and unstructured data using statistics, machine learning, and programming. Key components include data collection, data cleaning, exploratory analysis, model building, evaluation, and deployment.'),
        ('Explain overfitting and underfitting in machine learning.', 'Overfitting occurs when a model learns training data too well including noise and performs poorly on new data. Underfitting occurs when a model is too simple to capture underlying patterns. The goal is to find the right balance using techniques like regularization and cross-validation.'),
        ('What is the difference between supervised and unsupervised learning?', 'Supervised learning uses labeled training data where the algorithm learns the mapping from inputs to outputs. Unsupervised learning finds patterns in data without labeled responses, discovering hidden structure through clustering or dimensionality reduction.'),
        ('What is cross-validation?', 'Cross-validation is a technique to evaluate model performance by splitting data into multiple subsets. The most common is k-fold cross-validation where data is split into k equal parts, training on k-1 parts and testing on the remaining part, repeated k times.'),
        ('Explain precision, recall, and F1 score.', 'Precision is the proportion of true positives among all predicted positives. Recall is the proportion of true positives among all actual positives. F1 score is the harmonic mean of precision and recall, balancing both metrics. Useful for imbalanced datasets.'),
        ('What is the bias-variance tradeoff?', 'Bias is the error from overly simplified assumptions causing underfitting. Variance is the error from sensitivity to training data fluctuations causing overfitting. The tradeoff means reducing bias often increases variance and vice versa. The goal is to find the optimal balance minimizing total error.'),
        ('What is a confusion matrix?', 'A confusion matrix is a table showing True Positives, True Negatives, False Positives, and False Negatives. From it we derive metrics like accuracy, precision, recall, and F1 score. It gives a complete picture of how well a classification model performs across all classes.'),
        ('What is the difference between classification and regression?', 'Classification predicts discrete categorical labels (yes/no, spam/not spam, categories). Regression predicts continuous numerical values (price, temperature, salary). Classification uses algorithms like logistic regression and random forest; regression uses linear regression and similar models.'),
        ('What is feature engineering?', 'Feature engineering is the process of using domain knowledge to create, transform, or select input variables to improve model performance. It includes creating new features from existing ones, handling missing values, encoding categorical variables, normalizing data, and removing irrelevant features.'),
        ('What is principal component analysis (PCA)?', 'PCA is a dimensionality reduction technique that transforms data into a new coordinate system where the greatest variance is captured in the fewest dimensions (principal components). It reduces computational cost, removes correlated features, and helps visualize high-dimensional data.'),
        ('Explain the Random Forest algorithm.', 'Random Forest is an ensemble method that builds multiple decision trees on random subsets of data and features, then combines their predictions by majority voting for classification or averaging for regression. It reduces overfitting compared to single decision trees and handles high-dimensional data well.'),
        ('What is gradient descent?', 'Gradient descent is an optimization algorithm that minimizes a function by iteratively moving in the direction of steepest descent (negative gradient). In machine learning, it minimizes the loss function by updating model parameters. Variants include batch, stochastic, and mini-batch gradient descent.'),
        ('What are the steps in a typical data science project?', 'Steps include: 1) Problem definition and goal setting, 2) Data collection and acquisition, 3) Exploratory data analysis, 4) Data cleaning and preprocessing, 5) Feature engineering, 6) Model selection and training, 7) Model evaluation and tuning, 8) Deployment and monitoring.'),
        ('What is the difference between a data scientist and a data analyst?', 'A data analyst focuses on interpreting existing data using SQL, Excel, and visualization tools to answer specific business questions. A data scientist builds predictive models, develops algorithms, and uses advanced machine learning and statistical techniques to extract deeper insights and predict future outcomes.'),
        ('What is regularization in machine learning?', 'Regularization adds a penalty term to the loss function to prevent overfitting by discouraging overly complex models. L1 regularization (Lasso) adds the absolute value of coefficients and can produce sparse models. L2 regularization (Ridge) adds squared coefficients. Elastic Net combines both.'),
    ],
    'machine learning': [
        ('What is machine learning and its types?', 'Machine learning is a subset of AI that enables systems to learn from data without explicit programming. Types: supervised learning (labeled data), unsupervised learning (unlabeled data), reinforcement learning (learning through rewards and penalties), and semi-supervised learning.'),
        ('Explain the difference between a parametric and non-parametric model.', 'Parametric models assume a fixed functional form with a fixed number of parameters regardless of training data size (e.g., linear regression). Non-parametric models make fewer assumptions and complexity grows with data (e.g., k-nearest neighbors, decision trees).'),
        ('What is k-nearest neighbors (KNN)?', 'KNN is a simple algorithm that classifies a data point based on the majority class of its k nearest neighbors in the feature space. The distance metric (usually Euclidean) determines closeness. It requires no training phase but is slow at prediction time and sensitive to irrelevant features.'),
        ('What is a neural network?', 'A neural network is a computational model inspired by the human brain, consisting of interconnected layers of nodes (neurons). Input layer receives data, hidden layers transform it through weighted connections and activation functions, and output layer produces predictions. Deep learning uses many hidden layers.'),
        ('What is the difference between bagging and boosting?', 'Bagging (Bootstrap Aggregating) trains multiple models independently on random subsets and combines their predictions to reduce variance (e.g., Random Forest). Boosting trains models sequentially where each model corrects previous errors to reduce bias (e.g., AdaBoost, XGBoost, Gradient Boosting).'),
    ],
    'javascript': [
        ('What is JavaScript and what is it used for?', 'JavaScript is a dynamic, interpreted scripting language primarily used for making web pages interactive. It runs in browsers and on servers (Node.js). It supports event-driven, functional, and object-oriented programming styles and is essential for front-end web development.'),
        ('What is the difference between var, let, and const?', 'var has function scope and is hoisted. let has block scope and is not hoisted to usable state. const has block scope and cannot be reassigned (though objects/arrays it references can be mutated). let and const are modern ES6 additions; prefer them over var.'),
        ('What are JavaScript promises?', 'Promises represent the eventual result of an asynchronous operation. They have three states: pending, fulfilled (resolved), or rejected. Promises chain using .then() for success and .catch() for errors. async/await syntax provides cleaner way to work with promises using synchronous-looking code.'),
        ('Explain event bubbling and capturing in JavaScript.', 'Event bubbling: when an event fires on a child element, it propagates up to parent elements. Event capturing: events travel from the root down to the target element. addEventListener third parameter controls phase. event.stopPropagation() prevents further propagation in either direction.'),
        ('What is the difference between == and === in JavaScript?', '== performs type coercion before comparison so 1 == "1" is true. === is strict equality that checks both value and type without coercion so 1 === "1" is false. Always prefer === to avoid unexpected type coercion bugs in JavaScript.'),
        ('What is closure in JavaScript?', 'A closure is a function that retains access to variables from its outer (enclosing) scope even after the outer function has returned. Closures enable data encapsulation, private variables, and factory functions. They are fundamental to JavaScript functional programming patterns.'),
        ('What is the difference between synchronous and asynchronous JavaScript?', 'Synchronous code executes line by line, blocking until each operation completes. Asynchronous code allows the program to continue executing while waiting for operations like API calls or file reads. JavaScript handles async through callbacks, promises, and async/await using the event loop.'),
    ],
}

SKILL_TO_TOPIC = {
    'Python': 'python',
    'Java': 'java',
    'Javascript': 'javascript',
    'Sql': 'sql',
    'Mysql': 'sql',
    'Data Science': 'data science',
    'Machine Learning': 'machine learning',
    'Deep Learning': 'machine learning',
    'Scikit-Learn': 'data science',
    'Pandas': 'data science',
    'Numpy': 'data science',
}

QUESTIONS_PER_INTERVIEW = 5


def get_questions_for_topic(topic, count=QUESTIONS_PER_INTERVIEW):
    key = topic.lower()
    pool = TOPIC_QUESTIONS.get(key, TOPIC_QUESTIONS['hr'])
    return random.sample(pool, min(count, len(pool)))


def get_questions_for_skills(skills, count=8):
    questions = []
    seen_topics = set()
    random.shuffle(skills)
    for skill in skills:
        topic = SKILL_TO_TOPIC.get(skill)
        if topic and topic not in seen_topics:
            seen_topics.add(topic)
            pool = TOPIC_QUESTIONS.get(topic, [])
            picked = random.sample(pool, min(2, len(pool)))
            questions.extend(picked)
    if not questions:
        questions = random.sample(TOPIC_QUESTIONS['hr'], QUESTIONS_PER_INTERVIEW)
    # Always add 2 HR questions
    hr_pool = TOPIC_QUESTIONS['hr']
    questions.extend(random.sample(hr_pool, min(2, len(hr_pool))))
    random.shuffle(questions)
    return questions[:count]


def get_available_topics():
    return list(TOPIC_QUESTIONS.keys())

def generate_questions_from_resume(resume_text, num_questions=8):
    import os
    import json
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("[WARNING] GROQ_API_KEY not set, falling back to static questions.")
        return None
        
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        prompt = f"""
        You are an expert technical interviewer.
        Your task is to extract the candidate's core technical skills and generate {num_questions} interview questions strictly based ONLY on the following candidate's resume text.
        Do NOT ask generic behavioral questions (like "What is your greatest weakness?").
        Do NOT ask "Do you have any questions for us?".
        Do NOT ask broad technical questions unless the specific skill or concept is explicitly mentioned in the resume.
        Every single question MUST be directly tied to a specific project, job experience, or skill listed in the text provided below.
        
        Format your response ONLY as a valid JSON object containing an array called "skills" and an array called "questions".
        The "questions" array objects must have:
        "q": "The interview question"
        "a": "A brief ideal answer or key points the candidate should mention based on their resume"
        
        Example format:
        {{
            "skills": ["Python", "React", "Docker"],
            "questions": [
                {{"q": "I see you built a task manager using React. What state management approach did you use for that project?", "a": "Candidate should mention Redux or Context API as they listed it in their skills."}}
            ]
        }}
        
        Resume text:
        {resume_text[:5000]}
        """
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON generating assistant that outputs only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            temperature=0.5
        )
        
        text = response.choices[0].message.content.strip()
        data = json.loads(text)
        
        formatted_questions = []
        question_list = data.get("questions", []) if isinstance(data, dict) else data
        extracted_skills = data.get("skills", []) if isinstance(data, dict) else []
        
        for item in question_list:
            if isinstance(item, dict) and "q" in item and "a" in item:
                formatted_questions.append({'q': item['q'], 'a': item['a']})
                
        if len(formatted_questions) >= 3:
            return {
                "questions": formatted_questions[:num_questions],
                "skills": extracted_skills
            }
            
    except Exception as e:
        print(f"[ERROR] Groq generation failed: {str(e)}")
    
    return None
