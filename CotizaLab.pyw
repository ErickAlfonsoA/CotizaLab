import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import sys
from pathlib import Path
import json

#root
root = tk.Tk()

def cotiFun(): # Para la pestaña de cotizar
    cont = 0
    for widget in root.winfo_children(): # Para limpiar el frame dejando solo el switch 
        if cont > 0:
            widget.destroy()
        cont += 1
    stick.place(x=127) # Posicionar el palo

    def hiddenText(event):
        textH = cotSearch.get()
        if textH == "Buscar analisis":
            cotSearch.delete(0, tk.END)
            cotSearch.config(fg = 'black')
        elif textH == "":
            cotSearch.insert(0,"Buscar analisis")
            cotSearch.config(fg = 'grey')

    def search(event):
        tree.delete(*tree.get_children())
        for da in jdata['Data']:
            if cotSearch.get().upper() in da[0].upper():
                tree.insert("", "end", tags="back", text=da[0], values=(da[1], da[2], da[3], da[5], da[6]))
    
    def treeSelect(event):
        def finalPrice(name, pri, desc, popup2):
            # Insertacion del precio
            pri = float(float(pri)-((desc*float(pri))/100))
            ticketTree.insert("", "end", tags="back", text=name, values=(pri))
            reco = []
            tot = 0
            for ite in ticketTree.get_children():
                i = ticketTree.item(ite)
                reco += i['values']
            for r in reco:
                tot += float(r)
            total.config(text="Total: "+str(tot))
            root.wm_attributes("-disabled", False)
            #tree.selection_remove(tree.selection())
            popup2.destroy()

        def addPrice(name, pri):
            # Popup del descuento
            data = 'data.json' # Comprobar que exista el json
            salF = Path('.') / data
            if not salF.exists:
                print("No existe el archivo de entrada")
                sys.exit()

            jdata = None
            with salF.open(encoding="utf-8") as fjson: # Abrir el json y cargarlo en la variable jdata
                jdata = json.load(fjson)

            try:
                for da in jdata['Data']:
                    if name == da[0]:
                        if da[4] == 1:
                            popup2 = tk.Toplevel(root)
                            popup2.title("¿Tiene descuento?")
                            popup2.geometry("+297+300")
                            popup2.iconphoto(False, logo, logo)
                            popup2.config(bg = black)
                            root.wm_attributes("-disabled", True) #Hacer el popoup uno persistente (modal)
                            popup2.protocol("WM_DELETE_WINDOW", lambda: None) #Deshabilitar el boton de la X para cerrar ventana
                            popup2.resizable(0, 0) #Quitar el boton de maximizar ventana

                            labelP = tk.Label(popup2)
                            labelP.config(bg=black, fg=honey, text="¿Tiene descuento?", font=("Helvetica", 12))
                            labelP.pack()

                            value1 = tk.Button(popup2)
                            value1.config(bg=honey, text="0%", font=("Helvetica", 12), activebackground="#ef9659")
                            value1.pack(side='left', padx=10, pady=10)
                            value1.configure(command=lambda: finalPrice(name, pri, 0, popup2))

                            value2 = tk.Button(popup2)
                            value2.config(bg=honey, text="10%", font=("Helvetica", 12), activebackground="#ef9659")
                            value2.pack(side='left', padx=10, pady=10)
                            value2.configure(command=lambda: finalPrice(name, pri, 10, popup2))

                            value3 = tk.Button(popup2)
                            value3.config(bg=honey, text="15%", font=("Helvetica", 12), activebackground="#ef9659")
                            value3.pack(side='left', padx=10, pady=10)
                            value3.configure(command=lambda: finalPrice(name, pri, 15, popup2))
                            
                            value4 = tk.Button(popup2)
                            value4.config(bg=honey, text="20%", font=("Helvetica", 12), activebackground="#ef9659")
                            value4.pack(side='left', padx=10, pady=10)
                            value4.configure(command=lambda: finalPrice(name, pri, 20, popup2))
                            
                            value5 = tk.Button(popup2)
                            value5.config(bg=honey, text="25%", font=("Helvetica", 12), activebackground="#ef9659")
                            value5.pack(side='left', padx=10, pady=10)
                            value5.configure(command=lambda: finalPrice(name, pri, 25, popup2))
                        else:
                            # Insertacion del precio
                            ticketTree.insert("", "end", tags="back", text=name, values=(pri))
                            reco = []
                            tot = 0
                            for ite in ticketTree.get_children():
                                i = ticketTree.item(ite)
                                reco += i['values']
                            for r in reco:
                                tot += float(r)
                            total.config(text="Total: "+str(tot))
                            root.wm_attributes("-disabled", False)
                            #tree.selection_remove(tree.selection())
                            
            except UnboundLocalError:
                root.wm_attributes("-disabled", False) #Devolverle el control a la root
                popup2.destroy()

        for itemS in tree.selection():
            item = tree.item(itemS)
            record = item['values']
            name = item['text']
        
        try:
            addPrice(item["text"], record[0])
        except UnboundLocalError:
            pass

    def ticketTreeSelectButton():
        if ticketTree.selection() != ():
            for i in ticketTree.selection():
                val = ticketTree.item(i)["values"]
            total.config(text="Total: "+str(float(total.cget('text')[7::])-float(val[0])))
            ticketTree.delete(ticketTree.selection())
        else:
            ticketTree.delete(*ticketTree.get_children())
            total.config(text="Total: 0")

    #Instancias
    swFrame = tk.Frame(root, bg=black, bd=20, width=300)
    ticket = tk.Frame(root, bg=black, bd=20, relief='flat')

    #Configuracion de las instancias
    swFrame.pack(fill=tk.BOTH, expand=True, side='left')  
    ticket.pack(fill=tk.BOTH, expand=True, side='right')

    #Treeview del ticket
    ticketTree = ttk.Treeview(ticket)
    scrollTableTicket = tk.Scrollbar(ticket, command=ticketTree.yview)

    ticketTree.tag_configure("back", font=("Helvetica", 10))
    ticketTree["columns"] = ("col1")

    scrollTableTicket.place(in_=ticketTree, relx=1, relheight=1, bordermode='inside')

    ticketTree["style"] = "Custom.Treeview"

    ticketTree.heading("#0", text="Nombre del analisis")
    ticketTree.heading("col1", text="Precio")

    ticketTree.column("#0", width=100, minwidth=70, anchor='center')
    ticketTree.column("col1", width=70, minwidth=70, anchor='center')

    ticketTree.pack(fill='both', expand=True, padx=30)

    #Boton para eliminar lo seleccionado
    cotDelButton = tk.Button(ticket)
    cotDelButton.config(bg=honey, text="Eliminar", font=("Helvetica", 12), activebackground="#ef9659")
    cotDelButton.pack(side='left', padx=(70,0), pady=(10,0))
    cotDelButton.configure(command=ticketTreeSelectButton)

    #Label con el total
    total = tk.Label(ticket)
    total.config(bg=black, fg=honey, text="Total: 0", font=("Helvetica", 12))
    total.pack(pady=(12,0))

    #Buscador/Filtrador
    cotSearch = tk.Entry(swFrame)
    cotSearch.config(bg=white, fg='grey', font=("Helvetica", 12))
    cotSearch.insert(0, 'Buscar analisis')
    cotSearch.bind("<FocusIn>", hiddenText)
    cotSearch.bind("<FocusOut>", hiddenText)
    cotSearch.bind("<Return>", search)
    cotSearch.pack(pady=10)

    #Tabla
    tree = ttk.Treeview(swFrame)
    scrollTable = tk.Scrollbar(swFrame, command=tree.yview)
    #scrollTable2 = tk.Scrollbar(swFrame, command=tree.xview)

    tree.tag_configure("back", font=("Helvetica", 10))
    tree["columns"] = ("col1", "col2", "col3", "col4", "col5")

    #scrollTable.grid(sticky='NSW') #lo estira verticalmente y lo coloca en el medio de la fila
    scrollTable.place(in_=tree, relx=1, relheight=1, bordermode='inside')
    #scrollTable2.place(in_=tree, relx=1, relheight=1, bordermode='inside')

    tree["style"] = "Custom.Treeview"

    tree.heading("#0", text="Nombre del analisis")
    tree.heading("col1", text="Precio Publico")
    tree.heading("col2", text="Micro-Tec")
    tree.heading("col3", text="Lab-Tec")
    tree.heading("col4", text="Especificaciones")
    tree.heading("col5", text="Entrega")

    tree.column("#0", width=200, minwidth=70, anchor='center')
    tree.column("col1", width=40, minwidth=40, anchor='center')
    tree.column("col2", width=40, minwidth=40, anchor='center')
    tree.column("col3", width=70, minwidth=70, anchor='center')
    tree.column("col4", width=100, minwidth=100, anchor='center')
    tree.column("col5", width=40, minwidth=40, anchor='center')

    tree.pack(fill=tk.BOTH, expand=True, padx=30)

    tree.bind("<<TreeviewSelect>>", treeSelect)

    #Mostrar datos en la tabla
    data = 'data.json' # Comprobar que exista el json
    salF = Path('.') / data
    if not salF.exists:
        print("No existe el archivo de entrada")
        sys.exit()

    jdata = None
    with salF.open(encoding="utf-8") as fjson: # Abrir el json y cargarlo en la variable jdata
        jdata = json.load(fjson)

    for da in jdata['Data']:
        tree.insert("", "end", tags="back", text=da[0], values=(da[1], da[2], da[3], da[5], da[6]))

def addFun():
    cont = 0
    for widget in root.winfo_children():
        if cont > 0:
            widget.destroy()
        cont += 1
    stick.place(x=454)
    
    def addDataJson(name, pri1, pri2, pri3, d1, d2):
        try:
            if name.get() != "":
                jdata = None
                data = 'data.json' # Comprobar que exista el json
                salF = Path('.') / data
                newData = [name.get(), float(pri1.get()), pri2.get(), pri3.get(), int(rutinaRes.get()), d1.get(), d2.get().upper()]
                with salF.open(encoding="utf-8", mode='r+') as fjson: # Abrir el json y cargarlo en la variable jdata
                    jdata = json.load(fjson)
                    jdata["Data"] += [newData]
                
                exit = Path(".") / "data.json"
                with exit.open('w', encoding="utf-8") as ex:
                    ex.write(json.dumps(jdata))

                help.config(text="Datos ingresados correctamente!!")
                name.delete(0, tk.END)
                pri1.delete(0, tk.END)
                pri2.delete(0, tk.END)
                pri3.delete(0, tk.END)
                d1.delete(0, tk.END)
                d2.delete(0, tk.END)

                rutinaRes.set(False)
            else:
                help.config(text="Porfavor ingrese un nombre valido para el análisis")     
        except ValueError:
           help.config(text="Porfavor ingrese datos numericos en los precios ejemplo: 100")

    # Funciones de los botones
    def on_enter(text):
        help.config(text=text)

    def on_leave(text):
        help.config(text=text)

    swFrame = tk.Frame(root, bg=black, bd=20, width=300)
    swFrame.pack(fill=tk.BOTH, expand=True, side='left')

    swFrame.columnconfigure([0,1,2,3], weight=1)
    swFrame.rowconfigure([0,1,2,3,4], weight=1)

    nameLabel = tk.Label(swFrame)
    nameLabel.config(bg=black, fg=honey, text="Nombre del analisis:", font=("Helvetica", 10))
    nameLabel.grid(column=0, row=0)

    nameEntry = tk.Entry(swFrame)
    nameEntry.config(bg=white, fg='black', font=("Helvetica", 10), width=25)
    nameEntry.insert(0, "")
    nameEntry.grid(column=1, row=0)
    nameEntry.bind("<Enter>", lambda event: on_enter("Agrege el nombre del analisis siguiendo el siguiente formato\n'Nombre del analisis (Abreviacion)'"))
    nameEntry.bind("<Leave>", lambda event: on_leave(""))

    priceLabel1 = tk.Label(swFrame)
    priceLabel1.config(bg=black, fg=honey, text="Precio Publico:", font=("Helvetica", 10))
    priceLabel1.grid(column=2, row=0)

    priceEntry1 = tk.Entry(swFrame)
    priceEntry1.config(bg=white, fg='black', font=("Helvetica", 10), width=25)
    priceEntry1.insert(0, "")
    priceEntry1.grid(column=3, row=0)
    priceEntry1.bind("<Enter>", lambda event: on_enter("Agrege el precio del analisis segun el primer laboratorio"))
    priceEntry1.bind("<Leave>", lambda event: on_leave(""))

    priceLabel2 = tk.Label(swFrame)
    priceLabel2.config(bg=black, fg=honey, text="Micro-Tec:", font=("Helvetica", 10))
    priceLabel2.grid(column=0, row=1)

    priceEntry2 = tk.Entry(swFrame)
    priceEntry2.config(bg=white, fg='black', font=("Helvetica", 10), width=25)
    priceEntry2.insert(0, "")
    priceEntry2.grid(column=1, row=1)
    priceEntry2.bind("<Enter>", lambda event: on_enter("Agrege el precio del analisis segun Micro-Tec"))
    priceEntry2.bind("<Leave>", lambda event: on_leave(""))

    priceLabel3 = tk.Label(swFrame)
    priceLabel3.config(bg=black, fg=honey, text="Lab-Tec:", font=("Helvetica", 10))
    priceLabel3.grid(column=2, row=1)

    priceEntry3 = tk.Entry(swFrame)
    priceEntry3.config(bg=white, fg='black', font=("Helvetica", 10), width=25)
    priceEntry3.insert(0, "")
    priceEntry3.grid(column=3, row=1)
    priceEntry3.bind("<Enter>", lambda event: on_enter("Agrege el precio del analisis segun Lab-Tec"))
    priceEntry3.bind("<Leave>", lambda event: on_leave(""))

    detailsLabel = tk.Label(swFrame)
    detailsLabel.config(bg=black, fg=honey, text="Especificaciones", font=("Helvetica", 10))
    detailsLabel.grid(column=0, row=2)

    detailsEntry = tk.Entry(swFrame)
    detailsEntry.config(bg=white, fg='black', font=("Helvetica", 10), width=25)
    detailsEntry.insert(0, "")
    detailsEntry.grid(column=1, row=2)
    detailsEntry.bind("<Enter>", lambda event: on_enter("Agrege los detalles del análisis para el paciente"))
    detailsEntry.bind("<Leave>", lambda event: on_leave(""))

    deliveryLabel = tk.Label(swFrame)
    deliveryLabel.config(bg=black, fg=honey, text="Entrega", font=("Helvetica", 10))
    deliveryLabel.grid(column=2, row=2)

    deliveryEntry = tk.Entry(swFrame)
    deliveryEntry.config(bg=white, fg='black', font=("Helvetica", 10), width=25)
    deliveryEntry.insert(0, "")
    deliveryEntry.grid(column=3, row=2)
    deliveryEntry.bind("<Enter>", lambda event: on_enter("Agrega el tiempo en el que sera entregado el análisis"))
    deliveryEntry.bind("<Leave>", lambda event: on_leave(""))

    pushAddButton = tk.Button(swFrame)
    pushAddButton.config(bg=honey, text="Agregar", font=("Helvetica", 12), activebackground="#ef9659", width=20)
    pushAddButton.grid(column=3, row=3)
    pushAddButton.configure(command=lambda: addDataJson(nameEntry, priceEntry1, priceEntry2, priceEntry3, detailsEntry, deliveryEntry))
    pushAddButton.bind("<Enter>", lambda event: on_enter("Presione el boton para añadir los datos"))
    pushAddButton.bind("<Leave>", lambda event: on_leave(""))

    rutinaRes = IntVar()

    rutina = tk.Checkbutton(swFrame, text="Estudio de rutina?", variable=rutinaRes)
    rutina.config(background=black, fg=honey, font=("Helvetica", 10), activeforeground=honey, activebackground=black)
    rutina.grid(column=0, row=3)

    help = tk.Label(swFrame)
    help.config(bg=black, fg=honey, text="", font=("Helvetica", 14), height=5)
    help.grid(column=0, row=4, columnspan=4)


def ediFun():
    cont = 0
    nameAux = ""
    for widget in root.winfo_children():
        if cont > 0:
            widget.destroy()
        cont += 1
    stick.place(x=765)

    def hiddenText(text, obj):
        textH = obj.get()
        if textH == text:
            obj.delete(0, tk.END)
            obj.config(fg = 'black')
        elif textH == "":
            obj.insert(0,text)
            obj.config(fg = 'grey')

    def searchDataJson(name, pri1, pri2, pri3, d1, d2):
        jdata = None
        data = 'data.json' # Comprobar que exista el json
        salF = Path('.') / data
        with salF.open(encoding="utf-8", mode='r+') as fjson: # Abrir el json y cargarlo en la variable jdata
            jdata = json.load(fjson)

        aux = True
        for data in jdata["Data"]:
            if data[0].lower() == name.get().lower():
                auxHelp.config(text=name.get())
                aux = False
                pri1["state"] = "normal"
                pri2["state"] = "normal"
                pri3["state"] = "normal"
                d1["state"] = "normal"
                d2["state"] = "normal"
                rutina["state"] = "normal"
                pushChangeButton["state"] = "normal"
                delButton["state"] = "normal"

                name.delete(0, tk.END)
                pri1.delete(0, tk.END)
                pri2.delete(0, tk.END)
                pri3.delete(0, tk.END)
                d1.delete(0, tk.END)
                d2.delete(0, tk.END)


                pri1.config(fg="black")
                pri2.config(fg="black")
                pri3.config(fg="black")
                d1.config(fg="black")
                d2.config(fg="black")
                
                name.insert(0, data[0])
                pri1.insert(0, data[1])
                pri2.insert(0, data[2])
                pri3.insert(0, data[3])
                rutinaRes.set(data[4])
                if data[5] == "" and data[6] == "":
                    d1.insert(0, "Detalles del análisis")
                    d2.insert(0, "Entrega del análisis en días")
                    d1.config(fg="gray")
                    d2.config(fg="gray")
                elif data[5] == "":
                    d1.insert(0, "Detalles del análisis")
                    d2.insert(0, data[6])
                    d1.config(fg="gray")
                elif data [6] == "":
                    d1.insert(0, data[5])
                    d2.insert(0, "Entrega del análisis en días")
                    d2.config(fg="gray")
                else:
                    d1.insert(0, data[5])
                    d2.insert(0, data[6])
        
        if aux:
            help.config(text="No existe ese analisis en la base de datos")
        
    def changeDataJson(name, pri1, pri2, pri3, d1, d2):
        jdata = None
        data = 'data.json' # Comprobar que exista el json
        salF = Path('.') / data
        with salF.open(encoding="utf-8", mode='r+') as fjson: # Abrir el json y cargarlo en la variable jdata
            jdata = json.load(fjson)

        try:
            if name.get() != "":
                for data in jdata["Data"]:
                    if data[0].lower() == auxHelp.cget("text").lower():
                    
                        data[0] = name.get()
                        data[1] = float(pri1.get())
                        data[2] = pri2.get()
                        data[3] = pri3.get()
                        data[4] = rutinaRes.get()
                        data[5] = d1.get()
                        data[6] = d2.get()

                        name.delete(0, tk.END)
                        pri1.delete(0, tk.END)
                        pri2.delete(0, tk.END)
                        pri3.delete(0, tk.END)
                        d1.delete(0, tk.END)
                        d2.delete(0, tk.END)

                        pri1.insert(0, "Precio numerico")
                        pri2.insert(0, "Precio numerico")
                        pri3.insert(0, "Precio numerico")
                        d1.insert(0, "Detalles del análisis")
                        d2.insert(0, "Entrega del análisis en días")
                        
                        pri1['state'] = 'disabled'
                        pri2['state'] = 'disabled'
                        pri3['state'] = 'disabled'
                        d1['state'] = 'disabled'
                        d2['state'] = 'disabled'
                        rutina['state'] = 'disabled'
                        pushChangeButton["state"] = 'disabled'
                        delButton["state"] = 'disabled'

                        help.config(text="Los datos del análisis: "+auxHelp.cget("text")+" han sido actualizados")
                    
                exit = Path(".") / "data.json"
                with exit.open('w', encoding="utf-8") as ex:
                    ex.write(json.dumps(jdata))
            
            else:
                help.config(text="Por favor ingrese un nombre valido para el análisis")

        except ValueError:
            help.config(text="Por favor ingrese datos numericos en los precios")

    def delDataJson(name, pri1, pri2, pri3, d1, d2):
        jdata = None
        data = 'data.json' # Comprobar que exista el json
        salF = Path('.') / data
        with salF.open(encoding="utf-8", mode='r+') as fjson: # Abrir el json y cargarlo en la variable jdata
            jdata = json.load(fjson)
        
        deldata = [name.get(), float(pri1.get()), pri2.get(), pri3.get(), rutinaRes.get(), d1.get(), d2.get()]

        jdata['Data'].pop(jdata['Data'].index(deldata))

        exit = Path(".") / "data.json"
        with exit.open('w', encoding="utf-8") as ex:
            ex.write(json.dumps(jdata))
        
        name.delete(0, tk.END)
        pri1.delete(0, tk.END)
        pri2.delete(0, tk.END)
        pri3.delete(0, tk.END)
        d1.delete(0, tk.END)
        d2.delete(0, tk.END)

        pri1.insert(0, "Precio numerico")
        pri2.insert(0, "Precio numerico")
        pri3.insert(0, "Precio numerico")
        d1.insert(0, "Detalles del análisis")
        d2.insert(0, "Entrega del análisis en días")

        pri1['state'] = 'disabled'
        pri2['state'] = 'disabled'
        pri3['state'] = 'disabled'
        d1['state'] = 'disabled'
        d2['state'] = 'disabled'
        rutina['state'] = 'disabled'
        pushChangeButton["state"] = 'disabled'
        delButton["state"] = 'disabled'

        help.config(text="análisis eliminado de manera correcta")

    # Funciones de los botones
    def on_enter(text):
        help.config(text=text)

    def on_leave(text):
        help.config(text=text)
    
    swFrame = tk.Frame(root, bg=black, bd=20, width=300)
    swFrame.pack(fill=tk.BOTH, expand=True, side='left')

    swFrame.columnconfigure([0,1,2,3], weight=1)
    swFrame.rowconfigure([0,1,2,3,4], weight=1)

    auxHelp = tk.Label(swFrame)
    auxHelp.config(bg=black, fg=black, text="", font=("Helvetica", 6))
    auxHelp.grid(column=0, row=0)

    nameLabel = tk.Label(swFrame)
    nameLabel.config(bg=black, fg=honey, text="Analisis a buscar:", font=("Helvetica", 10))
    nameLabel.grid(column=0, row=0)

    nameEntry = tk.Entry(swFrame)
    nameEntry.config(bg=white, fg='grey', font=("Helvetica", 10), width=25)
    nameEntry.insert(0, "Analisis a buscar")
    nameEntry.grid(column=1, row=0)
    nameEntry.bind("<FocusIn>", lambda event: hiddenText("Analisis a buscar", nameEntry))
    nameEntry.bind("<FocusOut>", lambda event: hiddenText("Analisis a buscar", nameEntry))
    nameEntry.bind("<Enter>", lambda event: on_enter("Agrege el nombre del analisis que desea modificar, si quiere modificar el nombre\nsimplemente una vez buscado edite el campo del nombre y dele al boton de modificar"))
    nameEntry.bind("<Leave>", lambda event: on_leave(""))

    priceLabel1 = tk.Label(swFrame)
    priceLabel1.config(bg=black, fg=honey, text="Precio Publico:", font=("Helvetica", 10))
    priceLabel1.grid(column=2, row=0)

    priceEntry1 = tk.Entry(swFrame)
    priceEntry1.config(bg=white, fg='grey', font=("Helvetica", 10), width=25)
    priceEntry1.insert(0, "Precio numerico")
    priceEntry1.grid(column=3, row=0)
    priceEntry1.bind("<FocusIn>", lambda event: hiddenText("Precio numerico", priceEntry1))
    priceEntry1.bind("<FocusOut>", lambda event: hiddenText("Precio numerico", priceEntry1))
    priceEntry1.bind("<Enter>", lambda event: on_enter("Modifique el precio publico del análisis"))
    priceEntry1.bind("<Leave>", lambda event: on_leave(""))
    priceEntry1["state"] = "disabled"

    priceLabel2 = tk.Label(swFrame)
    priceLabel2.config(bg=black, fg=honey, text="Micro-Tec:", font=("Helvetica", 10))
    priceLabel2.grid(column=0, row=1)

    priceEntry2 = tk.Entry(swFrame)
    priceEntry2.config(bg=white, fg='grey', font=("Helvetica", 10), width=25)
    priceEntry2.insert(0, "Precio numerico")
    priceEntry2.grid(column=1, row=1)
    priceEntry2.bind("<FocusIn>", lambda event: hiddenText("Precio numerico", priceEntry2))
    priceEntry2.bind("<FocusOut>", lambda event: hiddenText("Precio numerico", priceEntry2))
    priceEntry2.bind("<Enter>", lambda event: on_enter("Modifique el precio del análisis segun Micro-Tec"))
    priceEntry2.bind("<Leave>", lambda event: on_leave(""))
    priceEntry2["state"] = "disabled"

    priceLabel3 = tk.Label(swFrame)
    priceLabel3.config(bg=black, fg=honey, text="Lab-Tec:", font=("Helvetica", 10))
    priceLabel3.grid(column=2, row=1)

    priceEntry3 = tk.Entry(swFrame)
    priceEntry3.config(bg=white, fg='grey', font=("Helvetica", 10), width=25)
    priceEntry3.insert(0, "Precio numerico")
    priceEntry3.grid(column=3, row=1)
    priceEntry3.bind("<FocusIn>", lambda event: hiddenText("Precio numerico", priceEntry3))
    priceEntry3.bind("<FocusOut>", lambda event: hiddenText("Precio numerico", priceEntry3))
    priceEntry3.bind("<Enter>", lambda event: on_enter("Modifique el precio del análisis segun Lab-Tec"))
    priceEntry3.bind("<Leave>", lambda event: on_leave(""))
    priceEntry3["state"] = "disabled"

    detailsLabel = tk.Label(swFrame)
    detailsLabel.config(bg=black, fg=honey, text="Especificaciones:", font=("Helvetica", 10))
    detailsLabel.grid(column=0, row=2)

    detailsEntry = tk.Entry(swFrame)
    detailsEntry.config(bg=white, fg='grey', font=("Helvetica", 10), width=25)
    detailsEntry.insert(0, "Detalles del análisis")
    detailsEntry.grid(column=1, row=2)
    detailsEntry.bind("<FocusIn>", lambda event: hiddenText("Detalles del análisis", detailsEntry))
    detailsEntry.bind("<FocusOut>", lambda event: hiddenText("Detalles del análisis", detailsEntry))
    detailsEntry.bind("<Enter>", lambda event: on_enter("Modifique los detalles del análisis"))
    detailsEntry.bind("<Leave>", lambda event: on_leave(""))
    detailsEntry["state"] = "disabled"

    deliveryLabel = tk.Label(swFrame)
    deliveryLabel.config(bg=black, fg=honey, text="Entrega:", font=("Helvetica", 10))
    deliveryLabel.grid(column=2, row=2)

    deliveryEntry = tk.Entry(swFrame)
    deliveryEntry.config(bg=white, fg='grey', font=("Helvetica", 10), width=25)
    deliveryEntry.insert(0, "Entrega del análisis en días")
    deliveryEntry.grid(column=3, row=2)
    deliveryEntry.bind("<FocusIn>", lambda event: hiddenText("Entrega del análisis en días", deliveryEntry))
    deliveryEntry.bind("<FocusOut>", lambda event: hiddenText("Entrega del análisis en días", deliveryEntry))
    deliveryEntry.bind("<Enter>", lambda event: on_enter("Modifique el tiempo de entrega del análisis"))
    deliveryEntry.bind("<Leave>", lambda event: on_leave(""))
    deliveryEntry["state"] = "disabled"

    pushSearchButton = tk.Button(swFrame)
    pushSearchButton.config(bg=honey, text="Buscar", font=("Helvetica", 12), activebackground="#ef9659", width=20)
    pushSearchButton.grid(column=3, row=3)
    pushSearchButton.configure(command=lambda: searchDataJson(nameEntry, priceEntry1, priceEntry2, priceEntry3, detailsEntry, deliveryEntry))
    pushSearchButton.bind("<Enter>", lambda event: on_enter("Presione el boton para buscar el analisis"))
    pushSearchButton.bind("<Leave>", lambda event: on_leave(""))

    pushChangeButton = tk.Button(swFrame)
    pushChangeButton.config(bg=honey, text="Modificar", font=("Helvetica", 12), activebackground="#ef9659", width=20)
    pushChangeButton.grid(column=2, row=3)
    pushChangeButton.configure(command=lambda: changeDataJson(nameEntry, priceEntry1, priceEntry2, priceEntry3, detailsEntry, deliveryEntry))
    pushChangeButton.bind("<Enter>", lambda event: on_enter("Presione el boton para modificar los datos"))
    pushChangeButton.bind("<Leave>", lambda event: on_leave(""))
    pushChangeButton["state"] = "disabled"

    delButton = tk.Button(swFrame)
    delButton.config(bg=honey, text="Eliminar", font=("Helvetica", 12), activebackground="#ef9659", width=20)
    delButton.grid(column=1, row=3)
    delButton.configure(command=lambda: delDataJson(nameEntry, priceEntry1, priceEntry2, priceEntry3, detailsEntry, deliveryEntry))
    delButton.bind("<Enter>", lambda event: on_enter("Presione el boton para eliminar el análisis de la base de datos"))
    delButton.bind("<Leave>", lambda event: on_leave(""))
    delButton["state"] = "disabled"

    rutinaRes = IntVar()

    rutina = tk.Checkbutton(swFrame, text="Estudio de rutina?", variable=rutinaRes)
    rutina.config(background=black, fg=honey, font=("Helvetica", 10), activeforeground=honey, activebackground=black)
    rutina.grid(column=0, row=3)
    rutina["state"] = "disabled"

    help = tk.Label(swFrame)
    help.config(bg=black, fg=honey, text="", font=("Helvetica", 14), height=5)
    help.grid(column=0, row=4, columnspan=4)

#colores y variables

white = "#ffffff"
brown = "#aa7b43"
black = "#ffffff"#000000
honey = "#4a67dc"#fcb258

#Configuraciones iniciales del root #'../img/taigaR.png'
logo = tk.PhotoImage(file = 'img/kumoko.png') #'env/img/taigaR.png' esta ruta es para poder correrlo desde aqui, la que esta es para el instalador
root.iconphoto(False, logo, logo)

root.geometry('960x643+297+33')
root.minsize(960,643)
root.resizable(0,0)
root.config(bg = "#d7d9d8")
root.title("CotizaLab")

#Menu Switcheable
    #Instancias
menuFrame = tk.Frame(root, bg=honey)
cotiButton = tk.Button(menuFrame, text="Cotizador", font=("Helvetica", 13), bd=0, fg=black, 
                       activeforeground=black, background=honey)

addButton = tk.Button(menuFrame, text="Añadir", font=("Helvetica", 13), bd=0, fg=black, 
                       activeforeground=black, background=honey)

ediButton = tk.Button(menuFrame, text="Editar", font=("Helvetica", 13), bd=0, fg=black, 
                       activeforeground=black, background=honey)
stick = tk.Label(menuFrame, bg=black)

    #Configuraciones de las instancias
menuFrame.columnconfigure([0,1,2], weight=1)
menuFrame.rowconfigure([0], weight=1)
menuFrame.pack(side=tk.TOP, fill=tk.X)
menuFrame.pack_propagate(False)
menuFrame.config(height=35, pady=10)

cotiButton.grid(column=0, row=0)
cotiButton.configure(command=cotiFun, activebackground=honey)

addButton.grid(column=1, row=0)
addButton.configure(command=addFun, activebackground=honey)

ediButton.grid(column=2, row=0)
ediButton.configure(command=ediFun, activebackground=honey)

stick.place(x=127, y=30, width=80, height=2)

#Cotizador Frame

#Iniciamos con cotizador
cotiFun()

root.mainloop()