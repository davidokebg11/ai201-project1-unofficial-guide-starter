# The Unofficial Freshman Survival Guide

A RAG (Retrieval-Augmented Generation) system that answers questions about 
surviving your first year of college using real student-generated advice.

## Domain
Freshman survival tips and advice from current and former college students. 
This knowledge is valuable because it's experience-based and honest — students 
share what they wish they had known, which official orientation materials never 
cover. It's hard to find in one place because it's scattered across Reddit 
threads, Quora answers, forums, and student blogs.

## Document Sources
1. reddit_underrated_tips.txt - reddit.com/r/college (underrated tips thread)
2. reddit_15_things.txt - reddit.com/r/college (15 things I wish I knew)
3. reddit_biggest_advice.txt - reddit.com/r/college (biggest advice for freshmen)
4. reddit_ncsu_guide.txt - reddit.com/r/NCSU (freshman survival guide)
5. quora_general_tips.txt - quora.com (general college freshman tips)
6. quora_topic_page.txt - quora.com/topic/College-Freshman
7. quora_yale_tips.txt - quora.com (Yale freshman tips)
8. fsu_survival_tips.txt - nxnwlife.com (FSU survival tips)
9. odyssey_freshman_survival_tips.txt - theodysseyonline.com
10. mindful_living_freshman_tips.txt - mindfullivingcompany.com

## Chunking Strategy
Documents are split into chunks of 500 characters with 100 character overlap. 
My documents are Reddit comments, Quora answers, and blog posts — mostly short 
paragraphs and bullet points. 500 characters captures one complete thought or 
tip without pulling in unrelated advice. The 100 character overlap ensures that 
if a tip spans two chunks, both chunks still have enough context to be found.
Total chunks produced: 104

## Sample Chunks

**Chunk 1 (source: reddit_underrated_tips.txt):**
"SLEEP. DO NOT UNDERESTIMATE HOW MUCH YOUR BODY NEEDS SLEEP. As long as you 
have a consistent sleep schedule and sleep for 8-10 hours a day you will be ok."

**Chunk 2 (source: odyssey_freshman_survival_tips.txt):**
"Get a planner. A planner will literally save your life in college. It doesn't 
have to be a super fancy and expensive planner. Get one that works for you."

**Chunk 3 (source: fsu_survival_tips.txt):**
"Office hours are one of the most underutilized resources available to college 
students. Professors hold these dedicated times to help students with coursework, 
clarify material, or give guidance on projects."

**Chunk 4 (source: reddit_ncsu_guide.txt):**
"Get a study group — they do help. But make sure to actually study. Studying 
with close friends is usually not the best idea since you'll goof off."

**Chunk 5 (source: mindful_living_freshman_tips.txt):**
"Don't force friendships. There's hundreds and thousands of other students on 
campus. You have a lot of people to meet, so just ease into it."

## Embedding Model
Model used: all-MiniLM-L6-v2 via sentence-transformers. This model runs 
locally with no API key or rate limits. For a production system I would 
consider: OpenAI embeddings for higher accuracy on nuanced queries, 
multilingual models if the audience includes non-English speakers, and 
the tradeoff between local models (free, private, slower) vs API models 
(cost per call, faster, higher accuracy).

## Retrieval Test Results

**Query 1: "How do I deal with homesickness in college?"**
Top chunks returned from: mindful_living_freshman_tips.txt, fsu_survival_tips.txt
These chunks are relevant because they directly discuss missing home and 
strategies like calling family and bringing comforting items from home.

**Query 2: "How important is going to office hours?"**
Top chunks returned from: reddit_underrated_tips.txt, fsu_survival_tips.txt
These chunks are relevant because they specifically discuss office hours, 
professor relationships, and letters of recommendation.

**Query 3: "What are tips for managing money in college?"**
Top chunks returned from: fsu_survival_tips.txt, reddit_15_things.txt
These chunks are relevant because they cover budgeting, student discounts, 
and textbook savings strategies.

## Grounded Generation
Grounding is enforced through the system prompt in query.py. The prompt 
explicitly instructs the LLM: "Answer the question using ONLY the information 
provided in the documents below. If the documents don't contain enough 
information to answer, say 'I don't have enough information on that.'"
Source attribution is added programmatically by extracting source filenames 
from ChromaDB metadata after retrieval.

## Example Responses

**Example 1 - Question: "How do students deal with homesickness in college?"**
Answer: "According to the document 'Dealing with Homesickness', students can 
deal with homesickness in college by staying connected with family through 
regular calls or video chats, and by bringing a few comforting items from home, 
like photos or favorite snacks, to make their dorm or apartment feel more familiar."
Sources: mindful_living_freshman_tips.txt, fsu_survival_tips.txt, quora_topic_page.txt

**Example 2 - Question: "How important is going to office hours?"**
Answer: "According to the documents, going to office hours is important because 
it allows you to build professional relationships with your professors, which can 
lead to helpful advice and later on, recommendations."
Sources: reddit_underrated_tips.txt, fsu_survival_tips.txt, reddit_biggest_advice.txt

**Out-of-scope query: "What is the best programming language to learn?"**
Answer: "I don't have enough information on that."

## Query Interface
The interface is a Gradio web app running at http://localhost:7860.
Input: A text box labeled "Your Question" where the user types their question.
Output: An "Answer" text box with the grounded response, and a "Sources" text 
box listing which documents the answer was pulled from.
The user types a question and clicks the orange "Ask" button or presses Enter.

**Sample interaction:**
Question: "What should freshmen do during the first week of class?"
Answer: "During the first week of class, freshmen should: visit classrooms 
before the first day to avoid getting lost, start a consistent schedule of 
waking up, studying, exercising and sleeping, begin staying on top of coursework 
by making a calendar with all due dates, and use academic resources such as 
professors' office hours."
Sources: quora_topic_page.txt, reddit_biggest_advice.txt, quora_general_tips.txt

## Evaluation Report

| # | Question | Expected Answer | System Response | Accuracy |
|---|---|---|---|---|
| 1 | What should freshmen do during the first week of class? | Attend class, read syllabus, introduce yourself to professors | Visit classrooms early, make a schedule, use office hours, stay on top of coursework | Accurate |
| 2 | How do students deal with homesickness in college? | Stay connected with family, bring comforting items from home | Stay connected via calls/video chat, bring photos or snacks from home | Accurate |
| 3 | What are tips for managing money as a college freshman? | Budget, use student discounts, buy used textbooks | Use student discounts, buy used textbooks, cook at home, apply for scholarships | Accurate |
| 4 | How important is going to office hours? | Very important for grades and recommendation letters | Very important for professor relationships, advice, and recommendation letters | Accurate |
| 5 | What do students wish they knew before starting college? | Get involved early, manage time well, use campus resources | Hard to adjust routine, importance of mental health, college is not like high school | Partially Accurate |

## Failure Case
Question 5 ("What do students wish they knew before starting college?") returned 
a partially accurate answer. The question is very broad, which means the 
retrieval pulled chunks about general adjustment and mental health rather than 
the full range of advice students wish they had known. The relevant information 
was spread across many chunks from many documents, so no single retrieved chunk 
captured everything. A better chunking strategy for this type of broad question 
might be to use larger chunks (800-1000 characters) to capture more complete 
thoughts per chunk.

## Spec Reflection
The spec helped by forcing me to decide on chunk size and overlap before writing 
any code. Having those numbers (500 chars, 100 overlap) already decided meant I 
could write the chunking code confidently without second-guessing it mid-build.

One way implementation diverged from the spec: I originally planned to scrape 
documents directly from URLs, but Reddit and Quora block automated scraping. I 
had to manually copy text into .txt files instead, which was more reliable and 
produced cleaner text anyway.

## AI Usage
1. I used Claude to generate the ingest.py script. I provided my chunking 
strategy (500 char chunks, 100 char overlap) and document structure (.txt files). 
Claude generated the load_documents() and chunk_text() functions. I reviewed 
the code and confirmed it matched my spec before running it.

2. I used Claude to generate the query.py script. I provided my grounding 
requirement (answers from retrieved context only, with source attribution) and 
the pipeline structure. Claude generated the ask() function. I had to override 
one thing: the original code didn't load the .env file, so I added the 
python-dotenv fix to make the Groq API key load correctly.