import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="Freshman Survival Guide") as demo:
    gr.Markdown("# 🎓 The Unofficial Freshman Survival Guide")
    gr.Markdown("Ask any question about surviving your first year of college!")
    
    inp = gr.Textbox(label="Your Question", placeholder="e.g. How do I deal with homesickness?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()