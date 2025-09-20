from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from openai import OpenAI

# -----------------------
API_KEY = "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"
# -----------------------

client = OpenAI(api_key=API_KEY)

system_message = (
    "You are a friendly sex and health education teacher. "
    "You must give correct, safe, and educational information only. "
    "Never prescribe or suggest the name of any medicine. "
    "Instead, explain possible reasons, preventive steps, and when to see a doctor. "
    "Always reply in the same language as the user, keeping answers simple and clear. "
    "If a question is unrelated to sex or health, politely say: "
    "'I can only answer questions related to sex education and health.'"
)

Window.softinput_mode = "pan"


class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Chat history
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_history = GridLayout(cols=1, spacing=30, size_hint_y=None, padding=30)
        self.chat_history.bind(minimum_height=self.chat_history.setter("height"))
        self.scroll.add_widget(self.chat_history)
        self.add_widget(self.scroll)

        # Input area anchored at bottom
        input_anchor = AnchorLayout(anchor_y="bottom", size_hint=(1, 0.2))
        input_area = BoxLayout(size_hint=(1, None), height=200, spacing=20, padding=[25, 25])

        self.user_input = TextInput(
            hint_text="Type your question...",
            multiline=False,
            font_size=60,          # 5x bada input text
            size_hint_x=0.7,
            padding=(30, 40)
        )

        send_btn = Button(
            text="Send",
            font_size=55,          # bada button text
            size_hint_x=0.3
        )
        send_btn.bind(on_press=self.send_message)

        input_area.add_widget(self.user_input)
        input_area.add_widget(send_btn)
        input_anchor.add_widget(input_area)

        self.add_widget(input_anchor)

    def add_message(self, sender, text):
        msg = Label(
            text=f"[b]{sender}:[/b] {text}",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="top",
            font_size=55          # bada reply text
        )
        msg.bind(
            width=lambda s, w: s.setter("text_size")(s, (w, None)),
            texture_size=lambda s, t: s.setter("height")(s, t[1])
        )
        self.chat_history.add_widget(msg)
        self.scroll.scroll_to(msg)

    def send_message(self, instance):
        user_text = self.user_input.text.strip()
        if not user_text:
            return

        self.add_message("You", user_text)
        self.user_input.text = ""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_text}
                ],
                max_tokens=400
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Error: {str(e)}"

        self.add_message("Bot", reply)


class SexEdApp(App):
    def build(self):
        return ChatScreen()


if __name__ == "__main__":
    SexEdApp().run()