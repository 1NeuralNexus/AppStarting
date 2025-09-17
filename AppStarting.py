from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.metrics import dp
from kivymd.uix.fitimage import FitImage
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
import random
import json
import smtplib
from email.mime.text import MIMEText

# ---------------- Firebase Firestore ----------------
from firebase_config import db


# ---------------- Email Config ----------------
with open("email_send_detail.json") as f:
    email_conf = json.load(f)

SENDER_EMAIL = email_conf["email"]
SENDER_PASS = email_conf["password"]

OTP_STORE = {}  # temporary store

# ---------------- KV Layout ----------------
KV = """
<WelcomeScreen>:
    name: 'welcome'
    md_bg_color: '#E0BBE4'

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(20)

        MDLabel:
            text: "Welcome\\nto NeuralNexus\\nCommunity"
            font_size: dp(35)
            bold: True
            color: '#1A1A1A'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: self.texture_size[1]
            adaptive_height: True

        FitImage:
            source: 'images/AppStarting1.png'
            size_hint_y: 1

        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            MDRaisedButton:
                id: welcome_next
                text: "Next"
                font_size: dp(18)
                bold: True
                md_bg_color: '#1A1A1A'
                text_color: '#FFFFFF'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                on_release: app.root.current = 'support'
                size_hint_x: 0.8
                height: dp(50)


<SupportScreen>:
    name: 'support'
    md_bg_color: '#FFF7AE'

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(20)

        MDLabel:
            text: "Get support\\nin your\\nnew career"
            font_size: dp(45)
            bold: True
            color: '#1A1A1A'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: self.texture_size[1]
            adaptive_height: True

        FitImage:
            source: 'images/AppStarting2.png'
            size_hint_y: 1

        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            MDRaisedButton:
                id: support_next
                text: "Next"
                font_size: dp(18)
                bold: True
                md_bg_color: '#1A1A1A'
                text_color: '#FFFFFF'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                on_release: app.root.current = 'login'
                size_hint_x: 0.8
                height: dp(50)


<LoginScreen>:
    name: 'login'
    md_bg_color: '#1A1A1A'

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(30)

        MDLabel:
            text: "Hello\\nagain!"
            font_size: dp(45)
            bold: True
            color: '#FFFFFF'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: self.texture_size[1]
            adaptive_height: True

        MDTextField:
            id: user_name_field
            hint_text: "User Name"
            mode: "rectangle"
            line_color_normal: '#505050'
            line_color_focus: '#FFF7AE'
            text_color_normal: '#FFFFFF'
            text_color_focus: '#FFFFFF'
            hint_text_color_normal: '#AAAAAA'
            hint_text_color_focus: '#FFF7AE'
            color_mode: 'custom'
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.9
            current_hint_text_color: '#FFF7AE'

        MDTextField:
            id: password_field
            hint_text: "Password"
            mode: "rectangle"
            password: True
            line_color_normal: '#505050'
            line_color_focus: '#FFF7AE'
            text_color_normal: '#FFFFFF'
            text_color_focus: '#FFFFFF'
            hint_text_color_normal: '#AAAAAA'
            hint_text_color_focus: '#FFF7AE'
            color_mode: 'custom'
            pos_hint: {'center_x': 0.5}
            size_hint_x: 0.9
            current_hint_text_color: '#FFF7AE'

        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            MDRaisedButton:
                id: login_btn
                text: "Log in"
                font_size: dp(18)
                bold: True
                md_bg_color: '#FFF7AE'
                text_color: '#1A1A1A'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                on_release: root.home()
                size_hint_x: 0.9
                height: dp(50)

        MDLabel:
            text: "I don't have an account"
            color: '#FFFFFF'
            halign: 'center'
            font_size: dp(14)
            size_hint_y: None
            height: self.texture_size[1]

        MDRaisedButton:
            id: signup_btn
            text: "Sign Up"
            font_size: dp(18)
            bold: True
            md_bg_color: '#FFF7AE'
            text_color: '#1A1A1A'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: app.root.current = 'Signup'
            size_hint_x: 1
            height: dp(50)


<SignUpPage>:
    name: 'Signup'
    md_bg_color: '#1A1A1A'

    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {'top': 1}

            MDLabel:
                text: "Join With Us\\nLearn New"
                font_size: dp(45)
                bold: True
                color: '#FFFFFF'
                halign: 'center'
                valign: 'top'
                size_hint_y: None
                height: self.texture_size[1]

            MDTextField:
                id: signup_email
                hint_text: 'User Email'
                mode: 'rectangle'
                line_color_normal: '#505050'
                line_color_focus: '#FFF7AE'
                text_color_normal: '#FFFFFF'
                text_color_focus: '#FFFFFF'
                hint_text_color_normal: '#AAAAAA'
                hint_text_color_focus: '#FFF7AE'
                color_mode: 'custom'
                pos_hint: {'center_x': 0.5}
                size_hint_x: 0.9
                current_hint_text_color: '#FFF7AE'

            # Added OTP message label
            MDLabel:
                id: otp_message
                text: ''
                color: (0.2, 0.8, 0.2, 1)  # Green color
                halign: 'center'
                size_hint_y: None
                height: self.texture_size[1]
                adaptive_height: True

            # OTP text field with a "Get OTP" button
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(48)
                spacing: dp(10)
                pos_hint: {'center_x': 0.5}
                size_hint_x: 0.9

                MDTextField:
                    id: otp_field
                    hint_text: 'OTP'
                    mode: 'rectangle'
                    line_color_normal: '#505050'
                    line_color_focus: '#FFF7AE'
                    text_color_normal: '#FFFFFF'
                    text_color_focus: '#FFFFFF'
                    hint_text_color_normal: '#AAAAAA'
                    hint_text_color_focus: '#FFF7AE'
                    color_mode: 'custom'
                    size_hint_x: 0.7
                    current_hint_text_color: '#FFF7AE'

                MDRaisedButton:
                    text: 'Get OTP'
                    md_bg_color: '#FFF7AE'
                    bold: True
                    text_color: '#1A1A1A'
                    size_hint_x: 0.3
                    height: dp(48)
                    on_release: root.send_otp()

            MDTextField:
                id: sign_pass
                hint_text: 'Password'
                mode: 'rectangle'
                line_color_normal: '#505050'
                line_color_focus: '#FFF7AE'
                text_color_normal: '#FFFFFF'
                text_color_focus: '#FFFFFF'
                hint_text_color_normal: '#AAAAAA'
                hint_text_color_focus: '#FFF7AE'
                color_mode: 'custom'
                password: True
                pos_hint: {'center_x': 0.5}
                size_hint_x: 0.9
                current_hint_text_color: '#FFF7AE'

            MDTextField:
                id: User_Name
                hint_text: 'Username'
                mode: 'rectangle'
                line_color_normal: '#505050'
                line_color_focus: '#FFF7AE'
                text_color_normal: '#FFFFFF'
                text_color_focus: '#FFFFFF'
                hint_text_color_normal: '#AAAAAA'
                hint_text_color_focus: '#FFF7AE'
                color_mode: 'custom'
                pos_hint: {'center_x': 0.5}
                size_hint_x: 0.9
                current_hint_text_color: '#FFF7AE'

            MDTextField:
                id: Pin_Num
                hint_text: 'Roll Number'
                mode: 'rectangle'
                line_color_normal: '#505050'
                line_color_focus: '#FFF7AE'
                text_color_normal: '#FFFFFF'
                text_color_focus: '#FFFFFF'
                hint_text_color_normal: '#AAAAAA'
                hint_text_color_focus: '#FFF7AE'
                color_mode: 'custom'
                pos_hint: {'center_x': 0.5}
                size_hint_x: 0.9
                current_hint_text_color: '#FFF7AE'

            MDRaisedButton:
                id: create_user
                text: 'Enjoy Career'
                md_bg_color: '#FFF7AE'
                bold: True
                pos_hint: {'center_x': 0.5}
                font_size: dp(18)
                text_color: '#1A1A1A'
                size_hint_x: 0.9
                height: dp(50)
                on_release: root.verify_otp()

            MDLabel:
                text: 'Note:'
                color: '#FFFFFF'
                font_size: dp(12)
                halign: 'left'
                valign: 'bottom'
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "If you're not a Hindu College student,\\nthen you don't need to fill the roll number text field."
                color: "#888484ff"
                font_size: dp(10)
                halign: 'left'
                valign: 'top'
                size_hint_y: None
                height: self.texture_size[1]
"""


# ---------------- Screens ----------------
class WelcomeScreen(MDScreen):
    pass

class SupportScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    def show_dialog(self, text):
        dialog = MDDialog(
            title="Message",
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda *a: dialog.dismiss())]
        )
        dialog.open()

    def home(self):
        username = self.ids.user_name_field.text.strip()
        password = self.ids.password_field.text.strip()

        if not (username and password):
            self.show_dialog("Enter username and password.")
            return

        try:
            users = (
                db.collection("users")
                .where("username", "==", username)
                .where("password", "==", password)
                .stream()
            )

            if any(users):
                self.show_dialog("Login successful!")
                self.manager.current = 'MainPage'
            else:
                self.show_dialog("Invalid credentials.")
        except Exception as e:
            self.show_dialog(f"Database error: {e}")


class SignUpPage(MDScreen):
    def show_dialog(self, text):
        dialog = MDDialog(
            title="Message",
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda *a: dialog.dismiss())]
        )
        dialog.open()

    def send_otp(self):
        email = self.ids.signup_email.text.strip()
        if not email:
            self.show_dialog("Please enter your email.")
            return

        users = db.collection("users").where("email", "==", email).stream()
        if any(users):
            self.show_dialog("Email already registered. Please login.")
            return

        otp = str(random.randint(100000, 999999))
        OTP_STORE[email] = otp

        try:
            msg = MIMEText(f"""
                           <!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EMAIL OTP FROM NEURALNEXUS</title>
</head>

<body style="margin:0; padding:0; font-family: Arial, Helvetica, sans-serif; background-color:#f4f4f4;">

  <!-- Outer Container -->
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f4f4f4; padding:30px 0;">
    <tr>
      <td align="center">

        <!-- Main Card -->
        <table width="600" border="0" cellspacing="0" cellpadding="20" 
               style="background-color:#ffffff; border-radius:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1);">
          <tr>
            <td align="center" style="background-color:#ffeb3b; border-radius:10px 10px 0 0; padding:25px;">
              <h1 style="margin:0; font-size:32px; font-weight:bold; color:#b97902; letter-spacing:2px;">
                NEURALNEXUS OTP
              </h1>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td align="left" style="font-size:20px; color:#333; padding-bottom:0;">
              <strong>Hi,</strong>
            </td>
          </tr>

          <!-- Message -->
          <tr>
            <td align="left" style="font-size:16px; color:#555; line-height:1.6;">
              Welcome to <strong>NeuralNexus</strong>!  
              <br><br>
              Your One-Time Password (OTP) is given below. Please use it to complete your account creation securely.
              <br><br>
              <strong style="display:block; text-align:center; font-size:26px; letter-spacing:6px; 
                             background-color:#fafafa; padding:15px; margin:20px 0; border:2px dashed #b97902; 
                             border-radius:8px; color:#b97902;">
                {otp}
              </strong>

              Our app includes features to support your daily college life:  
              <ul style="margin:10px 0; padding-left:20px; color:#333; font-size:15px;">
                <li>Event posts & updates</li>
                <li>Attendance and marks checking</li>
                <li>AI-integrated compiler & chatbot</li>
                <li>Programming tutorials</li>
                <li>Showcasing your friends' innovations</li>
              </ul>

              <p style="margin-top:20px; font-size:16px; color:#444;">
                Together, let’s move forward with innovation and learning.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="font-size:14px; color:#777; border-top:1px solid #eee; padding-top:15px;">
              With regards, <br>
              <strong>The NeuralNexus Team</strong>
            </td>
          </tr>

        </table>
        <!-- End Card -->

      </td>
    </tr>
  </table>

</body>
</html>

                           
                           
                           """,'html')
            msg["Subject"] = "NeuralNexus OTP"
            msg["From"] = SENDER_EMAIL
            msg["To"] = email

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            server.quit()

            self.ids.otp_message.text = "OTP Sent!"
            Clock.schedule_once(self.clear_otp_message, 5)
        except Exception as e:
            self.show_dialog(f"Failed to send OTP: {e}")

    def clear_otp_message(self, dt):
        self.ids.otp_message.text = ''

    def verify_otp(self):
        email = self.ids.signup_email.text.strip()
        entered_otp = self.ids.otp_field.text.strip()
        username = self.ids.User_Name.text.strip()
        password = self.ids.sign_pass.text.strip()
        roll_number = self.ids.Pin_Num.text.strip()

        if not (email and entered_otp and username and password):
            self.show_dialog("Fill all required fields.")
            return

        stored_otp = OTP_STORE.get(email)
        if stored_otp and stored_otp == entered_otp:
            user_data = {
                "username": username,
                "email": email,
                "password": password,  # ⚠️ hash in production
                "roll_number": roll_number
            }
            try:
                db.collection("users").add(user_data)
                OTP_STORE.pop(email)
                self.show_dialog("Signup successful! You can now log in.")
                self.manager.current = 'login'
            except Exception as e:
                self.show_dialog(f"Failed to save user: {e}")
        else:
            self.show_dialog("Invalid OTP. Try again.")

"""# ---------------- App ----------------
class HYUApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        Builder.load_string(KV)
        sm = MDScreenManager()
        sm.add_widget(WelcomeScreen())
        sm.add_widget(SupportScreen())
        sm.add_widget(LoginScreen())
        sm.add_widget(SignUpPage())
        return sm

if __name__ == '__main__':
    HYUApp().run()
"""