from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "sheetal_readymade_key"

# --- FINAL CONFIGURATION ---
DB_NAME = "sheetal_final.db"  # Naya Database (Final Fix)
TABLE_NAME = "final_products"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Purana table hatao taaki error na aaye
    c.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}") 

    # Naya Table Banao
    c.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, image TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT, total_price INTEGER, items TEXT, status TEXT)")
    
    # --- FINAL PRODUCT LIST (Tested Links) ---
    products = [
        # 1. Levis Trucker Jacket (Classic Blue)
        ("Levis Trucker Jacket", 3500, "https://images.unsplash.com/photo-1605908502724-9093a79a1b39?q=80&w=600&auto=format&fit=crop"),
        
        # 2. Tommy Hilfiger Shirt (Formal White/Blue)
        ("Tommy Hilfiger Shirt", 2200, "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?q=80&w=600&auto=format&fit=crop"),
        
        # 3. Raymond Formal Suit (Professional)
        ("Raymond Formal Suit", 8000, "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?q=80&w=600&auto=format&fit=crop"),
        
        # 4. Adidas Hoodie (Black Streetwear)
        ("Adidas Originals Hoodie", 4500, "https://images.unsplash.com/photo-1556906781-9a412961d289?q=80&w=600&auto=format&fit=crop"),

        # 5. Manyavar Wedding Kurta (Golden Sherwani - NEW LINK)
        ("Manyavar Wedding Kurta", 5500, "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0?q=80&w=600&auto=format&fit=crop"),
        
        # 6. Sabyasachi Royal Saree (Red Traditional)
        ("Sabyasachi Royal Saree", 12000, "https://images.unsplash.com/photo-1610030469983-98e550d6193c?q=80&w=600&auto=format&fit=crop"),

        # 7. Allen Solly Junior (Kids)
        ("Allen Solly Junior", 1500, "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?q=80&w=600&auto=format&fit=crop")
    ]
    
    c.executemany(f"INSERT INTO {TABLE_NAME} (name, price, image) VALUES (?, ?, ?)", products)
    conn.commit()
    conn.close()
    print("✅ SAB FIX HO GAYA! PHOTOS LOADED.")

# App start hote hi Database Load
init_db()

@app.route("/")
def home():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"SELECT * FROM {TABLE_NAME}")
    products = c.fetchall()
    conn.close()
    return render_template("index.html", products=products, cart_count=len(session.get("cart", [])))

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "cart" not in session: session["cart"] = []
    cart = session["cart"]
    cart.append(product_id)
    session["cart"] = cart
    return redirect(url_for("home"))

@app.route("/cart")
def view_cart():
    if "cart" not in session or not session["cart"]:
        return render_template("cart.html", cart_items=[], total=0)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    placeholders = ",".join("?" for _ in session["cart"])
    c.execute(f"SELECT * FROM {TABLE_NAME} WHERE id IN ({placeholders})", session["cart"])
    cart_items = c.fetchall()
    conn.close()
    return render_template("cart.html", cart_items=cart_items, total=sum(item[2] for item in cart_items))

@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("home"))

@app.route("/checkout")
def checkout():
    if "cart" not in session or not session["cart"]: return redirect(url_for("home"))
    order_id = "ORD-" + str(random.randint(10000, 99999))
    session.pop("cart", None)
    return render_template("success.html", order_id=order_id, amount="Paid")

if __name__ == "__main__":
    # Final Port 5006 - Taaki Browser purana cache na uthaye
    app.run(debug=True, port=5006)