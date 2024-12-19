from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

template = """
Input: 
```
{sentence}
```

You are an AI sentiment classifier agent. 
Your task is to take in a sentence and output the sentiment of the sentence as a valid JSON dictionary. 

The possible sentiments are:

- Satisfied: Sentences expressing satisfaction, agreement, approval, joy, saluting, fulfillment, salutation and a positive outlook on current or future outcomes.

- Dissatisfied: Sentences that communicate disappointment, dissatisfaction, unmet expectations, irritation, or strong displeasure.

- Sarcastic: Sentences that use irony or humor to convey subtle criticism or skepticism, often indicating the opposite of their literal meaning.

- Curious: Sentences that reflect a desire for more information, asking questions, or showing active interest in learning about a subject.

- Neutral: Sentences that present information objectively, without any discernible emotional tone or subjective viewpoint.

- Sad: Sentences that convey sorrow, a sense of loss, or aversion, often in response to unfortunate events or distasteful experiences.

- Profanity: Sentences containing offensive or intense language that may be profane, hostile, or disrespectful.

Reasoning:
1. Identify key phrases or words that might indicate sentiment.
2. Look for tone markers, such as polite or harsh words, emoji, or exclamations. Do not output the tone markers, just analyze them.
3. If mixed languages are used, translate relevant sections mentally to understand the overall meaning.
4. If the message is neither strongly positive nor strongly negative, mark it as neutral.
5. Pay special attention to curse, derogatory and offensive words and mark them as profanity. When assigning profanity, do so cautiously.
6. Be extremely careful as to not wrongly classify commetns as profanity.
7. If you are confused or unsure, translate the sentence to English and find out the sentiment.
8. Consider tone, word choice, and context to make your final judgment.

Provide the final result in a valid JSON dictionary in the following format:

Output format:
"sentiment": <identified_sentiment>

Output:

"""

prompt = PromptTemplate(template=template, input_variables=["sentence"]) 

parser = JsonOutputParser()

llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")
chain = prompt | llm | parser

def get_sentiment(sentence):
  result = chain.invoke({"sentence": sentence})
  
  try:
    sentiment_output = result.get('sentiment', None)
    return sentiment_output
  
  except Exception as e:
    return {"error": str(e)}