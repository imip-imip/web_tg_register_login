from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import sqlite3


def generate_pdf(username, favorite_anime, favorite_movie):
    pdf_file = f"{username}'s resume.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    c.setFont('Arial', 12)

    c.drawString(100, 700, f"Username: {username}")
    c.drawString(100, 680, f"Favorite Anime: {favorite_anime}")
    c.drawString(100, 660, f"Favorite Movie: {favorite_movie}")

    c.showPage()
    c.save()


def send_pdf(bot, chat_id, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, anime, film FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()

    if user:
        username, favorite_anime, favorite_movie = user
        generate_pdf(username, favorite_anime, favorite_movie)
        pdf_file = f"{username}'s resume.pdf"
        with open(pdf_file, 'rb') as f:
            bot.send_document(chat_id, f)
    else:
        bot.send_message(chat_id, "User not found in the database.")
