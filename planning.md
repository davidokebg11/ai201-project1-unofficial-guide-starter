# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain
Freshman survival tips and advice from current and former college students. 
This knowledge is valuable because it's experience-based and honest — students 
share what they wish they had known, which official orientation materials never 
cover. It's hard to find in one place because it's scattered across Reddit 
threads, Quora answers, forums, and student blogs.

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---

## Documents

1. https://www.reddit.com/r/college/comments/tzhzf5/current_college_students_whats_one_underrated_tip/
2. https://www.reddit.com/r/college/comments/km0d5c/15_things_i_wish_i_knew_as_a_freshman/
3. https://www.reddit.com/r/college/comments/vido4b/biggest_advice_you_will_give_to_a_freshman/
4. https://www.reddit.com/r/NCSU/comments/15dd4oq/freshmen_survival_guide/
5. https://www.quora.com/What-are-some-general-college-freshman-tips
6. https://www.quora.com/topic/College-Freshman
7. https://www.quora.com/What-do-freshmen-need-to-know-about-Yale-in-2022
8. https://nxnwlife.com/blog/college-freshman-survival-tips-to-thrive-at-fsu/
9. https://www.theodysseyonline.com/incoming-freshmen-tips
10. https://www.mindfullivingcompany.com/2017/06/09/15-things-people-didnt-tell-you-about-your-first-year-of-college/



<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

I will split documents into chunks of 500 characters with an overlap of 100 
characters. My documents are Reddit comments, Quora answers, and blog posts — 
mostly short paragraphs and bullet points. 500 characters captures one complete 
thought or tip without pulling in unrelated advice. The 100 character overlap 
ensures that if a tip spans two chunks, both chunks still have enough context 
to be found by a search query.

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

1. Q: What should freshmen do during the first week of class?
   A: Attend every class, read the syllabus, introduce yourself to professors.

2. Q: How do students deal with homesickness in college?
   A: Stay connected with family, bring comforting items from home, meet new people.

3. Q: What are tips for managing money as a college freshman?
   A: Make a budget, use student discounts, buy used textbooks, avoid eating out too much.

4. Q: How important is going to office hours?
   A: Very important — professors can clarify material and write recommendation letters.

5. Q: What do students wish they knew before starting college?
   A: Get involved early, don't skip class, use campus resources, manage time well.

I will use the all-MiniLM-L6-v2 embedding model from sentence-transformers. 
It runs locally with no API key or rate limits. I will retrieve the top 5 
chunks per query (k=5). If I were choosing for a production system I would 
consider: OpenAI embeddings for higher accuracy, multilingual models if the 
audience isn't English-only, and cost vs. latency tradeoffs between local 
and API-based models.


<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

1. Reddit and Quora pages may be hard to scrape because they use JavaScript 
   to load content. I may need to copy text manually into .txt files instead 
   of fetching them with code.

2. Some chunks may split a tip in half across a chunk boundary, meaning 
   neither chunk fully captures the advice. The 100 character overlap helps 
   reduce this but may not catch every case.

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

Document Ingestion (.txt files) 
        ↓
Chunking (500 chars, 100 overlap)
        ↓
Embedding (all-MiniLM-L6-v2 via sentence-transformers)
        ↓
Vector Store (ChromaDB)
        ↓
Retrieval (top 5 chunks by semantic similarity)
        ↓
Generation (Groq llama-3.3-70b-versatile, grounded response + source citation)

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

1. Ingestion and chunking code: I will give Claude my Documents section and 
   Chunking Strategy section and ask it to write a script that loads .txt 
   files and splits them into 500 character chunks with 100 character overlap.

2. Embedding and retrieval code: I will give Claude my Retrieval Approach 
   section and ask it to write a function that embeds chunks using 
   all-MiniLM-L6-v2 and stores them in ChromaDB with source metadata.

3. Generation code: I will give Claude my grounding requirement and ask it 
   to write a prompt template that forces the LLM to answer only from 
   retrieved chunks and always cite the source document.

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
