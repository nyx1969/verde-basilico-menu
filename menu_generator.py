from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
import webbrowser
import os
import threading
import time
import json

app = Flask(__name__)

# File per salvare i piatti
MENU_FILE = 'piatti.json'

def load_piatti():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'antipasti': [
            "Insalata di formentino",
            "Insalata mista",
            "Insalata Caprese",
            "Insalata con Tonno",
            "Salmone affumicato",
            "Insalata belga gratinata allo Zola",
            "Finocchi gratinati",
            "Carpaccio di manzo",
            "Tacchino Tonnato",
            "Antipasto Ticinese",
            "Uova ripiene",
            "Torta salata"
        ],
        'zuppe_e_primi': [
            "Minestrone di verdure",
            "Pasta e Fagioli",
            "Pasta e ceci",
            "Vellutata di piselli",
            "Vichyssoise porri e patate",
            "Minestra di patate",
            "vellutata di broccoli",
            "Vellutata di Carote",
            "Crema di Zucca",
            "Crema di asparagi",
            "Zuppa Griglionese",
            "Zuppa di cipolle",
            "Pasta al pomodoro",
            "Pasta alla carbonara",
            "Pasta alla Amatriciana",
            "Penne ai funghi",
            "Ravioli ricotta e spinaci",
            "Tortellini in brodo",
            "Lasagne alla Bolognese",
            "Lasagne al Pesto",
            "Cannelloni",
            "Crespelle ricotta e e spinaci",
            "Risotto alla milanese",
            "Risotto ai porcini",
            "Risotto agli asparagi",
            "Riso alla Cantonese",
            "Insalata di riso"
        ],
        'secondi': [
            "Arrosto di Maiale",
            "Brasato di Manzo",
            "Spezzatino di Manzo",
            "Pollo alla Zurighese",
            "Pollo al Curry e latte di Cocco",
            "Pollo al limone",
            "Tacchino alla pizzaiola",
            "Tacchino impanato",
            "Involtino di Tacchino",
            "Pollo Arrosto",
            "Polpettone di manzo",
            "Polpettone di Faraona",
            "Bistecca di Maiale",
            "Roastbeef di manzo",
            "Carpaccio di manzo",
            "Polpette di manzo",
            "Hamburger di Manzo",
            "Hamburger di Pollo",
            "Scaloppine al vino bianco",
            "Luganiga arrosto",
            "Bratwurst vitello",
            "Bratwurst di pollo",
            "Bratwurst di maiale",
            "Salamelle arrosto"
        ],
        'contorni': [
            "Patate al forno",
            "Patate Mantecate al prezzemolo",
            "Gratin Patate",
            "Patate al vapore",
            "Rösti di patate",
            "Purea di patate",
            "Ratatouille di verdure",
            "Spinaci",
            "Piselli"
        ]
    }

def save_piatti(piatti):
    with open(MENU_FILE, 'w', encoding='utf-8') as f:
        json.dump(piatti, f, ensure_ascii=False, indent=4)

# Inizializza i piatti dal file se esiste
piatti = load_piatti()

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

def create_pdf(menu_settimanale):
    pdf_path = "menu_settimanale.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Sfondo colore verde chiaro
    c.setFillColor(colors.Color(0.9, 1, 0.9))
    c.rect(0, 0, width, height, fill=True)
    
    # Titolo principale
    c.setFillColor(colors.Color(0.17, 0.33, 0.19))  # Verde scuro
    c.setFont("Helvetica-Bold", 36)
    c.drawString(width/2 - 150, height - 80, "Verde Basilico")
    
    # Sottotitolo
    c.setFont("Helvetica-Oblique", 24)
    c.drawString(width/2 - 100, height - 120, "Menu della Settimana")
    
    # Linea decorativa
    c.setStrokeColor(colors.Color(0.17, 0.33, 0.19))
    c.setLineWidth(2)
    c.line(50, height - 140, width - 50, height - 140)

    # Aggiungi i menu giornalieri
    y_position = height - 180
    for giorno, piatti in menu_settimanale.items():
        if not any(piatti.values()):  # Salta i giorni senza piatti selezionati
            continue
            
        # Giorno della settimana
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, y_position, giorno)
        y_position -= 25

        # Piatti del giorno
        c.setFont("Helvetica", 14)
        for tipo, piatto in piatti.items():
            if piatto:  # Mostra solo i piatti selezionati
                # Tipo di piatto in corsivo
                c.setFont("Helvetica-Oblique", 12)
                c.drawString(70, y_position, f"{tipo}:")
                # Nome del piatto in normale
                c.setFont("Helvetica", 14)
                c.drawString(140, y_position, piatto)
                y_position -= 20
        
        # Linea decorativa tra i giorni
        c.setLineWidth(1)
        c.line(70, y_position - 5, width - 70, y_position - 5)
        y_position -= 20

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(width/2 - 100, 30, "Buon appetito!")

    c.save()
    return pdf_path

@app.route("/")
def index():
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    return render_template("index.html", 
                         giorni=giorni,
                         antipasti=piatti['antipasti'], 
                         zuppe_e_primi=piatti['zuppe_e_primi'], 
                         secondi=piatti['secondi'], 
                         contorni=piatti['contorni'])

@app.route("/gestione-piatti")
def gestione_piatti():
    return render_template("gestione_piatti.html", piatti=piatti)

@app.route("/aggiungi-piatto", methods=["POST"])
def aggiungi_piatto():
    categoria = request.form.get("categoria")
    nuovo_piatto = request.form.get("piatto")
    
    if categoria and nuovo_piatto and categoria in piatti:
        if nuovo_piatto not in piatti[categoria]:
            piatti[categoria].append(nuovo_piatto)
            save_piatti(piatti)
    
    return redirect(url_for('gestione_piatti'))

@app.route("/rimuovi-piatto", methods=["POST"])
def rimuovi_piatto():
    categoria = request.form.get("categoria")
    piatto = request.form.get("piatto")
    
    if categoria and piatto and categoria in piatti:
        if piatto in piatti[categoria]:
            piatti[categoria].remove(piatto)
            save_piatti(piatti)
    
    return redirect(url_for('gestione_piatti'))

@app.route("/menu", methods=["POST"])
def menu():
    menu_settimanale = {}
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    
    for giorno in giorni:
        menu_settimanale[giorno] = {
            "Antipasto": request.form.get(f"antipasto_{giorno}", ""),
            "Primo": request.form.get(f"primo_{giorno}", ""),
            "Secondo": request.form.get(f"secondo_{giorno}", ""),
            "Contorno": request.form.get(f"contorno_{giorno}", "")
        }
    
    pdf_path = create_pdf(menu_settimanale)
    return send_file(pdf_path, as_attachment=True, download_name="Menu_Verde_Basilico.pdf")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
