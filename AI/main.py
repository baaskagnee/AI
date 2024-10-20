import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

# Мэдээллийн загвар (жишээ)
data = {
    'questions': [
        "Таны нэр юу?", "Сайн уу?", "Та юу хийдэг вэ?", "Баярлалаа", 
        "Та хэлийг яаж сурах вэ?", "Хамгийн том хот ямар вэ?"],
    'answers': [
        "Миний нэр Chatbot.", "Сайн байна уу!", "Би танд асуултанд хариулахад тусална.", 
        "Танд баярлалаа!", "Хэл сурах чухал.", "Улаанбаатар."
    ]
}

# Дата рам үүсгэх
df = pd.DataFrame(data)

# Мэдээллийг бэлтгэх
X = df['questions']
y = df['answers']

# Дата сургалт, тест дунд хуваах
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Машин сургалтын загвар үүсгэх
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Загварыг сургах
model.fit(X_train, y_train)

# Хэрэглэгчийн асуултанд таамаглах
def predict_answer(user_input):
    return model.predict([user_input])[0]

# Chatbot функц
def chatbot():
    print("Chatbot-той ярилцахад тавтай морил! (гарчиг 'төгсгөл'-д дуусах)")
    
    while True:
        user_input = input("Та: ")
        if user_input.lower() == 'төгсгөл':
            print("Chatbot: Баярлалаа! Уулзсандаа баяртай байна.")
            break
        response = predict_answer(user_input)
        print(f"Chatbot: {response}")

# Chatbot-ыг эхлүүлэх
print(df)
chatbot()

