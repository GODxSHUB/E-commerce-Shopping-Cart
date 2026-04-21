from flask import Flask, render_template, redirect, url_for, session, request, flash

app = Flask(__name__)
app.secret_key = "pymart-secret-key-2024"

# ── Product catalogue ──────────────────────────────────────────────
PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 1999, "icon": "🎧",
     "desc": "40hr battery, active noise cancellation, studio-grade sound."},
    {"id": 2, "name": "Mechanical Keyboard",  "price": 2499, "icon": "⌨️",
     "desc": "TKL layout, tactile switches, RGB per-key lighting, aluminium frame."},
    {"id": 3, "name": "USB-C Hub 7-in-1",     "price":  899, "icon": "🔌",
     "desc": "4K HDMI, 100W PD, SD/microSD, 3× USB-A. Plug and play."},
    {"id": 4, "name": "Webcam HD 1080p",      "price": 1499, "icon": "📷",
     "desc": "Auto light correction, privacy shutter, wide-angle 90° lens."},
    {"id": 5, "name": "Mouse Pad XL",         "price":  399, "icon": "🖱️",
     "desc": "900×400mm surface, stitched edges, anti-slip rubber base."},
    {"id": 6, "name": "LED Desk Lamp",        "price":  799, "icon": "💡",
     "desc": "Touch dimmer, 3 colour temps, USB charging port, flexible neck."},
]

# ── Helpers ────────────────────────────────────────────────────────
def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart
    session.modified = True

def cart_summary(cart):
    """Return list of items with product details + running total."""
    items = []
    total = 0
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p["id"] == int(pid)), None)
        if product:
            subtotal = product["price"] * qty
            items.append({**product, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return items, total

# ── Routes ─────────────────────────────────────────────────────────
@app.route("/")
def index():
    cart = get_cart()
    cart_count = sum(cart.values())
    return render_template("index.html", products=PRODUCTS, cart_count=cart_count)


@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("index"))

    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    save_cart(cart)
    flash(f"{product['icon']} {product['name']} added to cart!", "success")
    return redirect(url_for("index"))


@app.route("/cart")
def view_cart():
    cart = get_cart()
    items, total = cart_summary(cart)
    cart_count = sum(cart.values())
    return render_template("cart.html", items=items, total=total, cart_count=cart_count)


@app.route("/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    action = request.form.get("action")
    cart = get_cart()
    key = str(product_id)

    if key in cart:
        if action == "increase":
            cart[key] += 1
        elif action == "decrease":
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]

    save_cart(cart)
    return redirect(url_for("view_cart"))


@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    flash("Item removed from cart.", "success")
    return redirect(url_for("view_cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = get_cart()
    items, total = cart_summary(cart)
    cart_count = sum(cart.values())

    if not items:
        flash("Your cart is empty!", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        card_number = request.form.get("card_number", "").replace(" ", "")
        card_name   = request.form.get("card_name", "").strip()
        card_expiry = request.form.get("card_expiry", "").strip()
        card_cvv    = request.form.get("card_cvv", "").strip()

        # ── Validation (Phase 3 requirement) ──
        errors = []
        if len(card_number) != 16 or not card_number.isdigit():
            errors.append("Card number must be exactly 16 digits.")
        if not card_name:
            errors.append("Cardholder name is required.")
        if not card_expiry:
            errors.append("Expiry date is required.")
        if len(card_cvv) != 3 or not card_cvv.isdigit():
            errors.append("CVV must be 3 digits.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("checkout.html", items=items,
                                   total=total, cart_count=cart_count)

        # ── Payment successful — clear cart ──
        save_cart({})
        return render_template("success.html", total=total)

    return render_template("checkout.html", items=items,
                           total=total, cart_count=cart_count)


if __name__ == "__main__":
    app.run(debug=True)
