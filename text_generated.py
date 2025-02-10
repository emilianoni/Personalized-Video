from groq import Groq

# Initialize the Groq client with your API key
api_key = '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'
client = Groq(api_key=api_key)

# Define the prompt template
prompt_text = """
Kamu adalah pakar pemasaran yang membantu klien di industri keuangan. 
Berdasarkan pola merchant yang diberikan, buatlah ringkasan yang ramah dan menarik tentang tempat-tempat seperti apa transaksi yang sering dia lakukan yang ditujukan langsung kepada pelanggan.
Mulailah respons dengan "Haloo," dan jelaskan kebiasaan transaksi mereka dengan nada percakapan yang relevan pakai sapaan 'kamu'.
Tulis hingga 2 kalimat pendek agar menarik dan mudah dipahami.

Data input: {user_query}
"""

prompt_category = """
Kamu adalah pakar pemasaran yang membantu klien di industri keuangan. 
Kamu akan diberikan beberapa kalimat berisi deskripsi singkat nasabah mengenai dirinya dan transaksi yang sering dilakukan.
Berdasarkan beberapa kalimat deskripsi tersebut, kategorikan nasabah tersebut ke salah satu kategori-kategori berikut.
- belanja
- makanan & minuman
- hiburan
- lainnya

Hanya berikan output kategorinya saja tanpa kata-kata lainnya. Hanya berikan 1 kategori saja untuk 1 user.

Data input: {user_query}
"""

def get_response_text(user_input):
    """
    Generate a response from the Groq model based on the user input.

    :param user_input: The user's query to process
    :return: Generated response as a string
    """
    final_prompt = prompt_text.format(user_query=user_input)

    # Generate response from the model
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": final_prompt},
        ],
        model="llama-3.3-70b-versatile",
    )

    return response.choices[0].message.content

def get_response_category(user_input):
    """
    Generate a response from the Groq model based on the user input.

    :param user_input: The user's query to process
    :return: Generated response as a string
    """
    final_prompt = prompt_category.format(user_query=user_input)

    # Generate response from the model
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": final_prompt},
        ],
        model="llama-3.3-70b-versatile",
    )

    return response.choices[0].message.content

