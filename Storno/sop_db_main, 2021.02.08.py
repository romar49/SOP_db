import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import datetime as dt
import os
import shutil


# ******************************************************** #
# ** Pripomočki ****************************************** #
# ******************************************************** #

# Brisanje vsebine Entry in Combo polj v posameznem oknu
def brisi(stars):
    otroci = stars.winfo_children()
    for otrok in otroci:
        if otrok.winfo_class() == "Entry":
            otrok.delete(0, "end")
        elif otrok.winfo_class() == "TCombobox":
            otrok.delete(0, "end")


# Brisanje vseh widgetov v posameznem oknu
def brisi_widget(stars):
    otroci = stars.winfo_children()
    for otrok in otroci:
        otrok.grid_remove()


# Preberi podatke iz Entry widgetov v posameznem oknu
def preberi_podatke(stars):
    vnos = []
    otroci = stars.winfo_children()
    for otrok in otroci:
        if otrok.winfo_class() == "Entry":
            vnos.append(otrok.get())
    return vnos


# Iz sqlite tabele poberem imena stolpcev in iz njih naredim vnosna polja na obrazcu
def imena_stolpcev(tabela):
    try:
        imena_stolpcev = [xyz[0] for xyz in cur.execute("SELECT * FROM {tabela}".
                                                        format(tabela=tabela)).description]
        return imena_stolpcev
    except Exception as e:
        messagebox.showerror("Napaka v klicu funkcije imena_stolpcev", message="Zaznana je bila napaka: " + f'{e}')


# Iz sqlite tabele poberem podatke v vrsticah in iz njih naredim elemente comoboboxa
def vrednosti_vrstic(ime_stolpca, tabela):
    try:
        vrednosti_vrstic = [xyz[0] for xyz in cur.execute("SELECT {ime_stolpca} FROM {tabela}".
                                                          format(ime_stolpca=ime_stolpca, tabela=tabela)).fetchall()]
        return vrednosti_vrstic
    except Exception as e:
        messagebox.showerror("Napaka v klicu funkcije vrednosti_vrstic", message="Zaznana je bila napaka: " + f'{e}')


# ________________________________________________________ #
# ________________________________________________________ #
# ________________________________________________________ #

# Ustvarim povezavo z db in cursor, ki kaže na njo
con = sqlite3.connect("sop_main.db")
cur = con.cursor()

# ******************************************************** #
# ** Arhiviranje backup kopij **************************** #
# ******************************************************** #

# Na začetku vedno naredim backup kopijo v mapi "C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup"
list_datotek = [file for file in os.listdir("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup")
                if os.path.isfile(os.path.join("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup", file))]

# V seznam si zapišem številke obstoječih datotek
st_bck = []
for i in list_datotek:
    try:
        x = i.index(".db")
        st_bck.append(i[16:x])
    except ValueError:
        pass

# Glede na to koliko kopij je narejenih se odločim ali dodajam nove kopije, ali pa jih prepisujem
if not st_bck:
    bck = sqlite3.connect("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/sop_main_backup_10.db")
    with bck:
        con.backup(bck)
    bck.close()

elif len(st_bck) < 30:
    nov_index = int(st_bck[-1]) + 1
    bck = sqlite3.connect(
        "C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/sop_main_backup_" + str(nov_index) + ".db")
    with bck:
        con.backup(bck)
    bck.close()

else:
    os.remove("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/sop_main_backup_10.db")

    list_datotek = [file for file in os.listdir("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup")
                    if os.path.isfile(os.path.join("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup", file))]

    for i in list_datotek:
        os.rename(r"C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/" + i,
                  r"C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/sop_main_backup_" +
                  str(int(i[16:18]) - 1) + ".db")
    nov_index = int(st_bck[-1])
    bck = sqlite3.connect(
        "C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/sop_main_backup_" + str(nov_index) + ".db")
    with bck:
        con.backup(bck)
    bck.close()

# Vsak dan prekopiram zadnjo včerajšnjo kopijo v mapo
list_datotek = [file for file in os.listdir("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup")
                if os.path.isfile(os.path.join("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup", file))]

list_dnevnih_datotek = [file for file in os.listdir("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup"
                                                    "/dnevne_kopije")
                        if os.path.isfile(os.path.join("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup"
                                                       "/dnevne_kopije", file))]

if not list_datotek:
    pass

elif not list_dnevnih_datotek:
    zadnja_kopija = list_datotek[-1]
    datum_zadnje_kopije = os.path.getmtime("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/" + zadnja_kopija)
    ymd_datum_zadnje_kopije = dt.datetime.fromtimestamp(datum_zadnje_kopije).strftime('%Y.%m.%d')
    dnevna_kopija = zadnja_kopija[0:15] + "_" + ymd_datum_zadnje_kopije + ".db"
    shutil.copyfile("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/" + zadnja_kopija,
                    "C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/dnevne_kopije/" + dnevna_kopija)

else:
    print("tu sem")
    zadnja_kopija = list_datotek[-1]
    datum_zadnje_kopije = os.path.getmtime("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/" + zadnja_kopija)
    zadnja_dnevna_kopija = list_dnevnih_datotek[-1]
    datum_zadnje_dnevne_kopije = os.path.getmtime("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/dnevne_kopije/"
                                                  + zadnja_dnevna_kopija)

    if len(list_dnevnih_datotek) < 31:
        print("pa sedaj tukaj")
        if (dt.datetime.fromtimestamp(datum_zadnje_dnevne_kopije).strftime('%m.%d')) < \
                (dt.datetime.fromtimestamp(datum_zadnje_kopije).strftime('%m.%d')):
            print("Datum je manjši in imam MANJ kot XX kopij")
            ymd_datum_zadnje_kopije = dt.datetime.fromtimestamp(datum_zadnje_kopije).strftime('%Y.%m.%d')
            dnevna_kopija = zadnja_kopija[0:15] + "_" + ymd_datum_zadnje_kopije + ".db"
            shutil.copyfile("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/" + zadnja_kopija,
                            "C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/dnevne_kopije/" + dnevna_kopija)

    else:
        print("ali pa tukaj")
        if (dt.datetime.fromtimestamp(datum_zadnje_dnevne_kopije).strftime('%m.%d')) < \
                (dt.datetime.fromtimestamp(datum_zadnje_kopije).strftime('%m.%d')):
            print("Datum je manjši in imam VEČ kot XX kopij")
            print(list_dnevnih_datotek)
            print(list_dnevnih_datotek[0])
            os.remove("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup/dnevne_kopije/" + list_dnevnih_datotek[0])
            list_dnevnih_datotek = [file for file in os.listdir("C:/Users/Marko.Rogic/PycharmProjects/SOP_db/db_backup"
                                                                "/dnevne_kopije")
                                    if os.path.isfile(os.path.join("C:/Users/Marko.Rogic/PycharmProjects/SOP_db"
                                                                   "/db_backup/dnevne_kopije", file))]
            print("Prvo datoteko sem odstranil")
            print(list_dnevnih_datotek)


# ________________________________________________________ #
# ________________________________________________________ #
# ________________________________________________________ #


# # Ukazi, ki se izvedejo po kliku na gumb "Izpis podatkov"
# def click_db_izpis():
#     podokno_izpis = tk.Toplevel()
#     podokno_izpis.title("Izpis podatkov")
#     podokno_izpis.geometry("400x500")
#     x = okno_main.winfo_x()
#     y = okno_main.winfo_y()
#     podokno_izpis.geometry("+%d+%d" % (x + 200, y + 20))
#
#     zbir_nizov = cur.execute('''SELECT * from projekt LIMIT 0,10''') # select vse zapise v tabeli
#     WHERE mesto = "Mohelnice" # select samo zapise, ki imajo v stolpcu "mesto" vrednost Mohelnice
#     WHERE mesto IS NULL OR mesto = '' # select vse zapise, ki imajo v stolpcu "mesto" prazno polje
#     zbir_nizov = cur.execute("""
#                         SELECT delovni_nalog,investitor, mesto
#                         FROM projekt
#                         WHERE mesto = "Mohelnice"
#                              """)
#     zbir_nizov = cur.execute("""
#                             SELECT delovni_nalog, investitor, mesto
#                             FROM projekt
#                             WHERE mesto = ? """,
#                              (entry_isci.get(),)
#                              )
#
#     i = 0  # row value inside the loop
#     for niz in zbir_nizov:
#         print(niz)
#         for j in range(len(niz)):
#             e = Entry(podokno_izpis, width=10, fg='blue')
#             e.grid(row=i, column=j)
#             e.insert(END, niz[j])
#         i = i + 1

# enostaven način kako onemogočiti predhodno okno
# več info na https://stackoverflow.com/questions/29233029/python-tkinter-show-only-one-copy-of-window
# podokno_izpis.transient(okno_main)
# podokno_izpis.grab_set()
# okno_main.wait_window(podokno_izpis)


# Ukazi, ki se izvedejo po kliku na gumb "Vnos podatkov v bazo"
def click_vnos():
    global podokno_vnos  # TODO Moram ugotoviti zakaj je potrebno deklarirati podokno_vnos kot global

    podokno_vnos = tk.Toplevel()
    podokno_vnos.title("Vnos podatkov v bazo")
    x = okno_main.winfo_x()
    y = okno_main.winfo_y()
    podokno_vnos.geometry("400x500" + f'+{x + 100}+{y + 10}')

    for i in range(1):
        podokno_vnos.columnconfigure(i, weight=1)
    for i in range(3):
        podokno_vnos.rowconfigure(i, weight=1)

    btn_vnos_nalogov = tk.Button(podokno_vnos,
                                 text="Vnos delovnih nalogov",
                                 relief="raised",
                                 command=click_vnos_nalogov,
                                 bg="white",
                                 fg='black')
    btn_vnos_nalogov.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_vnos_opreme = tk.Button(podokno_vnos,
                                text="Vnos opreme in materialov",
                                command=click_vnos_opreme,
                                relief="raised",
                                bg="white",
                                fg='black')
    btn_vnos_opreme.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_cancel_vnos = tk.Button(podokno_vnos,
                                text="Zaključi z vnosom",
                                relief="raised",
                                command=podokno_vnos.destroy,
                                bg="white",
                                fg='black')
    btn_cancel_vnos.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

    # enostaven način kako onemogočiti predhodno okno
    # več info na https://stackoverflow.com/questions/29233029/python-tkinter-show-only-one-copy-of-window
    podokno_vnos.transient(okno_main)
    podokno_vnos.grab_set()
    okno_main.wait_window(podokno_vnos)


# Ukazi, ki se izvedejo po kliku na gumb "Vnos delovnih nalogov"
def click_vnos_nalogov():
    # Dobi podatke iz obstoječe tabele in jih zapiši v tuple "rezultat"
    def preberi_tabelo_projekt():
        global rezultat
        rezultat = cur.execute("""SELECT
                                projekt_id, delovni_nalog, investitor, mesto, drzava,
                                datum_povpr, datum_ponudbe, datum_narocila, vodja_projekta 
                                FROM 
                                projekt 
                                WHERE 
                                delovni_nalog=?""",
                               (combo_dn.get(),)
                               ).fetchall()

        return rezultat

    # Polja v oknu "Vnos delovnih nalogov" popolni s podatki iz baze
    def izpolni_polja(eventObject):

        print(eventObject)

        rezultat = preberi_tabelo_projekt()

        entry_investitor.delete(0, "end")
        entry_investitor.insert(0, rezultat[0][2])

        entry_mesto.delete(0, "end")
        entry_mesto.insert(0, rezultat[0][3])

        entry_drzava.delete(0, "end")
        entry_drzava.insert(0, rezultat[0][4])

        # strftime pretvori datum iz UTC formata (YYYY-mm-dd hh:mm:ss) v string d.m.yyyy
        entry_povprasevanje.delete(0, "end")
        if rezultat[0][5] == "":
            entry_ponudba.insert(0, rezultat[0][5])
        else:
            entry_povprasevanje.insert(0, dt.datetime.fromisoformat(rezultat[0][5]).strftime("%d.%m.%Y"))

        entry_ponudba.delete(0, "end")
        if rezultat[0][6] == "":
            entry_ponudba.insert(0, rezultat[0][6])
        else:
            entry_ponudba.insert(0, dt.datetime.fromisoformat(rezultat[0][6]).strftime("%d.%m.%Y"))

        entry_narocilo.delete(0, "end")
        if rezultat[0][7] == "":
            entry_narocilo.insert(0, rezultat[0][7])
        else:
            entry_narocilo.insert(0, dt.datetime.fromisoformat(rezultat[0][7]).strftime("%d.%m.%Y"))

        entry_vodja.delete(0, "end")
        entry_vodja.insert(0, rezultat[0][8])

    # Kontrola pravilnosti vpisanih podatkov in prepis podatkov iz vpisnih oken v spremenljivke
    # Če niso vpisani pravi podatki nastavim kontrolko na vrednost 0
    def zberi_podatke():

        if combo_dn.get() != "":
            dn = combo_dn.get()
        else:
            messagebox.showerror("Napaka pri vnosu v bazo",
                                 message="Delovni nalog\nZaznana je bila napaka: Vpiši kodo Delovnega naloga.")
            combo_dn.focus_set()
            kontrolka = (0,)
            return kontrolka

        if entry_investitor.get() != "":
            investitor = entry_investitor.get()
        else:
            messagebox.showerror("Napaka pri vnosu v bazo",
                                 message="Investitor\nZaznana je bila napaka: Vpiši podatek o Investitorju.")
            entry_investitor.focus_set()
            kontrolka = (0,)
            return kontrolka

        if entry_mesto.get() != "":
            mesto = entry_mesto.get()
        else:
            messagebox.showerror("Napaka pri vnosu v bazo",
                                 message="Mesto\nZaznana je bila napaka: Vpiši Mesto.")
            entry_mesto.focus_set()
            kontrolka = (0,)
            return kontrolka

        if entry_drzava.get() != "":
            drzava = entry_drzava.get()
        else:
            messagebox.showerror("Napaka pri vnosu v bazo",
                                 message="Država\nZaznana je bila napaka: Vpiši Državo.")
            entry_drzava.focus_set()
            kontrolka = (0,)
            return kontrolka

        # strptime pretvori datum iz stringa d.m.yyyy v UTC format (YYYY-mm-dd hh:mm:ss)
        try:
            povprasevanje = dt.datetime.strptime(entry_povprasevanje.get(), "%d.%m.%Y")
        except Exception as e:
            messagebox.showerror("Napaka pri vnosu v bazo",
                                 message="Datum povpraševanja\nZaznana je bila napaka: " + f'{e}'
                                         + "\nVpiši datum Povpraševanja v formatu dd.mm.yyyy")
            entry_povprasevanje.focus_set()
            kontrolka = (0,)
            return kontrolka

        # preverim ali je vnos v polja Datum ponudbe in Datum naročila v pravilni obliki ali enak nič,
        # ne sme pa biti kaj drugega
        try:
            if entry_ponudba.get() == "":
                ponudba = ""
            else:
                ponudba = dt.datetime.strptime(entry_ponudba.get(), "%d.%m.%Y")
        except Exception as e:
            messagebox.showerror("Napaka pri vnosu v bazo", message="Datum ponudbe\nZaznana je bila napaka: " + f'{e}'
                                                                    + "\nVpiši datum Ponudbe v formatu dd.mm.yyyy")
            entry_ponudba.focus_set()
            kontrolka = (0,)
            return kontrolka

        try:
            if entry_narocilo.get() == "":
                narocilo = ""
            else:
                narocilo = dt.datetime.strptime(entry_narocilo.get(), "%d.%m.%Y")
        except Exception as e:
            messagebox.showerror("Napaka pri vnosu v bazo", message="Datum naročila\nZaznana je bila napaka: " + f'{e}'
                                                                    + "\nVpiši datum Naročila v formatu dd.mm.yyyy")
            entry_narocilo.focus_set()
            kontrolka = (0,)
            return kontrolka

        vodja = entry_vodja.get()

        # če sem uspešno prebral vse podatke dovolim, nastavim vrednost kontrolke na 99
        kontrolka = 99

        return kontrolka, dn, investitor, mesto, drzava, povprasevanje, ponudba, narocilo, vodja

    # Ukazi, ki se izvedejo po kliku na gumb "Vnos delovnih nalogov v bazo"
    def click_vnos_nalogov_v_db():

        podatki_za_vpis = zberi_podatke()

        if podatki_za_vpis[0] == 99:
            msg_box = messagebox.askquestion(title="Pozor",
                                             message="Pozor, če boste izbrali Da, boste spremenili bazo podatkov.",
                                             icon="warning",
                                             parent=btn_vnos_nalogov_v_db)
            if msg_box == "yes":
                # Način kako vnesti nov zapis v db
                try:
                    con.execute("""INSERT INTO projekt
                                (delovni_nalog, investitor, mesto, drzava,
                                datum_povpr, datum_ponudbe, datum_narocila, vodja_projekta)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (podatki_za_vpis[1], podatki_za_vpis[2], podatki_za_vpis[3], podatki_za_vpis[4],
                                 podatki_za_vpis[5], podatki_za_vpis[6], podatki_za_vpis[7], podatki_za_vpis[8])
                                )
                    con.commit()

                    # ker fetchall vrne poizvedbo kot list of tuples, s pomočjo [i[0] for i in žblj] dobim samo
                    # posamezne vrednosti
                    values_combo_dn = [i[0] for i in con.execute("""
                                                                SELECT delovni_nalog FROM projekt
                                                                """).fetchall()]
                    combo_dn["value"] = values_combo_dn
                except Exception as e:
                    messagebox.showerror("Napaka pri vnosu v bazo", message="Zaznana je bila napaka: " + f'{e}')
            else:
                pass

    def click_posodobi_db():

        podatki_za_vpis = zberi_podatke()

        if podatki_za_vpis[0] == 99:
            msg_box = messagebox.askquestion(title="Pozor",
                                             message="Pozor, če boste izbrali Da, boste spremenili bazo podatkov.",
                                             icon="warning",
                                             parent=btn_vnos_nalogov_v_db)
            if msg_box == "yes":
                # Način kako posodobiti obstoječi zapis v db
                try:
                    con.execute("""UPDATE
                                projekt
                                SET
                                delovni_nalog = ?,
                                investitor = ?,
                                mesto = ?,
                                drzava = ?,
                                datum_povpr = ?,
                                datum_ponudbe = ?,
                                datum_narocila = ?,
                                vodja_projekta = ?
                                WHERE
                                projekt_id = ?""",
                                (podatki_za_vpis[1], podatki_za_vpis[2], podatki_za_vpis[3], podatki_za_vpis[4],
                                 podatki_za_vpis[5], podatki_za_vpis[6], podatki_za_vpis[7], podatki_za_vpis[8],
                                 rezultat[0][0])
                                )
                    con.commit()

                    # ker fetchall vrne poizvedbo kot list of tuples, s pomočjo [i[0] for i in žblj] dobim samo
                    # posamezne vrednosti
                    values_combo_dn = [i[0] for i in cur.execute("""
                                                  SELECT delovni_nalog FROM projekt
                                                  """).fetchall()]
                    combo_dn["value"] = values_combo_dn
                except Exception as e:
                    messagebox.showerror("Napaka pri vnosu v bazo", message="Zaznana je bila napaka: " + f'{e}')
            else:
                pass

    # Glavni del funkcije, ki se izvede po kliku na gumb "Vnos delovnih nalogov"
    podokno_vnos_nalogov = tk.Toplevel()
    podokno_vnos_nalogov.title("Vnos delovnih nalogov")
    x = okno_main.winfo_x()
    y = okno_main.winfo_y()
    podokno_vnos_nalogov.geometry("400x500" + f'+{x + 200}+{y + 20}')

    for i in range(1):
        podokno_vnos_nalogov.columnconfigure(i, weight=1, uniform="enk1")
    podokno_vnos_nalogov.rowconfigure(0, weight=5, uniform="enk1")
    podokno_vnos_nalogov.rowconfigure(1, weight=4, uniform="enk1")

    zg_frame = tk.Frame(podokno_vnos_nalogov)
    zg_frame.grid(row=0, column=0, sticky="NSEW")
    zg_frame.columnconfigure(0, weight=0, uniform="enk2")
    zg_frame.columnconfigure(1, weight=1, uniform="enk2")
    for i in range(8):
        zg_frame.rowconfigure(i, weight=1, uniform="enk2")

    sp_frame = tk.Frame(podokno_vnos_nalogov)
    sp_frame.grid(row=1, column=0, sticky="NSEW")
    sp_frame.columnconfigure(0, weight=1, uniform="enk3")
    for i in range(4):
        sp_frame.rowconfigure(i, weight=1, uniform="enk3")

    lbl_dn = tk.Label(zg_frame, text="Delovni nalog  " + f'\N{COMBINING ASTERISK ABOVE}' + ":")
    lbl_dn.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)

    # ker fetchall vrne poizvedbo kot list of tuples, s pomočjo [i[0] for i in žblj] dobim samo posamezne vrednosti
    values_combo_dn = [i[0] for i in cur.execute("""
                                                 SELECT delovni_nalog FROM projekt
                                                 """).fetchall()]
    combo_dn = ttk.Combobox(zg_frame, values=values_combo_dn)
    combo_dn.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
    combo_dn.bind("<<ComboboxSelected>>", izpolni_polja)

    lbl_investitor = tk.Label(zg_frame, text="Investitor  " + f'\N{COMBINING ASTERISK ABOVE}' + ":")
    lbl_investitor.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)

    entry_investitor = tk.Entry(zg_frame)
    entry_investitor.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

    lbl_mesto = tk.Label(zg_frame, text="Mesto  " + f'\N{COMBINING ASTERISK ABOVE}' + ":")
    lbl_mesto.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)

    entry_mesto = tk.Entry(zg_frame)
    entry_mesto.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

    lbl_drzava = tk.Label(zg_frame, text="Država  " + f'\N{COMBINING ASTERISK ABOVE}' + ":")
    lbl_drzava.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)

    entry_drzava = tk.Entry(zg_frame)
    entry_drzava.grid(row=3, column=1, sticky=tk.NSEW, padx=5, pady=5)

    lbl_povprasevanje = tk.Label(zg_frame, text="Datum povpraševanja  " + f'\N{COMBINING ASTERISK ABOVE}' + ":")
    lbl_povprasevanje.grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)

    entry_povprasevanje = tk.Entry(zg_frame)
    entry_povprasevanje.grid(row=4, column=1, sticky=tk.NSEW, padx=5, pady=5)

    lbl_ponudba = tk.Label(zg_frame, text="Datum ponudbe:")
    lbl_ponudba.grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)

    entry_ponudba = tk.Entry(zg_frame)
    entry_ponudba.grid(row=5, column=1, sticky=tk.NSEW, padx=5, pady=5)

    lbl_narocilo = tk.Label(zg_frame, text="Datum naročila:")
    lbl_narocilo.grid(row=6, column=0, sticky=tk.E, padx=5, pady=5)

    entry_narocilo = tk.Entry(zg_frame)
    entry_narocilo.grid(row=6, column=1, sticky=tk.NSEW, padx=5, pady=5)

    lbl_vodja = tk.Label(zg_frame, text="Vodja projekta  " + f'\N{COMBINING ASTERISK ABOVE}' + ":")
    lbl_vodja.grid(row=7, column=0, sticky=tk.E, padx=5, pady=5)

    entry_vodja = tk.Entry(zg_frame)
    entry_vodja.grid(row=7, column=1, sticky=tk.NSEW, padx=5, pady=5)

    btn_vnos_nalogov_v_db = tk.Button(sp_frame,
                                      text="Vnos delovnih nalogov v bazo",
                                      # command=click_vnos_nalogov_v_db,
                                      relief="raised",
                                      bg="white",
                                      fg='black')
    btn_vnos_nalogov_v_db.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_posodobi_db = tk.Button(sp_frame,
                                text="Posodobi vnos v bazi",
                                # command=click_posodobi_db,
                                relief="raised",
                                bg="white",
                                fg='black')
    btn_posodobi_db.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_izbrisi_podatke = tk.Button(sp_frame,
                                    text="Počisti tabelo",
                                    command=lambda: brisi(zg_frame),
                                    relief="raised",
                                    bg="white",
                                    fg='black')
    btn_izbrisi_podatke.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_zakljuci_vnos = tk.Button(sp_frame,
                                  text="Zaključi z vnosom",
                                  relief="raised",
                                  command=podokno_vnos_nalogov.destroy,
                                  bg="white",
                                  fg='black')
    btn_zakljuci_vnos.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)

    # enostaven način kako onemogočiti predhodno okno
    # več info na https://stackoverflow.com/questions/29233029/python-tkinter-show-only-one-copy-of-window
    podokno_vnos_nalogov.transient(podokno_vnos)
    podokno_vnos_nalogov.grab_set()
    podokno_vnos.wait_window(podokno_vnos_nalogov)


def click_vnos_opreme():
    # Funkcija prikaže samo potrebne zaslonske elemente
    def odpri_combo_oprema_mat(eventObject):
        print(eventObject)
        if combo_oprema_mat.get() == "Oprema":
            lbl_material.grid_remove()
            combo_material.delete(0, "end")
            combo_material.grid_remove()
            lbl_material.grid(row=2, column=0, sticky="W", padx=5, pady=5)
            combo_oprema.grid(row=3, column=0, sticky="NSEW", padx=5, pady=5)

        elif combo_oprema_mat.get() == "Material":
            lbl_oprema.grid_remove()
            combo_oprema.delete(0, "end")
            combo_oprema.grid_remove()
            lbl_oprema.grid(row=2, column=0, sticky="W", padx=5, pady=5)
            combo_material.grid(row=3, column=0, sticky="NSEW", padx=5, pady=5)

    # Iz sqlite tabele poberem imena stolpcev in iz njih naredim vnosna polja na obrazcu
    def izpis_polj(eventObject):
        print(eventObject)
        list_imena_stolpcev = []
        try:
            if combo_oprema.get() != "":
                list_imena_stolpcev = imena_stolpcev(combo_oprema.get())
            elif combo_material.get() != "":
                list_imena_stolpcev = imena_stolpcev(combo_material.get())

            z = 1
            while z < len(list_imena_stolpcev):
                if z == 1:
                    tekst_polja = str(list_imena_stolpcev[z])
                    urejen_tekst = tekst_polja.replace("_", " ")
                    lbl_polja = tk.Label(frame_2, text=urejen_tekst.capitalize())
                    lbl_polja.grid(row=0, column=0, sticky="S", padx=5, pady=5, columnspan=2)
                    entry_polje = tk.Entry(frame_2)
                    entry_polje.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5, columnspan=2)

                if z == 2:
                    tekst_polja = list_imena_stolpcev[z]
                    urejen_tekst = tekst_polja.replace("_", " ")
                    lbl_polja = tk.Label(frame_2, text=urejen_tekst.capitalize())
                    lbl_polja.grid(row=0, column=2, sticky="S", padx=5, pady=5)
                    entry_polje = tk.Entry(frame_2)
                    entry_polje.grid(row=1, column=2, sticky=tk.EW, padx=5, pady=5)

                if 2 < z <= 5:
                    tekst_polja = list_imena_stolpcev[z]
                    urejen_tekst = tekst_polja.replace("_", " ")
                    lbl_polja = tk.Label(frame_2, text=urejen_tekst.capitalize())
                    lbl_polja.grid(row=0, column=z, sticky="S", padx=5, pady=5)
                    entry_polje = tk.Entry(frame_2)
                    entry_polje.grid(row=1, column=z, sticky=tk.EW, padx=5, pady=5)

                if z > 5:
                    tekst_polja = list_imena_stolpcev[z]
                    urejen_tekst = tekst_polja.replace("_", " ")
                    lbl_polja = tk.Label(frame_2, text=urejen_tekst.capitalize())
                    lbl_polja.grid(row=2, column=z - 6, sticky="S", padx=5, pady=5)
                    entry_polje = tk.Entry(frame_2)
                    entry_polje.grid(row=3, column=z - 6, sticky=tk.EW, padx=5, pady=5)

                z += 1

        except Exception as e:
            messagebox.showerror("Napaka v izpis_polj", message="Zaznana je bila napaka: " + f'{e}')

    # Počistim vse izbire iz obrazca, da lahko uporabnik ponovno začne od začetka
    def pocisti_obrazec():
        lbl_material.grid_remove()
        combo_material.delete(0, "end")
        combo_material.grid_remove()
        lbl_oprema.grid_remove()
        combo_oprema.delete(0, "end")
        combo_oprema.grid_remove()
        combo_oprema_mat.delete(0, "end")
        combo_oprema_mat.focus_set()

        brisi_widget(frame_2)

    # Kontrola pravilnosti vpisanih podatkov in prepis podatkov iz vpisnih oken v spremenljivke
    # Če niso vpisani pravi podatki nastavim kontrolko na vrednost 0
    def zberi_podatke():
        vnos = preberi_podatke(frame_2)
        print(vnos)
        # if vnos != "":
        #     print("Vnos v obrazcu je: ", vnos)

        # if combo_dn.get() != "":
        #     dn = combo_dn.get()
        # else:
        #     messagebox.showerror("Napaka pri vnosu v bazo",
        #                          message="Delovni nalog\nZaznana je bila napaka: Vpiši kodo Delovnega naloga.")
        #     combo_dn.focus_set()
        #     kontrolka = (0,)
        #     return kontrolka
        #
        # if entry_investitor.get() != "":
        #     investitor = entry_investitor.get()
        # else:
        #     messagebox.showerror("Napaka pri vnosu v bazo",
        #                          message="Investitor\nZaznana je bila napaka: Vpiši podatek o Investitorju.")
        #     entry_investitor.focus_set()
        #     kontrolka = (0,)
        #     return kontrolka
        #
        # if entry_mesto.get() != "":
        #     mesto = entry_mesto.get()
        # else:
        #     messagebox.showerror("Napaka pri vnosu v bazo",
        #                          message="Mesto\nZaznana je bila napaka: Vpiši Mesto.")
        #     entry_mesto.focus_set()
        #     kontrolka = (0,)
        #     return kontrolka

    # Glavni del funkcije, ki se izvede po kliku na gumb "Vnos opreme"
    podokno_vnos_opreme = tk.Toplevel()
    podokno_vnos_opreme.title("Vnos opreme in materialov")
    x = okno_main.winfo_x()
    y = okno_main.winfo_y()
    podokno_vnos_opreme.geometry("1200x500" + f'+{x - 400}+{y - 20}')
    podokno_vnos_opreme.columnconfigure(0, weight=1, uniform="uni1")
    podokno_vnos_opreme.columnconfigure(1, weight=5, uniform="uni1")
    podokno_vnos_opreme.columnconfigure(2, weight=1, uniform="uni1")
    podokno_vnos_opreme.rowconfigure(0, weight=1, uniform="uni1")
    podokno_vnos_opreme.rowconfigure(1, weight=1, uniform="uni1")

    frame_1 = tk.Frame(podokno_vnos_opreme)
    frame_1.grid(row=0, column=0, sticky="NSEW", rowspan=2)
    # frame_1.config(bg="red")
    frame_1.columnconfigure(0, weight=1, uniform="uni2")
    for i in range(14):
        frame_1.rowconfigure(i, weight=1, uniform="uni2")

    frame_2 = tk.Frame(podokno_vnos_opreme)
    frame_2.grid(row=0, column=1, sticky="NSEW")
    # frame_2.config(bg="blue")
    for i in range(6):
        frame_2.columnconfigure(i, weight=1, uniform="uni3")
    for i in range(7):
        frame_2.rowconfigure(i, weight=1, uniform="uni3")

    frame_3 = tk.Frame(podokno_vnos_opreme)
    frame_3.grid(row=1, column=1, sticky="NSEW")
    # frame_3.config(bg="cyan")
    for i in range(1):
        frame_3.columnconfigure(i, weight=1, uniform="uni4")
    for i in range(7):
        frame_3.rowconfigure(i, weight=1, uniform="uni4")

    frame_4 = tk.Frame(podokno_vnos_opreme)
    frame_4.grid(row=0, column=2, sticky="NSEW", rowspan=2)
    # frame_4.config(bg="green")
    for i in range(1):
        frame_4.columnconfigure(i, weight=1, uniform="uni5")
    for i in range(9):
        frame_4.rowconfigure(i, weight=1, uniform="uni5")

    lbl_oprema_mat = tk.Label(frame_1, text="Oprema ali Material:")
    lbl_oprema_mat.grid(row=0, column=0, sticky="W", padx=5, pady=5)
    values_combo_oprema_mat = vrednosti_vrstic("oprema_ali_material", "oprema_ali_material")
    combo_oprema_mat = ttk.Combobox(frame_1, values=values_combo_oprema_mat)
    combo_oprema_mat.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
    combo_oprema_mat.bind("<<ComboboxSelected>>", odpri_combo_oprema_mat)

    lbl_oprema = tk.Label(frame_1, text="Vrsta opreme")
    values_combo_oprema = vrednosti_vrstic("vrsta_opreme", "oprema")
    combo_oprema = ttk.Combobox(frame_1, values=values_combo_oprema)
    combo_oprema.bind("<<ComboboxSelected>>", izpis_polj)

    lbl_material = tk.Label(frame_1, text="Vrsta materiala")
    values_combo_material = vrednosti_vrstic("vrsta_materiala", "material")
    combo_material = ttk.Combobox(frame_1, values=values_combo_material)
    combo_material.bind("<<ComboboxSelected>>", izpis_polj)

    btn_vnos_opreme_v_db = tk.Button(frame_4,
                                     text="Vnos opreme ali materiala v bazo",
                                     command=zberi_podatke,
                                     relief="raised",
                                     bg="white",
                                     fg='black',
                                     wraplength=100)
    btn_vnos_opreme_v_db.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_posodobi_db = tk.Button(frame_4,
                                text="Posodobi vnos v bazi",
                                # command=click_posodobi_db,
                                relief="raised",
                                bg="white",
                                fg='black')
    btn_posodobi_db.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_izbrisi_podatke = tk.Button(frame_4,
                                    text="Počisti obrazec",
                                    command=pocisti_obrazec,
                                    relief="raised",
                                    bg="white",
                                    fg='black')
    btn_izbrisi_podatke.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

    btn_zakljuci_vnos = tk.Button(frame_4,
                                  text="Zaključi z vnosom",
                                  relief="raised",
                                  command=podokno_vnos_opreme.destroy,
                                  bg="white",
                                  fg='black')
    btn_zakljuci_vnos.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)

    # enostaven način kako onemogočiti predhodno okno
    # več info na https://stackoverflow.com/questions/29233029/python-tkinter-show-only-one-copy-of-window
    podokno_vnos_opreme.transient(podokno_vnos)
    podokno_vnos_opreme.grab_set()
    podokno_vnos.wait_window(podokno_vnos_opreme)


# Dobi osnovne podatke iz uporabniškega okna
okno_main = tk.Tk()
okno_main.title("Baza podatkov SOP")
okno_width = 400
okno_height = 500
screen_width = okno_main.winfo_screenwidth()
screen_height = okno_main.winfo_screenheight()
start_x = int((screen_width / 2) - (okno_width / 2))
start_y = int((screen_height / 2) - (okno_height / 2))
# Positions the window in the center of the page.
okno_main.geometry(f'{okno_width}x{okno_height}+{start_x}+{start_y}')
okno_main.resizable(False, False)
okno_main.lift()

for i in range(1):
    okno_main.columnconfigure(i, weight=1)
for i in range(3):
    okno_main.rowconfigure(i, weight=1)

btn_vnos = tk.Button(okno_main,
                     text="Vnos podatkov v bazo",
                     relief="raised",
                     command=click_vnos,
                     bg="white",
                     fg='black')
btn_vnos.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

btn_izpis = tk.Button(okno_main,
                      text="Izpis podatkov",
                      relief="raised",
                      # command=click_db_izpis,
                      bg="white",
                      fg='black')
btn_izpis.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

btn_cancel = tk.Button(okno_main,
                       text="Izhod iz programa",
                       relief="raised",
                       command=okno_main.quit,
                       bg="white",
                       fg='black')
btn_cancel.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

okno_main.mainloop()
