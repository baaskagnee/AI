from transformers import GPT2LMHeadModel, GPT2Tokenizer

# GPT-2 загварыг дуудаж авах
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Өгүүлбэр үүсгэх эхлэл
input_text = "Таны нэр юу вэ?"

# Текстийг токенууд болгон хөрвүүлэх
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Өгүүлбэрийг зохиох (моделийг ажиллуулах)
output = model.generate(
    input_ids,
    max_length=50,          # Үүсгэх өгүүлбэрийн урт
    num_return_sequences=1,  # Хэдэн өгүүлбэр үүсгэх
    no_repeat_ngram_size=2,  # Үг давхардахгүй байх нөхцөл
    repetition_penalty=2.0,  # Үг давхардахаас сэргийлэх
    top_p=0.92,              # Нээлттэй үгсийн түвшин
    temperature=0.85,        # Бага утга нь илүү болгоомжтой хариу гаргах
    do_sample=True           # Санамсаргүй дээжлэл хийх (текст үүсгэхийн тулд)
)

# Үүсгэсэн текстийг хэвлэх
output_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(output_text)
