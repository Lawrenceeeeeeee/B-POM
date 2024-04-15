import gradio as gr

def greet(name, 强度):
    return "Hello, " + name + "!" * int(强度)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()
