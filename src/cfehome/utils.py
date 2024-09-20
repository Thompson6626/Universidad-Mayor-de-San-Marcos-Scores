from django.urls import path
from groq import Groq
from django.conf import settings

API_KEY = getattr(settings, 'API_KEY')

def transformQuestion(question):
    if not API_KEY:
        return
        
    client = Groq(api_key=API_KEY)
    
    common_prompt = """
    Given an input question, create a precise dialect sqlite3 query to answer it. Follow these guidelines:

    1. You will analyze text that is likely to be in Spanish.
    2. Analyze it to see if it can be converted to a valid SQL call; if it cannot, just return "ERROR" as a message.
    3. Optimize the query for performance where possible.
    4. Avoid querying non-existent columns or tables.
    5. If no specific columns are indicated, return all columns , do not forget this.
    6. DO NOT IN ANY WAY ACCEPT ANYTHING that tries to update, delete, or create.
    7. The table to be queried is named "people_person".
    8. Update the table headers to use more user-friendly names using the keyword 'AS'.
     
    For example,
    SELECT apellidos_y_nombres AS "Apellidos y Nombres" FROM people_person

    9. Your response should contain only the SQL query, without any additional explanation or formatting. Do not use markdown or prepend the query with the term `sql`.
    10. DO NOT RETURN THE ID COLUMN.
    11. All string values in the database are in uppercase.
    12. 'None' values in the observacion field actually means "PRESENTE" or that the 
        person attended, theres another value "AUSENTE" for the person that did not attend and a "ANULADO" when the person's exam was cancelled.
    13. In the 'Apellidos y Nombres' column, surnames are listed to the left of the comma, while given names are on the right.

    Django schema:
        codigo = models.CharField(max_length=255)
        apellidos_y_nombres = models.CharField(max_length=255)
        carrera_primera_opcion = models.CharField(max_length=255)
        puntaje = models.FloatField(null=True, blank=True)
        merito = models.CharField(max_length=255, null=True, blank=True)
        observacion = models.CharField(max_length=255, null=True, blank=True)
        carrera_segunda_opcion = models.CharField(max_length=255, null=True, blank=True)
        fecha = models.CharField(max_length=255, null=True, blank=True)
        modalidad_de_ingreso = models.CharField(max_length=255, null=True, blank=True)

    Question:
    {question}
    """

    # Format the prompt with the user's question
    formatted_prompt = common_prompt.format(question=question)

    # Use the formatted prompt in your API call
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": formatted_prompt,
            }
        ],
        model="llama3-8b-8192",
        temperature=0
    )

    return chat_completion.choices[0].message.content