import flet as ft
from chat_page import chat_with_bc

def main(page: ft.Page):
    page.title = "Chat Application"
    page.bgcolor = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=["#e0eafc", "#cfdef3"]
    )

    def show_home(e=None):
        page.clean()
        page.title = "Chat Application"
        page.bgcolor = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#e0eafc", "#cfdef3"]
        )
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Icon(name="chat", color="#2196F3", size=46),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(
                            "Bienvenue sur My Chat",
                            size=32,
                            weight="bold",
                            color="#075e54",
                            text_align="center",
                        ),
                        ft.Text(
                            "Discuter facilement avec votre ERP",
                            size=18,
                            color="#666",
                            italic=True,
                            text_align="center",
                        ),
                        ft.Divider(height=18, color="transparent"),
                        ft.FilledButton(
                            "💬  Chat with BC",
                            on_click=go_to_chat,
                            style=ft.ButtonStyle(
                                bgcolor="#25D366",
                                color="white",
                                shape=ft.RoundedRectangleBorder(radius=28),
                                padding=ft.padding.symmetric(horizontal=25, vertical=14),
                                elevation=3,
                            ),
                            width=240
                        ),
                        ft.Divider(height=10, color="transparent"),
                        ft.FilledButton(
                            "⚡  Advanced chat with BC",
                            on_click=go_to_advanced_chat,
                            style=ft.ButtonStyle(
                                bgcolor="#ececec",
                                color="#2196F3",
                                shape=ft.RoundedRectangleBorder(radius=28),
                                padding=ft.padding.symmetric(horizontal=25, vertical=14),
                                elevation=2,
                            ),
                            width=240
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                width=390,
                padding=32,
                bgcolor="white",
                border_radius=28,
                shadow=ft.BoxShadow(
                    blur_radius=30,
                    spread_radius=1,
                    color="#B0BEC5",
                    offset=ft.Offset(0, 10)
                ),
                alignment=ft.alignment.center,
                expand=True,   # Centrage vertical/horizontal
            )
        )

    def go_to_chat(e=None):
        chat_with_bc(page, show_home)

    def go_to_advanced_chat(e=None):
        page.snack_bar = ft.SnackBar(ft.Text("Fonction à venir !"))
        page.snack_bar.open = True
        page.update()

    show_home()

ft.app(target=main, view=ft.FLET_APP)
