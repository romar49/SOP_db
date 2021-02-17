from tkinter import *
import sqlite3

# Ustvarim povezavo z db in cursor, ki kaže na njo
from tkinter import messagebox

con = sqlite3.connect("sop_main.db")
cur = con.cursor()

# Način kako ustvariti novo tabelo v db, pri čemer predhodno preverim ali tabela s tem imenom že obstaja
# Preverim tudi, da ne vnašam praznih stringov in da se last_name ne ponavlja - ni dvojnik
cur.execute("""
            CREATE TABLE IF NOT EXISTS projekt
            (
            projekt_id integer PRIMARY KEY,
            delovni_nalog text NOT NULL UNIQUE CHECK(delovni_nalog <> ""),
            investitor text NOT NULL CHECK(investitor <> ""),
            mesto text NOT NULL CHECK(mesto <> ""),
            drzava text NOT NULL CHECK(drzava <> ""),
            datum_povpr text NOT NULL CHECK(datum_povpr <> ""),
            datum_ponudbe text,
            datum_narocila text,
            vodja_projekta text
            )
            """)


# Preimenovanje stolpca v tabeli
# cur.execute("ALTER TABLE projekt RENAME COLUMN koda_projekta TO delovni_nalog")

# Dodajanje stoplca tabeli
# cur.execute("ALTER TABLE projekt ADD COLUMN mesto")

# Ukazi, ki se izvedejo po kliku na gumb "Vnos podatkov v bazo"
def click_db_vnos():
    msg_box = messagebox.askquestion(title="Pozor",
                                     message="Pozor, če boste izbrali Da, boste spremenili bazo podatkov.",
                                     icon="warning")
    if msg_box == "yes":
        # Način kako vnesti nov zapis v db
        try:
            cur.execute("INSERT INTO projekt "
                        "(delovni_nalog, investitor, mesto, drzava, datum_povpr, datum_ponudbe, datum_narocila, "
                        "vodja_projekta) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (entry_dn.get(), entry_investitor.get(), entry_mesto.get(), entry_drzava.get(),
                         entry_povprasevanje.get(), entry_ponudba.get(), entry_narocilo.get(), entry_vodja.get())
                        )
            con.commit()
        except Exception as e:
            messagebox.showerror("Napaka pri vnosu v bazo", message="Zaznana je bila napaka: " + f'{e}')


# Ukazi, ki se izvedejo po kliku na gumb "Izpis podatkov"
def click_db_izpis():
    okno_izpis = Toplevel()
    okno_izpis.title("Izpis podatkov")
    okno_izpis.geometry("1000x500")

    # zbir_nizov = cur.execute('''SELECT * from projekt LIMIT 0,10''') # select vse zapise v tabeli
    # WHERE mesto = "Mohelnice" # select samo zapise, ki imajo v stolpcu "mesto" vrednost Mohelnice
    # WHERE mesto IS NULL OR mesto = '' # select vse zapise, ki imajo v stolpcu "mesto" prazno polje
    # zbir_nizov = cur.execute("""
    #                     SELECT delovni_nalog,investitor, mesto
    #                     FROM projekt
    #                     WHERE mesto = "Mohelnice"
    #                          """)
    zbir_nizov = cur.execute("""
                            SELECT delovni_nalog, investitor, mesto
                            FROM projekt
                            WHERE mesto = ? """,
                             (entry_isci.get(),)
                             )

    i = 0  # row value inside the loop
    for niz in zbir_nizov:
        print(niz)
        for j in range(len(niz)):
            e = Entry(okno_izpis, width=10, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, niz[j])
        i = i + 1


def click_btn_vnos():
    print("dd")


class GlavnoOkno:
    def __init__(self, master, title="", okno_width=500, okno_height=500):
        self.master = master

        master.title(title)

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        start_x = int((screen_width / 2) - (okno_width / 2))
        start_y = int((screen_height / 2) - (okno_height / 2))
        # Positions the window in the center of the page.
        master.geometry(f'{okno_width}x{okno_height}+{start_x}+{start_y}')
        master.resizable(False, False)
        master.lift()


# Odprem glavno okno z osnovnimi nadzornimi gumbi
root = Tk()
root_title = "Baza podatkov SOP"
okno_main = GlavnoOkno(root, root_title)

for i in range(2):
    okno_main.master.columnconfigure(i, weight=1)
for i in range(1):
    okno_main.master.rowconfigure(i, weight=1)

lbl_proba = Label(okno_main.master, text="Proba")
lbl_proba.grid(row=0, column=0, sticky=W)

btn_vnos = Button(okno_main.master,
                  text="Vnos v bazo SOP",
                  command=click_btn_vnos(),
                  # command=okno_main.master.quit,
                  bg="white",
                  fg='black')
btn_vnos.grid(row=1, column=0, sticky=EW)

btn_cancel = Button(okno_main.master,
                    text="Izhod iz programa",
                    command=okno_main.master.quit,
                    bg="white",
                    fg='black')
btn_cancel.grid(row=1, column=1, sticky=EW)

root.mainloop()

# # Ukazi, ki se izvedejo po kliku na gumb "Izhod iz programa"
# def click_db_izhod():
#     okno_main.destroy()
#
#
# # Dobi osnovne podatke iz uporabniškega okna
# okno_main = Tk()
# # okno_main.tk.call('encoding', 'system', 'utf-8')
# okno_main.title("Baza podatkov SOP")
# okno_width = 500
# okno_height = 500
# screen_width = okno_main.winfo_screenwidth()
# screen_height = okno_main.winfo_screenheight()
# start_x = int((screen_width / 2) - (okno_width / 2))
# start_y = int((screen_height / 2) - (okno_height / 2))
# # Positions the window in the center of the page.
# # okno.geometry('{}x{}+{}+{}'.format(okno_width, okno_height, start_x, start_y))
# okno_main.geometry(f'{okno_width}x{okno_height}+{start_x}+{start_y}')
# okno_main.resizable(False, False)
# okno_main.lift()
#
# lbl_dn = Label(okno_main, text="Delovni nalog:")
# lbl_dn.place(x=10, y=10)
#
# entry_dn = Entry(okno_main)
# entry_dn.place(x=140, y=10)
#
# lbl_investitor = Label(okno_main, text="Investitor:")
# lbl_investitor.place(x=10, y=40)
#
# entry_investitor = Entry(okno_main)
# entry_investitor.place(x=140, y=40)
#
# lbl_mesto = Label(okno_main, text="Mesto:")
# lbl_mesto.place(x=10, y=70)
#
# entry_mesto = Entry(okno_main)
# entry_mesto.place(x=140, y=70)
#
# lbl_drzava = Label(okno_main, text="Država:")
# lbl_drzava.place(x=10, y=100)
#
# entry_drzava = Entry(okno_main)
# entry_drzava.place(x=140, y=100)
#
# lbl_povprasevanje = Label(okno_main, text="Datum povpraševanja:")
# lbl_povprasevanje.place(x=10, y=130)
#
# entry_povprasevanje = Entry(okno_main)
# entry_povprasevanje.place(x=140, y=130)
#
# lbl_ponudba = Label(okno_main, text="Datum ponudbe:")
# lbl_ponudba.place(x=10, y=160)
#
# entry_ponudba = Entry(okno_main)
# entry_ponudba.place(x=140, y=160)
#
# lbl_narocilo = Label(okno_main, text="Datum naročila:")
# lbl_narocilo.place(x=10, y=190)
#
# entry_narocilo = Entry(okno_main)
# entry_narocilo.place(x=140, y=190)
#
# lbl_vodja = Label(okno_main, text="Vodja projekta:")
# lbl_vodja.place(x=10, y=220)
#
# entry_vodja = Entry(okno_main)
# entry_vodja.place(x=140, y=220)
#
# lbl_isci = Label(okno_main, text="Išči:")
# lbl_isci.place(x=10, y=280)
#
# entry_isci = Entry(okno_main)
# entry_isci.place(x=140, y=280)
#
# btn_vnos = Button(okno_main,
#                   text="Vnos podatkov v bazo",
#                   command=click_db_vnos,
#                   bg="white",
#                   fg='black')
# btn_vnos.place(relx=0.1, rely=0.8, anchor=W)
#
# btn_izpis = Button(okno_main,
#                    text="Izpis podatkov",
#                    command=click_db_izpis,
#                    bg="white",
#                    fg='black')
# btn_izpis.place(relx=0.45, rely=0.8, anchor=W)
#
# btn_cancel = Button(okno_main,
#                     text="Izhod iz programa",
#                     command=click_db_izhod,
#                     bg="white",
#                     fg='black')
# btn_cancel.place(relx=0.7, rely=0.8, anchor=W)
#
# menubar = Menu(okno_main)
# sett_menu = Menu(menubar, tearoff=0)
# menubar.add_cascade(label="Nastavitve", menu=sett_menu)
# # sett_menu.add_command(label="Podatki zaposlenih", command=uredi_podatke)
# okno_main.config(menu=menubar)
#
# okno_main.mainloop()
