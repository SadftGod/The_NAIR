from nicegui import ui
from ui.client.ask import grpc_chat_question
def render():
    async def ask():
        q = await ui.run_javascript('document.getElementById("query_field").value')
        q = q.strip()
        if q:
            response = grpc_chat_question(q)
            if response:
                ui.notify(response)
            else:
                ui.notify("⚠️ No response", type="warning")
        else:
            ui.notify("❗ Query is empty", type="negative")

    ui.element('div').classes("style_square squere_big")
    ui.element('div').classes("style_square squere_little")
    ui.element('div').classes("style_square2 squere_medium")
    ui.element("div")
    with ui.element("div").classes("main_menu"):
        with ui.element("div").classes("menu_container").on("click", lambda e: print("🔥 clicked")):
            ui.element("div").classes("rhombus first_rh")
            ui.element("div").classes("rhombus second_rh")
            ui.element("div").classes("rhombus third_rh")
        ui.element("div").classes("")


        
        with ui.element("main").classes("chat_section"):
            with ui.element("div").classes("swipping_panel"):
                ui.label("a")
            with ui.element("div").classes("chat_container"):
                with ui.element("div").classes("messages"):
                    pass
                with ui.element("div").classes("input_block"):
                    ui.element("input").props('id="query_field"').classes("send_input")


                        

