import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- Image directory setup ---
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# --- Database Setup ---
conn = sqlite3.connect('library.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL,
        added_on TEXT NOT NULL,
        image_path TEXT
    )
''')
conn.commit()

# --- Function Definitions ---
def add_book(title, author, genre, year, image_path=None):
    c.execute('INSERT INTO books (title, author, genre, year, added_on, image_path) VALUES (?, ?, ?, ?, ?, ?)',
              (title, author, genre, year, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), image_path))
    conn.commit()

def view_books():
    c.execute('SELECT * FROM books')
    return c.fetchall()

def delete_book(book_id):
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()

def search_books(keyword):
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?",
              ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    return c.fetchall()

# --- Page Config ---
st.set_page_config(page_title="📚 Library Manager", layout="wide")

# --- App Header ---
st.markdown("""
    <div style="text-align:center;">
        <h1 style='color:#4B8BBE;'>📚 Library Management System</h1>
        <p style='font-size:18px;'>A simple and elegant app to manage your books 📖</p>
    </div>
""", unsafe_allow_html=True)

# --- Navigation ---
menu = ["➕ Add Book", "📖 View All", "🔍 Search", "❌ Delete Book"]
choice = st.sidebar.radio("Navigate", menu)

# --- Add Book ---
if choice == "➕ Add Book":
    with st.form("add_form"):
        st.subheader("Add a New Book")
        title = st.text_input("📕 Title")
        author = st.text_input("✍️ Author")
        genre = st.selectbox("🏷️ Genre", ["Fiction", "Non-Fiction", "Science", "Fantasy", "Biography", "Other"])
        year = st.number_input("📅 Year", min_value=1000, max_value=2050, step=1)
        image_file = st.file_uploader("🖼️ Upload Book Cover", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("✅ Add Book")
        
        if submitted:
            if title and author and year:
                image_path = None
                if image_file is not None:
                    image_path = os.path.join(IMAGE_DIR, f"{title}_{datetime.now().timestamp()}.png")
                    with open(image_path, "wb") as f:
                        f.write(image_file.read())
                add_book(title, author, genre, year, image_path)
                st.success(f"✅ '{title}' by {author} added!")
            else:
                st.warning("⚠️ Please fill in all the fields.")

# --- View All Books ---
elif choice == "📖 View All":
    st.subheader("📚 All Books")
    books = view_books()
    if books:
        for b in books:
            col1, col2 = st.columns([1, 4])
            with col1:
                if b[6] and os.path.exists(b[6]):
                    st.image(b[6], width=120)
                else:
                    st.image("https://via.placeholder.com/120x160?text=No+Cover", width=120)
            with col2:
                st.markdown(f"""
                    <div style='border:1px solid #ddd; border-radius:10px; padding:10px; margin-bottom:10px; background-color:#f9f9f9;'>
                        <strong>{b[1]}</strong> by {b[2]}<br>
                        <em>Genre:</em> {b[3]} | <em>Year:</em> {b[4]} | <em>Added on:</em> {b[5]}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No books found.")

# --- Search Books ---
elif choice == "🔍 Search":
    st.subheader("🔎 Search Books")
    keyword = st.text_input("Enter a title, author or genre:")
    if st.button("Search"):
        results = search_books(keyword)
        if results:
            for r in results:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if r[6] and os.path.exists(r[6]):
                        st.image(r[6], width=120)
                    else:
                        st.image("https://via.placeholder.com/120x160?text=No+Cover", width=120)
                with col2:
                    st.markdown(f"""
                        <div style='border:1px solid #e3e3e3; border-radius:8px; padding:10px; background-color:#eef6fb;'>
                            <strong>{r[1]}</strong> by {r[2]} <br>
                            <em>{r[3]}</em> | {r[4]} | Added: {r[5]}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("🔍 No matching books found.")

# --- Delete Book ---
elif choice == "❌ Delete Book":
    st.subheader("🗑️ Delete Book")
    books = view_books()
    if books:
        book_options = {f"{b[1]} by {b[2]}": b[0] for b in books}
        selected = st.selectbox("Select a book to delete", list(book_options.keys()))
        if st.button("❌ Delete"):
            delete_book(book_options[selected])
            st.success(f"Deleted '{selected}' from the library.")
    else:
        st.info("No books available to delete.")
