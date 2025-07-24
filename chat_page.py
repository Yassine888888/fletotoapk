import flet as ft
import requests
from requests_ntlm import HttpNtlmAuth
import json

WHATSAPP_GREEN = "#25D366"
WHATSAPP_LIGHT = "#ECE5DD"

def chat_with_bc(page: ft.Page, go_home):
    page.clean()
    page.title = "Chat with BC"
    page.bgcolor = "#ece5dd"
    page.vertical_alignment = ft.MainAxisAlignment.END

    messages = ft.Column(expand=True, scroll="always")

    input_box = ft.TextField(
        hint_text="Écris un message…",
        expand=True,
        border_radius=30,
        filled=True,
        bgcolor="#fff",
        content_padding=ft.padding.symmetric(horizontal=18, vertical=12),
        autofocus=True,
    )

    def get_bubble_width():
        return min(page.width * 0.75, 430)

    def create_bubble(text, is_user=True):
        color = WHATSAPP_GREEN if is_user else "#fff"
        align = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        border_radius = ft.border_radius.only(
            top_left=20,
            top_right=20,
            bottom_left=20 if is_user else 4,
            bottom_right=4 if is_user else 20
        )
        return ft.Row(
            [
                ft.Container(
                    ft.Text(text, color="black", size=16, selectable=True),
                    bgcolor=color,
                    border_radius=border_radius,
                    padding=5,
                    margin=5,
                    shadow=ft.BoxShadow(blur_radius=4, color="#BDBDBD", offset=ft.Offset(0, 2)),
                    width=get_bubble_width(),
                )
            ],
            alignment=align,
        )

    def send_message(e):
        msg = input_box.value.strip()
        if msg:
            messages.controls.append(create_bubble(msg, is_user=True))
            page.update()
            input_box.value = ""
            page.update()

            url = "http://197.13.22.3:7048/SMART/ODataV4/ODATA_TestOdata?company=IRPP2"
            auth = HttpNtlmAuth("YMI", "b2m-IT@2024")
            headers = {"Content-Type": "application/json"}
            data = {"messageOData": msg}
            try:
                r = requests.post(url, headers=headers, data=json.dumps(data), auth=auth, timeout=100)
                api_response = r.json().get("value") if r.status_code == 200 else f"Erreur API {r.status_code}: {r.text}"
            except Exception as ex:
                api_response = f"Erreur de connexion: {ex}"

            messages.controls.append(create_bubble(api_response, is_user=False))
            page.update()
            page.scroll_to("end")

    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def handle_image_upload(e):
        if file_picker.result and file_picker.result.files:
            file_path = file_picker.result.files[0].path
            api_key = 'K88536716788957'  # Mets ta clé API OCR.Space ici !
            language = 'fre'
            isOverlayRequired = False

            payload = {
                'isOverlayRequired': isOverlayRequired,
                'apikey': api_key,
                'language': language,
                'iscreatesearchablepdf': False,
                'issearchablepdfhidetextlayer': False
            }

            with open(file_path, 'rb') as f:
                r = requests.post(
                    'https://api.ocr.space/parse/image',
                    files={'filename': f},
                    data=payload,
                )

            result = r.json()
            if result.get('IsErroredOnProcessing'):
                error_msg = result.get('ErrorMessage', 'Erreur lors du traitement OCR')
                page.snack_bar = ft.SnackBar(ft.Text(f"Erreur OCR: {error_msg}"))
                page.snack_bar.open = True
                page.update()
            else:
                try:
                    text = result['ParsedResults'][0]['ParsedText'].strip()
                    text = text.replace('\n', ' ').replace('\r', ' ')  # une seule ligne
                    if text:
                        input_box.value = text
                        send_message(None)
                    else:
                        page.snack_bar = ft.SnackBar(ft.Text("Aucun texte reconnu dans l’image."))
                        page.snack_bar.open = True
                        page.update()
                except Exception as e:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Erreur extraction texte: {e}"))
                    page.snack_bar.open = True
                    page.update()

    file_picker.on_result = handle_image_upload

    upload_btn = ft.IconButton(
        icon="image",
        tooltip="Uploader une image et extraire le texte",
        on_click=lambda e: file_picker.pick_files(
            dialog_title="Choisissez une image",
            allowed_extensions=["png", "jpg", "jpeg"],
            allow_multiple=False,
        ),
    )

    send_btn = ft.FilledButton(
        "Envoyer",
        on_click=send_message,
        style=ft.ButtonStyle(bgcolor=WHATSAPP_GREEN, color="white", shape=ft.RoundedRectangleBorder(radius=22))
    )
    back_btn = ft.TextButton("← Retour", on_click=go_home)

    header = ft.Container(
        ft.Row([
            back_btn,
            ft.Text("Chat with BC", size=20, weight="bold", color="white"),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor="#075e54",
        border_radius=ft.border_radius.only(top_left=10, top_right=10),
    )

    page.add(
        header,
        ft.Container(messages, expand=True, padding=10, bgcolor="#ece5dd", border_radius=10),
        ft.Row([
            upload_btn,
            ft.Container(input_box, padding=6, expand=True),
            send_btn
        ], alignment=ft.MainAxisAlignment.CENTER),
    )

    page.on_resize = lambda e: input_box.focus()
