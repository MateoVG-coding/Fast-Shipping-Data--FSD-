import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
import pygame
from PIL import ImageTk, Image
import FSD_FUNCIONES as fsdF
import FSD_ESTADISTICAS as fsdE




def App():

    #---------------------------ROOT----------------------------------------------------------
    root=tk.Tk()
    root.state("zoomed")
    root.title("Fast Shipping Data (FSD)")
    root.iconbitmap("icons/ICON_FSD.ico")
    root.config(bg="gray40", relief="groove")

    MyNotebook=ttk.Notebook(root)

    fsdF.ConectarBBDD()

    pygame.mixer.init()

    pygame.mixer.music.load("resources/SONIDO_FSD.mp3")
    pygame.mixer.music.play(loops=0)





    #--------------------------------------STYLES---------------------------------------------------------

    fontLabel=tkFont.Font(family="Bahnschrift Light", size=16, slant="roman", weight="bold")

    styleNotebookTab=ttk.Style()
    settingsNoteBook={"TNotebook.Tab": {"configure": {"padding": [8,8],"font": ("Bahnschrift Light",12), "background": "deep sky blue3"}, 
                        "map": {"background": [("selected", "gray40")],
                                "foreground": [("selected", "white"), ("active", "white")]
                                }}} 

    styleNotebookTab.theme_create("TNotebook.Tab", parent="clam", settings=settingsNoteBook)
    styleNotebookTab.theme_use("TNotebook.Tab")

    StyleBtMain=ttk.Style()
    StyleBtMain.configure("TButton",foreground="black", background="deep sky blue3", anchor="center",
    font=fontLabel, width=10, padding=2, relief="raised", borderwidth=4)
    StyleBtMain.map("TButton", background=[('active', 'white')])




    #----------------------------------------------------IMAGES------------------------------------------

    img_check = ImageTk.PhotoImage(Image.open('icons/checkbox.png'))

    img_uncheck = ImageTk.PhotoImage(Image.open('icons/uncheckbox.png'))
    
    img_eraser = ImageTk.PhotoImage(Image.open('icons/eraser.png'))

    img_glass= ImageTk.PhotoImage(Image.open('icons/magnifiGlass.png'))

    img_pin= ImageTk.PhotoImage(Image.open('icons/pin.png'))

    img_client= ImageTk.PhotoImage(Image.open('icons/client.png'))

    img_reload= ImageTk.PhotoImage(Image.open('icons/reload.png'))








    #-------------------------------------WINDOW COP/PAST/CUT--------------------------------------------

    class ComboboxPlus(ttk.Combobox):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.menu =tk.Menu(self, tearoff=0, activebackground="deep sky blue3", activeforeground="black")
            self.menu.add_command(label="Copiar" + " "*15 + "Ctrl + C", command=self.popup_copy)
            self.menu.add_command(label="Cortar" + " "*15 + "Ctrl + X", command=self.popup_cut)
            self.menu.add_separator()
            self.menu.add_command(label="Pegar" + " "*15 + "Ctrl + V", command=self.popup_paste)
            self.bind("<Button-3>", self.display_popup)
        
        def display_popup(self, event):
            self.menu.post(event.x_root, event.y_root)
        
        def popup_copy(self):
            self.event_generate("<<Copy>>")
        def popup_cut(self):
            self.event_generate("<<Cut>>")
        def popup_paste(self):
            self.event_generate("<<Paste>>")

    class EntryPlus(ttk.Entry):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.menu =tk.Menu(self, tearoff=0, activebackground="deep sky blue3", activeforeground="black")
            self.menu.add_command(label="Copiar" + " "*15 + "Ctrl + C", command=self.popup_copy)
            self.menu.add_command(label="Cortar" + " "*15 + "Ctrl + X", command=self.popup_cut)
            self.menu.add_separator()
            self.menu.add_command(label="Pegar" + " "*15 + "Ctrl + V", command=self.popup_paste)
            self.bind("<Button-3>", self.display_popup)
        
        def display_popup(self, event):
            self.menu.post(event.x_root, event.y_root)
        
        def popup_copy(self):
            self.event_generate("<<Copy>>")
        def popup_cut(self):
            self.event_generate("<<Cut>>")
        def popup_paste(self):
            self.event_generate("<<Paste>>")

    class TextPlus(tk.Text):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.menu =tk.Menu(self, tearoff=0, activebackground="deep sky blue3", activeforeground="black")
            self.menu.add_command(label="Copiar" + " "*15 + "Ctrl + C", command=self.popup_copy)
            self.menu.add_command(label="Cortar" + " "*15 + "Ctrl + X", command=self.popup_cut)
            self.menu.add_separator()
            self.menu.add_command(label="Pegar" + " "*15 + "Ctrl + V", command=self.popup_paste)
            self.bind("<Button-3>", self.display_popup)
        
        def display_popup(self, event):
            self.menu.post(event.x_root, event.y_root)
        
        def popup_copy(self):
            self.event_generate("<<Copy>>")
        def popup_cut(self):
            self.event_generate("<<Cut>>")
        def popup_paste(self):
            self.event_generate("<<Paste>>")


    #--------------------------MENU------------------------------------------------------------

    BarraMenu=tk.Menu(root)
    root.config(menu=BarraMenu)

    Inicio=tk.Menu(BarraMenu, tearoff=0, activebackground="deep sky blue3", activeforeground="black")
    Inicio.add_command(label="Insertar", command=lambda:fsdF.InsertarTabla(TextDomDiario,TextTotal,listEntry,TreeViewDay,TreeViewTab,TextPendientes,TextEntregados))
    Inicio.add_separator()
    Inicio.add_command(label="Salir", command=lambda:fsdF.SalirDeApp(root))

    Borrar=tk.Menu(BarraMenu, tearoff=0, activebackground="deep sky blue3", activeforeground="black")
    Borrar.add_command(label="Domicilios diarios", command=lambda:fsdF.EliminarTabla("DOMICILIOS DIARIOS", TextDomDiario,TextTotal,textClient,listEntry,TreeViewDay,TextPendientes,TextEntregados))
    Borrar.add_command(label="Domicilios totales", command=lambda:fsdF.EliminarTabla("DOMICILIOS TOTALES", TextDomDiario,TextTotal,textClient,listEntry,TreeViewTab))
    Borrar.add_command(label="Clientes", command=lambda:fsdF.EliminarTabla("CLIENTES", TextDomDiario,TextTotal,textClient,listEntry,TViewTabClient))


    Ayuda=tk.Menu(BarraMenu, tearoff=0, activebackground="deep sky blue3", activeforeground="black")
    Ayuda.add_command(label="Documentación", command=fsdF.MostrarDocum)
    Ayuda.add_command(label="Contacto", command=fsdF.MostrarContacto)
    Ayuda.add_command(label="Licencia", command=fsdF.MostrarLicencia)
    Ayuda.add_command(label="Sobre FSD", command=fsdF.MostrarVersion)

    BarraMenu.add_cascade(label="Inicio", menu=Inicio)
    BarraMenu.add_cascade(label="Eliminar", menu=Borrar)
    BarraMenu.add_cascade(label="Ayuda", menu=Ayuda)








    #----------------------------MAIN FRAME--------------------------------------------------------

    FrameRegistros=tk.Frame(MyNotebook)
    FrameRegistros.config(bg="gray40", pady=5)
    FrameRegistros.pack()

    FrameRegistros.columnconfigure((0,1,2,3,4), weight=1)
    FrameRegistros.rowconfigure((0,1,2,3,4,5,6,7), weight=1)

    TextEntryID=tk.StringVar(value="-----------------------------")
    TextEntryClient=tk.StringVar()
    TextEntryPhone=tk.StringVar()
    TextEntryAdressPick=tk.StringVar()
    TextEntryAdressDelv=tk.StringVar()
    TextEntryDelv=tk.StringVar()
    TextEntryServ=tk.StringVar()
    TextEntryPrice=tk.DoubleVar()

    ListText=[TextEntryID,TextEntryClient,TextEntryPhone,TextEntryAdressPick,
    TextEntryAdressDelv,TextEntryDelv,TextEntryServ,TextEntryPrice]


    #----------------------LABELS MAIN FRAME-------------------------------------------------------------------

    labID=tk.Label(FrameRegistros, text="ID:", font=fontLabel)
    labID.grid(column=0, row=0, sticky="w", padx=50)
    labID.config(foreground="black", background="gray40")

    labClient=tk.Label(FrameRegistros, text="Cliente:", font=fontLabel)
    labClient.grid(column=0, row=1, sticky="w", padx=50)
    labClient.config(foreground="black", background="gray40")

    labPhone=tk.Label(FrameRegistros, text="Teléfono:", font=fontLabel)
    labPhone.grid(column=0, row=2, sticky="w", padx=50)
    labPhone.config(foreground="black", background="gray40")

    labAdressPick=tk.Label(FrameRegistros, text="Dirección a recoger:", font=fontLabel)
    labAdressPick.grid(column=0, row=3, sticky="w", padx=50)
    labAdressPick.config(foreground="black", background="gray40", justify="center")

    labAdressDelv=tk.Label(FrameRegistros, text="Dirección a entregar:", font=fontLabel)
    labAdressDelv.grid(column=0, row=4, sticky="w")
    labAdressDelv.config(foreground="black", background="gray40", padx=50)

    LabDelv=tk.Label(FrameRegistros, text="Mensajero: ", font=fontLabel)
    LabDelv.grid(column=0, row=5, sticky="w", padx=50)
    LabDelv.config(foreground="black", background="gray40")

    labServ=tk.Label(FrameRegistros, text="Tipo de servicio:", font=fontLabel)
    labServ.grid(column=0, row=6, sticky="w", padx=50)
    labServ.config(foreground="black", background="gray40")

    labPrice=tk.Label(FrameRegistros, text="Precio:", font=fontLabel)
    labPrice.grid(column=2, row=0, sticky="w", padx=120)
    labPrice.config(foreground="black", background="gray40")

    labObs=tk.Label(FrameRegistros, text="Descripción:", font=fontLabel)
    labObs.grid(column=2, row=1, sticky="ew")
    labObs.config(foreground="black", background="gray40")

    LabDomiciliosPend=tk.Label(FrameRegistros, text="🔵 DOMICILIOS PENDIENTES:", font=fontLabel, width=25)
    LabDomiciliosPend.grid(column=3, row=5, sticky="w")
    LabDomiciliosPend.config(foreground="deep sky blue2", background="gray40")

    TextPendientes=tk.StringVar()
    labServiceTotal=tk.Label(FrameRegistros, textvariable=TextPendientes, font=fontLabel)
    labServiceTotal.grid(column=3, row=5, sticky="e")
    labServiceTotal.config(foreground="black", background="gray40")

    LabDomiciliosEntreg=tk.Label(FrameRegistros, text="🔵 DOMICILIOS ENTREGADOS:", font=fontLabel, width=25)
    LabDomiciliosEntreg.grid(column=3, row=6, sticky="w")
    LabDomiciliosEntreg.config(foreground="deep sky blue2", background="gray40")

    TextEntregados=tk.StringVar()
    labServiceTotal=tk.Label(FrameRegistros, textvariable=TextEntregados, font=fontLabel)
    labServiceTotal.grid(column=3, row=6, sticky="e")
    labServiceTotal.config(foreground="black", background="gray40")

    fsdF.entregadoOrPendiente(TextPendientes,TextEntregados)



    #-----------------------COMBOBOX/TEXT MAIN FRAME------------------------------------------------

    EntryID=ComboboxPlus(FrameRegistros, textvariable=TextEntryID, height=5)
    EntryID.grid(column=1, row=0, ipady=8, sticky="we")
    EntryID.config(justify="center")

    EntryClient=ComboboxPlus(FrameRegistros, textvariable=TextEntryClient, height=5)
    EntryClient.grid(column=1, row=1, ipady=8, sticky="we")
    EntryClient.config(justify="center")

    EntryPhone=ComboboxPlus(FrameRegistros, textvariable=TextEntryPhone, height=5)
    EntryPhone.grid(column=1, row=2,  ipady=8, sticky="we")
    EntryPhone.config(justify="center")
     
    EntryAdressPick=ComboboxPlus(FrameRegistros, textvariable=TextEntryAdressPick, height=5)
    EntryAdressPick.grid(column=1, row=3, ipady=8, sticky="we")
    EntryAdressPick.config(justify="center")

    EntryAdressDelv=ComboboxPlus(FrameRegistros, textvariable=TextEntryAdressDelv, height=5)
    EntryAdressDelv.grid(column=1, row=4, ipady=8, sticky="we")
    EntryAdressDelv.config(justify="center")

    EntryDelv=ComboboxPlus(FrameRegistros, textvariable=TextEntryDelv, height=5)
    EntryDelv.grid(column=1, row=5, ipady=8, sticky="we")
    EntryDelv.config(justify="center")

    EntryServ=ComboboxPlus(FrameRegistros, textvariable=TextEntryServ)
    EntryServ["values"]=["ENVÍO","CONSIGNACIÓN","COMPRA","PAGO"]
    EntryServ.grid(column=1, row=6, ipady=8, sticky="we")
    EntryServ.config(justify="center")

    EntryPrice=EntryPlus(FrameRegistros, textvariable=TextEntryPrice)
    EntryPrice.grid(column=3, row=0, pady=8, ipady=8, sticky="we")
    EntryPrice.config(justify="center")

    TextObs=TextPlus(FrameRegistros, width=10, height=1)
    TextObs.grid(column=3, row=1, ipady=8, sticky="wens", rowspan=3)
    scrollVert=tk.Scrollbar(FrameRegistros, command=TextObs.yview)
    scrollVert.place(in_=TextObs, relx=1, relheight=1, bordermode="outside")
    TextObs.config(yscrollcommand=scrollVert.set, font=("Arial", 11), selectbackground="black")


    listEntry=[EntryID,EntryClient,EntryPhone,EntryAdressPick,EntryAdressDelv,
    EntryDelv,EntryServ,EntryPrice]

    fsdF.ValoresCombobox(listEntry)


    #----------------------------BUTTONS MAIN FRAME------------------------------------------

    botonCrear=ttk.Button(FrameRegistros, text="Crear",  command=lambda:fsdF.CrearRegistro(ListText,listEntry,TextObs,TextDomDiario,TreeViewDay,TextPendientes,TextEntregados))
    botonCrear.grid(column=0, row=7, padx=20, pady=5, ipadx=15)
    botonCrear.config(cursor="hand2")

    botonLeer=ttk.Button(FrameRegistros, text="Buscar",  command=lambda:fsdF.LeerRegistro(ListText,TextObs))
    botonLeer.grid( column=1, row=7, padx=20, pady=5, ipadx=15)
    botonLeer.config(cursor="hand2")

    botonActualizar=ttk.Button(FrameRegistros, text="Actualizar",  command=lambda:fsdF.ActualizarRegistro(listEntry,TextObs,ListText,TreeViewDay))
    botonActualizar.grid(column=2, row=7, padx=20, pady=5, ipadx=15)
    botonActualizar.config(cursor="hand2")

    botonEliminar=ttk.Button(FrameRegistros, text="Eliminar",  command=lambda:fsdF.EliminarRegistro(TextEntryID, TextDomDiario, ListText, TextObs, listEntry,TreeViewDay,TextPendientes,TextEntregados))
    botonEliminar.grid(column=3, row=7, padx=20, pady=5, ipadx=15)
    botonEliminar.config(cursor="hand2")

    ButtonPrice=ttk.Button(FrameRegistros, image=img_pin, command=lambda:fsdF.FijarPrecio(TextEntryPrice))
    ButtonPrice.grid(column=4, row=0, sticky="w", padx=10)
    ButtonPrice.config(cursor="hand2")

    ButtonClient=ttk.Button(FrameRegistros, image=img_client, command=lambda:fsdF.ClienteReg(TextEntryClient, ListText))
    ButtonClient.grid(column=2, row=1, sticky="w", padx=15)
    ButtonClient.config(cursor="hand2")

    ButtonPend=ttk.Button(FrameRegistros, image=img_glass, command=lambda:fsdF.TreeViewPend(fontLabel,TextPendientes,TextEntregados,TreeViewDay))
    ButtonPend.grid(column=4, row=5, padx=10)
    ButtonPend.config(cursor="hand2")

    ButtonBorrCampos=ttk.Button(FrameRegistros, image=img_eraser, command=lambda:fsdF.BorrarCampos(ListText, TextObs))
    ButtonBorrCampos.grid(column=3, row=4, padx=3, pady=10, sticky="e", ipadx=15)
    ButtonBorrCampos.config(cursor="hand2")







    #---------------------------FRAME TABLES VIEWER---------------------------------------------

    FrameTablesView=tk.Frame(MyNotebook)
    FrameTablesView.config(bg="gray40", pady=6)
    FrameTablesView.columnconfigure((0,1,2,3,4), weight=1)
    FrameTablesView.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
    FrameTablesView.pack()


    #----------------------LABELS TABLES VIEWER-------------------------------------------------------------------

    labIDTab=tk.Label(FrameTablesView, text="ID:", font=fontLabel)
    labIDTab.grid(column=0, row=0, pady=8, sticky="w", padx=50)
    labIDTab.config(foreground="black", background="gray40")

    labClientTab=tk.Label(FrameTablesView, text="Cliente:", font=fontLabel)
    labClientTab.grid(column=2, row=0, pady=8, sticky="w", padx=50)
    labClientTab.config(foreground="black", background="gray40")

    labPhoneTab=tk.Label(FrameTablesView, text="Teléfono:", font=fontLabel)
    labPhoneTab.grid(column=0, row=1, pady=8, sticky="w", padx=50)
    labPhoneTab.config(foreground="black", background="gray40")

    LabDelvTab=tk.Label(FrameTablesView, text="Mensajero: ", font=fontLabel)
    LabDelvTab.grid(column=2, row=1, pady=8, sticky="w", padx=50)
    LabDelvTab.config(foreground="black", background="gray40")

    labAdressPickTab=tk.Label(FrameTablesView, text="Dirección a recoger:", font=fontLabel)
    labAdressPickTab.grid(column=0, row=2, pady=8, sticky="w", padx=50)
    labAdressPickTab.config(foreground="black", background="gray40")

    labAdressDelvTab=tk.Label(FrameTablesView, text="Dirección a entregar:", font=fontLabel)
    labAdressDelvTab.grid(column=2, row=2, pady=8, sticky="w", padx=50)
    labAdressDelvTab.config(foreground="black", background="gray40")

    labServTab=tk.Label(FrameTablesView, text="Tipo de servicio:", font=fontLabel)
    labServTab.grid(column=0, row=3, pady=8, sticky="w", padx=50)
    labServTab.config(foreground="black", background="gray40")

    labPriceTab=tk.Label(FrameTablesView, text="Precio:", font=fontLabel)
    labPriceTab.grid(column=2, row=3, pady=8, sticky="w", padx=50)
    labPriceTab.config(foreground="black", background="gray40")

    labTableTab=tk.Label(FrameTablesView, text="Tabla:", font=fontLabel)
    labTableTab.grid(column=0, row=4, pady=8, sticky="w", padx=50)
    labTableTab.config(foreground="black", background="gray40")

    labEstadoTab=tk.Label(FrameTablesView, text="Estado:", font=fontLabel)
    labEstadoTab.grid(column=2, row=4, pady=8, sticky="w", padx=50)
    labEstadoTab.config(foreground="black", background="gray40")

    labFechaInicial=tk.Label(FrameTablesView, text="Desde:", font=fontLabel)
    labFechaInicial.grid(column=0, row=5, pady=8, sticky="w", padx=50)
    labFechaInicial.config(foreground="black", background="gray40")

    labFechaFin=tk.Label(FrameTablesView, text="Hasta:", font=fontLabel)
    labFechaFin.grid(column=2, row=5, pady=8, sticky="w", padx=50)
    labFechaFin.config(foreground="black", background="gray40")



    #-----------------------COMBOBOX/TEXT TABLES FRAME------------------------------------------------

    EntryIDTab=EntryPlus(FrameTablesView)
    EntryIDTab.grid(column=1, row=0, pady=8, ipady=8, sticky="we")
    EntryIDTab.config(justify="center")

    EntryClientTab=EntryPlus(FrameTablesView)
    EntryClientTab.grid(column=3, row=0, pady=8, ipady=8, sticky="we")
    EntryClientTab.config(justify="center")

    EntryPhoneTab=EntryPlus(FrameTablesView)
    EntryPhoneTab.grid(column=1, row=1, pady=8, ipady=8, sticky="we")
    EntryPhoneTab.config(justify="center")

    EntryDelvTab=EntryPlus(FrameTablesView)
    EntryDelvTab.grid(column=3, row=1, pady=8, ipady=8, sticky="we")
    EntryDelvTab.config(justify="center")

    EntryAdressPickTab=EntryPlus(FrameTablesView)
    EntryAdressPickTab.grid(column=1, row=2, pady=8, ipady=8, sticky="we")
    EntryAdressPickTab.config(justify="center")

    EntryAdressDelvTab=EntryPlus(FrameTablesView)
    EntryAdressDelvTab.grid(column=3, row=2, pady=8, ipady=8, sticky="we")
    EntryAdressDelvTab.config(justify="center")
    
    EntryServTab=ComboboxPlus(FrameTablesView)
    EntryServTab["values"]=["ENVÍO","CONSIGNACIÓN","COMPRA","PAGO"]
    EntryServTab.grid(column=1, row=3, pady=8, ipady=8, sticky="we")
    EntryServTab.config(justify="center")

    EntryPriceTab=EntryPlus(FrameTablesView)
    EntryPriceTab.grid(column=3, row=3, pady=8, ipady=8, sticky="we")
    EntryPriceTab.config(justify="center")

    EntryTable=ComboboxPlus(FrameTablesView, state="readonly")
    EntryTable["values"]=["DOMICILIOS DIARIOS", "DOMICILIOS TOTALES"]
    EntryTable.grid(column=1, row=4, pady=8, ipady=8, sticky="we")
    EntryTable.config(justify="center")

    StringEstado=tk.StringVar(value='TODOS')
    EntryEstado=ComboboxPlus(FrameTablesView, state="readonly", textvariable=StringEstado)
    EntryEstado["values"]=["TODOS","ENTREGADO", "PENDIENTE"]
    EntryEstado.grid(column=3, row=4, pady=8, ipady=8, sticky="we")
    EntryEstado.config(justify="center")

    StringYearInic=tk.StringVar(value="YYYY")
    YearInic=ComboboxPlus(FrameTablesView, height=5 , state="readonly", width=4, textvariable=StringYearInic)
    YearInic["values"]=["2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033","2034","2035"]
    YearInic.grid(column=0, row=5, padx=60, ipadx=5, ipady=8, sticky="e")
    YearInic.config(justify="center")

    StringMonthInic=tk.StringVar(value="MM")
    MonthInic=ComboboxPlus(FrameTablesView,height=5 , state="readonly", width=4, textvariable=StringMonthInic)
    MonthInic["values"]=["01","02","03","04","05","06","07","08","09","10","11","12"]
    MonthInic.grid(column=1, row=5, ipadx=5, ipady=8, sticky="w")
    MonthInic.config(justify="center")

    StringDayInic=tk.StringVar(value="DD")
    DayInic=ComboboxPlus(FrameTablesView, height=5 , state="readonly", width=4, textvariable=StringDayInic)
    DayInic["values"]=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    DayInic.grid(column=1, row=5, ipadx=5, ipady=8)
    DayInic.config(justify="center")

    StringHourInic=tk.StringVar(value="HH")
    HourInic=ComboboxPlus(FrameTablesView, height=5 , state="readonly", width=4, textvariable=StringHourInic)
    HourInic["values"]=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
    HourInic.grid(column=1, row=5, ipadx=5, ipady=8, sticky="e")
    HourInic.config(justify="center")

    StringYearFin=tk.StringVar(value="YYYY")
    YearFin=ComboboxPlus(FrameTablesView, height=5 , state="readonly", width=4, textvariable=StringYearFin)
    YearFin["values"]=["2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033","2034","2035"]
    YearFin.grid(column=2, row=5, padx=60, ipadx=5, ipady=8, sticky="e")
    YearFin.config(justify="center")

    StringMonthFin=tk.StringVar(value="MM")
    MonthFin=ComboboxPlus(FrameTablesView,height=5 , state="readonly", width=4, textvariable=StringMonthFin)
    MonthFin["values"]=["01","02","03","04","05","06","07","08","09","10","11","12"]
    MonthFin.grid(column=3, row=5, pady=7, ipadx=5, ipady=8, sticky="w")
    MonthFin.config(justify="center")

    StringDayFin=tk.StringVar(value="DD")
    DayFin=ComboboxPlus(FrameTablesView, height=5 , state="readonly", width=4, textvariable=StringDayFin)
    DayFin["values"]=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    DayFin.grid(column=3, row=5, ipadx=5, ipady=8)
    DayFin.config(justify="center")

    StringHourFin=tk.StringVar(value="HH")
    HourFin=ComboboxPlus(FrameTablesView, height=5 , state="readonly", width=4, textvariable=StringHourFin)
    HourFin["values"]=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
    HourFin.grid(column=3, row=5, ipadx=5, ipady=8, sticky="e")
    HourFin.config(justify="center")


    ListEntryTab=[EntryClientTab,EntryPhoneTab,EntryAdressPickTab,EntryAdressDelvTab,EntryDelvTab,
    EntryServTab,EntryPriceTab,EntryIDTab,EntryEstado,EntryTable]


    #--------------------------------BUTTON TABLES VIEWER--------------------------------------------------

    ButtonSearch=ttk.Button(FrameTablesView, text="Buscar",  
    command=lambda:fsdF.MostrarBusquedad(ListEntryTab,YearInic,MonthInic,DayInic,HourInic,YearFin,MonthFin,DayFin,HourFin,fontLabel))
    ButtonSearch.config(cursor="hand2")
    ButtonSearch.grid(column=2, row=7, pady=30, ipadx=15, padx=20)


    ButtonBorrCamposViewer=ttk.Button(FrameTablesView, image=img_eraser, command=lambda:fsdF.BorrarCampos(ListEntryTab))
    ButtonBorrCamposViewer.grid(column=0, row=6, padx=50, ipadx=15, sticky='w')
    ButtonBorrCamposViewer.config(cursor="hand2")




    #-----------------------------------FRAME TABLE CLIENT------------------------------------------------

    FrameClients=tk.Frame(MyNotebook)
    FrameClients.config(bg="gray40")
    FrameClients.columnconfigure((0,1,2,3,4), weight=2)
    FrameClients.rowconfigure(3, weight=1)
    FrameClients.pack()


    #-----------------------------------LABELS TABLE CLIENT------------------------------------------------

    labClientView=tk.Label(FrameClients, text="Cliente:", font=fontLabel, width=18)
    labClientView.grid(column=0, row=0, pady=20, sticky="w", padx=10)
    labClientView.config(foreground="black", background="gray40")

    labPhoneView=tk.Label(FrameClients, text="Teléfono:", font=fontLabel, width=18)
    labPhoneView.grid(column=0, row=1, pady=20, sticky="w", padx=20)
    labPhoneView.config(foreground="black", background="gray40")

    labAdressPickView=tk.Label(FrameClients, text="Dirección a recoger:", font=fontLabel, width=18)
    labAdressPickView.grid(column=2, row=0, pady=20, sticky="w", padx=20)
    labAdressPickView.config(foreground="black", background="gray40")

    labAdressDelvView=tk.Label(FrameClients, text="Dirección a entregar:", font=fontLabel, width=18)
    labAdressDelvView.grid(column=2, row=1, pady=20, sticky="w", padx=20)
    labAdressDelvView.config(foreground="black", background="gray40")

    labTotalClient=tk.Label(FrameClients, text="🔵 CLIENTES:", font=fontLabel, width=18)
    labTotalClient.grid(column=3, row=2, pady=20, ipadx=40)
    labTotalClient.config(foreground="deep sky blue2", background="gray40")

    textClient=tk.StringVar()
    labNumClient=tk.Label(FrameClients, textvariable=textClient, font=fontLabel, width=6)
    labNumClient.grid(column=3, row=2, pady=20, padx=40, sticky="e")
    labNumClient.config(foreground="black", background="gray40")

    fsdF.MostrarTotal(textClient,"CLIENTES")



    #-----------------------------------ENTRYS TABLE CLIENT-----------------------------------------------

    ClientTabClient=EntryPlus(FrameClients)
    ClientTabClient.grid(column=1, row=0, pady=20, ipadx=100, ipady=5)
    ClientTabClient.config(justify="center")

    PhoneTabClient=EntryPlus(FrameClients)
    PhoneTabClient.grid(column=1, row=1, pady=20, ipadx=100, ipady=5)
    PhoneTabClient.config(justify="center")

    AdressPickTabClient=EntryPlus(FrameClients)
    AdressPickTabClient.grid(column=3, row=0, pady=20, ipadx=100, ipady=5)
    AdressPickTabClient.config(justify="center")

    AdressDelvTabClient=EntryPlus(FrameClients)
    AdressDelvTabClient.grid(column=3, row=1, pady=20, ipadx=100, ipady=5)
    AdressDelvTabClient.config(justify="center")

    ListEntryClients=[ClientTabClient,PhoneTabClient,AdressPickTabClient,AdressDelvTabClient]


    #-----------------------------------BUTTON FRAME CLIENTS----------------------------------------------------

    ButtonView=ttk.Button(FrameClients, text="Buscar", command=lambda:fsdF.BuscarClient(ClientTabClient,TViewTabClient))
    ButtonView.config(cursor="hand2")
    ButtonView.grid(column=2, row=2, pady=30, ipadx=15)

    InsertButton=ttk.Button(FrameClients, text="Crear", command=lambda:fsdF.AgregarCliente(ListEntryClients, TViewTabClient, textClient))
    InsertButton.config(cursor="hand2")
    InsertButton.grid(column=0, row=2, pady=30, ipadx=15)

    ButtonSuprm=ttk.Button(FrameClients, text="Eliminar", command=lambda:fsdF.EliminarCliente(TViewTabClient, ClientTabClient, textClient))
    ButtonSuprm.config(cursor="hand2")
    ButtonSuprm.grid(column=1, row=2, pady=30, ipadx=15)

    ButtonReset = ttk.Button(FrameClients, image=img_reload, width=2, padding=2.5, command=lambda:fsdF.MostrarTablas(TViewTabClient, 'CLIENTES'))
    ButtonReset.config(cursor="hand2")
    ButtonReset.grid(column=3, row=2, pady=30, sticky='e')

    ButtonBorrCamposClient=ttk.Button(FrameClients, image=img_eraser, command=lambda:fsdF.BorrarCampos(ListEntryClients))
    ButtonBorrCamposClient.grid(column=0, row=0, padx=20, sticky='w')
    ButtonBorrCamposClient.config(cursor="hand2")

    
    #--------------------------------TREEVIEW TABLE CLIENT------------------------------------------------

    TViewTabClient=ttk.Treeview(FrameClients, height=30, show="headings") 
    TViewTabClient["columns"]=("CLIENTE","TELEFONO","DIRECCION_RECOGER","DIRECCION_ENTREGAR")

    tvClient=ttk.Style(TViewTabClient)
    tvClient.configure("Treeview", rowheight=55)

    scrollVertClient=tk.Scrollbar(FrameClients, orient="vertical")
    scrollVertClient.config(command=TViewTabClient.yview)
    scrollVertClient.grid(column=5, row=3, rowspan=1, sticky="ns")

    scrollHorClient=tk.Scrollbar(FrameClients, orient="horizontal")
    scrollHorClient.config(command=TViewTabClient.xview)
    scrollHorClient.grid(column=0, row=4, columnspan=6, sticky="we")

    TViewTabClient.config(yscrollcommand=scrollVertClient.set, xscrollcommand=scrollHorClient.set)

    TViewTabClient.column("CLIENTE", width=300, minwidth=150)
    TViewTabClient.column("TELEFONO", width=300, minwidth=150)
    TViewTabClient.column("DIRECCION_RECOGER", width=500, minwidth=250)
    TViewTabClient.column("DIRECCION_ENTREGAR", width=500, minwidth=250)

    TViewTabClient.heading("CLIENTE", text="CLIENTE", anchor="w")
    TViewTabClient.heading("TELEFONO", text="TELÉFONO", anchor="w")
    TViewTabClient.heading("DIRECCION_RECOGER", text="DIRECCIÓN A RECOGER", anchor="w")
    TViewTabClient.heading("DIRECCION_ENTREGAR", text="DIRECCIÓN A ENTREGAR", anchor="w")

    TViewTabClient.grid(column=0, row=3, columnspan=4)
    TViewTabClient.tag_configure("par", foreground="black", background="SkyBlue1")
    TViewTabClient.tag_configure("impar", foreground="black", background="SkyBlue3")

    fsdF.MostrarTablas(TViewTabClient, "CLIENTES")








    #-----------------------------------FRAME TABLE STATISTICS------------------------------------------------

    FrameEstadisticas=tk.Frame(MyNotebook)
    FrameEstadisticas.config(bg="gray40", pady=5)
    FrameEstadisticas.columnconfigure((0,1,2,3,4), weight=2)
    FrameEstadisticas.rowconfigure((0,1,2,3,4), weight=2)
    FrameEstadisticas.pack()

    #---------------------------------LABELS FRAME STATISTICS--------------------------------------------------

    LabelGraf=tk.Label(FrameEstadisticas, text="Gráfica:", font=fontLabel, width=18)
    LabelGraf.grid(column=0, row=0, pady=7)
    LabelGraf.config(foreground="black", background="gray40")

    LabelTable=tk.Label(FrameEstadisticas, text="Tabla:", font=fontLabel, width=18)
    LabelTable.grid(column=2, row=0, pady=7)
    LabelTable.config(foreground="black", background="gray40")

    LabelCampos=tk.Label(FrameEstadisticas, text="Columna:", font=fontLabel, width=18)
    LabelCampos.grid(column=0, row=1, pady=7)
    LabelCampos.config(foreground="black", background="gray40")

    LabelOpcion=tk.Label(FrameEstadisticas, text="Opción:", font=fontLabel, width=18)
    LabelOpcion.grid(column=2, row=1, pady=7)
    LabelOpcion.config(foreground="black", background="gray40")

    LabelDesde=tk.Label(FrameEstadisticas, text="Desde:", font=fontLabel, width=18)
    LabelDesde.grid(column=0, row=2, pady=7)
    LabelDesde.config(foreground="black", background="gray40")

    LabelDesde=tk.Label(FrameEstadisticas, text="Hasta:", font=fontLabel, width=18)
    LabelDesde.grid(column=2, row=2, pady=7)
    LabelDesde.config(foreground="black", background="gray40")


    #-------------------------------------COMBOBOX FRAME STATISTICS------------------------------------

    CombGraf=ComboboxPlus(FrameEstadisticas, state="readonly")
    CombGraf["values"]=["LINEAL","BARRAS"]
    CombGraf.grid(column=1, row=0, ipady=8, sticky="we")
    CombGraf.config(justify="center")

    CombTable=ComboboxPlus(FrameEstadisticas, state="readonly")
    CombTable["values"]=["DOMICILIOS DIARIOS","DOMICILIOS TOTALES"]
    CombTable.grid(column=3, row=0, ipady=8, sticky="we")
    CombTable.config(justify="center")

    CombCampos=ComboboxPlus(FrameEstadisticas, height=5, state="readonly")
    CombCampos["values"]=["SERVICIOS","CLIENTE","TELEFONO","DIRECCION A ENTREGAR","DIRECCION A RECOGER","MENSAJERO","TIPO DE SERVICIO"]
    CombCampos.grid(column=1, row=1, ipady=8, sticky="we")
    CombCampos.config(justify="center")

    CombOpcion=ComboboxPlus(FrameEstadisticas)
    CombOpcion["values"]=["TODOS","MÁS REPETIDOS"]
    CombOpcion.grid(column=3, row=1, ipady=8, sticky="we")
    CombOpcion.config(justify="center")

    textYear=tk.StringVar(value="YYYY")
    CombYear=ComboboxPlus(FrameEstadisticas, height=5 , text="lol",state="readonly", width=6, textvariable=textYear)
    CombYear["values"]=["2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033","2034","2035"]
    CombYear.grid(column=1, row=2, ipady=8, sticky="w", ipadx=8)
    CombYear.config(justify="center")

    textMonth=tk.StringVar(value="MM")
    CombMonth=ComboboxPlus(FrameEstadisticas,height=5 , state="readonly", width=6, textvariable=textMonth)
    CombMonth["values"]=["01","02","03","04","05","06","07","08","09","10","11","12"]
    CombMonth.grid(column=1, row=2, pady=7, ipady=8, padx=7, ipadx=8)
    CombMonth.config(justify="center")

    textDay=tk.StringVar(value="DD")
    CombDay=ComboboxPlus(FrameEstadisticas, height=5 , state="readonly", width=6, textvariable=textDay)
    CombDay["values"]=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    CombDay.grid(column=1, row=2, ipady=8, sticky="e", ipadx=8)
    CombDay.config(justify="center")

    CombDateFin=ComboboxPlus(FrameEstadisticas, height=5 , state="readonly")
    CombDateFin["values"]=["1 mes despúes","2 meses despúes","3 meses despúes","4 meses despúes","5 meses despúes","6 meses despúes"]
    CombDateFin.grid(column=3, row=2, ipady=8, sticky="ew")
    CombDateFin.config(justify="center")

    listEntryEstadis=[CombGraf,CombTable,CombCampos,CombOpcion]


    #---------------------------------------BUTTON STATISTICS-----------------------------------------------

    buttonStatistics=ttk.Button(FrameEstadisticas, text="Generar",  command=lambda:fsdE.Graf(CombTable,CombCampos,CombOpcion,CombGraf,CombYear,CombMonth,CombDay,CombDateFin))
    buttonStatistics.config(cursor="hand2")
    buttonStatistics.grid(column=1, row=3, pady=15, ipadx=20)

    ButtonBorrCamposEstadis=ttk.Button(FrameEstadisticas, image=img_eraser, command=lambda:fsdF.BorrarCampos(listEntryEstadis))
    ButtonBorrCamposEstadis.grid(column=0, row=3, ipadx=15)
    ButtonBorrCamposEstadis.config(cursor="hand2")

    





    #------------------------------------------FRAME TABLE DOMICILIOS TOTALES--------------------------------------------------

    TableTotalView=tk.Frame(MyNotebook)
    TableTotalView.config(bg="gray40", relief="groove")
    TableTotalView.columnconfigure((0,1,2,3,4), weight=2)
    TableTotalView.pack()

    TreeViewTab=ttk.Treeview(TableTotalView, height=11) 
    TreeViewTab["columns"]=("ID","CLIENTE","TELEFONO","DIRECCION_RECOGER","DIRECCION_ENTREGAR",
    "MENSAJERO","TIPOSERVICIO","PRECIO","DESCRIPCION","FECHA")

    tv=ttk.Style(TreeViewTab)
    tv.configure("Treeview", rowheight=55)

    scrollVertTreeV=tk.Scrollbar(TableTotalView, orient="vertical")
    scrollVertTreeV.config(command=TreeViewTab.yview)
    scrollVertTreeV.grid(column=5, row=3, rowspan=3, sticky="ns")

    scrollHorTreeV=tk.Scrollbar(TableTotalView, orient="horizontal")
    scrollHorTreeV.config(command=TreeViewTab.xview)
    scrollHorTreeV.grid(column=0, row=5, columnspan=6, sticky="we")

    TreeViewTab.config(yscrollcommand=scrollVertTreeV.set, xscrollcommand=scrollHorTreeV.set)

    TreeViewTab.column("ID", width=50, minwidth=25)
    TreeViewTab.column("CLIENTE", width=300, minwidth=150)
    TreeViewTab.column("TELEFONO", width=300, minwidth=150)
    TreeViewTab.column("DIRECCION_RECOGER", width=500, minwidth=250)
    TreeViewTab.column("DIRECCION_ENTREGAR", width=500, minwidth=250)
    TreeViewTab.column("MENSAJERO", width=200, minwidth=100)
    TreeViewTab.column("TIPOSERVICIO", width=300, minwidth=150)
    TreeViewTab.column("PRECIO", width=200, minwidth=100)
    TreeViewTab.column("DESCRIPCION", width=500, minwidth=150)
    TreeViewTab.column("FECHA", width=200, minwidth=100)

    TreeViewTab.heading("ID", text="ID", anchor="w")
    TreeViewTab.heading("CLIENTE", text="CLIENTE", anchor="w")
    TreeViewTab.heading("TELEFONO", text="TELÉFONO", anchor="w")
    TreeViewTab.heading("DIRECCION_RECOGER", text="DIRECCIÓN A RECOGER", anchor="w")
    TreeViewTab.heading("DIRECCION_ENTREGAR", text="DIRECCIÓN A ENTREGAR", anchor="w")
    TreeViewTab.heading("MENSAJERO", text="MENSAJERO", anchor="w")
    TreeViewTab.heading("TIPOSERVICIO", text="TIPO DE SERVICIO", anchor="w")
    TreeViewTab.heading("PRECIO", text="PRECIO", anchor="w")
    TreeViewTab.heading("DESCRIPCION", text="DESCRIPCIÓN", anchor="w")
    TreeViewTab.heading("FECHA", text="FECHA", anchor="w")

    TreeViewTab.grid(column=0, row=4, columnspan=12)
    TreeViewTab.tag_configure("par", foreground="black", background="SkyBlue1")
    TreeViewTab.tag_configure("impar", foreground="black", background="SkyBlue3")
    TreeViewTab.tag_configure("check", image=img_check)
    TreeViewTab.tag_configure("uncheck", image=img_uncheck)


    def toggleCheckTotal(event):

        try:

            rowid = TreeViewTab.identify_row(event.y)
            tag1 = TreeViewTab.item(rowid, "tags")[0]
            tag2 = TreeViewTab.item(rowid, "tags")[1]

            tags = list(TreeViewTab.item(rowid, "tags"))
            tags.remove(tag1)
            TreeViewTab.item(rowid, tags = tags)


            if tag1 == "check" and tag2 == "par":
                TreeViewTab.item(rowid, tags = ("uncheck", "par"))

            elif tag1 == "check" and tag2 == "impar":
                TreeViewTab.item(rowid, tags = ("uncheck", "impar"))

            elif tag1 == "uncheck" and tag2 == "par":
                TreeViewTab.item(rowid, tags = ("check", "par"))

            elif tag1 == "uncheck" and tag2 == "impar":
                TreeViewTab.item(rowid, tags = ("check", "impar"))
                

        except IndexError:

            pass


    def selectItemTotal(a):

        try:

            curItem = TreeViewTab.focus()
            tag = TreeViewTab.item(curItem)['tags'][0]
            reg = TreeViewTab.item(curItem)['values']


            fsdF.estadoReg("DOMICILIOS TOTALES",tag,reg[0], reg[9],TextPendientes,TextEntregados)

        except IndexError:

            pass

    
    R1Total = tk.Button(TableTotalView, image = img_check, borderwidth=0, activebackground="gray40", command=lambda:checkUncheckTable('ENTREGADO','DOMICILIOS_TOTALES',TextPendientes,TextEntregados,TreeViewTab))
    R1Total.config(cursor="hand2", background='gray40')
    R1Total.grid(column=0, row=0, sticky="w", padx=15, pady=15)

    R2Total = tk.Button(TableTotalView, image = img_uncheck, borderwidth=0, activebackground="gray40", command=lambda:checkUncheckTable('PENDIENTE','DOMICILIOS_TOTALES',TextPendientes,TextEntregados,TreeViewTab))
    R2Total.config(cursor="hand2", background='gray40')
    R2Total.grid(column=0, row=0, padx=15, pady=15)

    labResultadoTotal=tk.Label(TableTotalView, text="🔵 DOMICILIOS TOTALES:", font=fontLabel)
    labResultadoTotal.grid(column=1, row=0, pady=30)
    labResultadoTotal.config(foreground="deep sky blue2", background="gray40")

    TextTotal=tk.StringVar()
    labRegBusquedaTotal=tk.Label(TableTotalView, textvariable=TextTotal, font=fontLabel)
    labRegBusquedaTotal.grid(column=2, row=0, pady=30, sticky='w')
    labRegBusquedaTotal.config(foreground="black", background="gray40")

    fsdF.MostrarTotal(TextTotal,"DOMICILIOS TOTALES")


    TreeViewTab.bind("<Button 1>", toggleCheckTotal)
    TreeViewTab.bind('<ButtonRelease-1>', selectItemTotal)

    fsdF.MostrarTablas(TreeViewTab, "DOMICILIOS_TOTALES")



    #------------------------------------------FRAME TABLE DOMICILIOS DIARIOS--------------------------------------------------

    TableDayView=tk.Frame(MyNotebook)
    TableDayView.config(bg="gray40", relief="groove")
    TableDayView.columnconfigure((0,1,2,3,4), weight=2)
    TableDayView.pack()
    
    TreeViewDay=ttk.Treeview(TableDayView, height=11) 
    TreeViewDay["columns"]=("ID","CLIENTE","TELEFONO","DIRECCION_RECOGER","DIRECCION_ENTREGAR",
    "MENSAJERO","TIPOSERVICIO","PRECIO","DESCRIPCION","FECHA")

    tv=ttk.Style(TreeViewDay)
    tv.configure("Treeview", rowheight=55)

    scrollVertTreeV=tk.Scrollbar(TableDayView, orient="vertical")
    scrollVertTreeV.config(command=TreeViewDay.yview)
    scrollVertTreeV.grid(column=5, row=3, rowspan=3, sticky="ns")

    scrollHorTreeV=tk.Scrollbar(TableDayView, orient="horizontal")
    scrollHorTreeV.config(command=TreeViewDay.xview)
    scrollHorTreeV.grid(column=0, row=5, columnspan=6, sticky="we")

    TreeViewDay.config(yscrollcommand=scrollVertTreeV.set, xscrollcommand=scrollHorTreeV.set)

    TreeViewDay.column("ID", width=50, minwidth=25)
    TreeViewDay.column("CLIENTE", width=300, minwidth=150)
    TreeViewDay.column("TELEFONO", width=300, minwidth=150)
    TreeViewDay.column("DIRECCION_RECOGER", width=500, minwidth=250)
    TreeViewDay.column("DIRECCION_ENTREGAR", width=500, minwidth=250)
    TreeViewDay.column("MENSAJERO", width=200, minwidth=100)
    TreeViewDay.column("TIPOSERVICIO", width=300, minwidth=150)
    TreeViewDay.column("PRECIO", width=200, minwidth=100)
    TreeViewDay.column("DESCRIPCION", width=500, minwidth=150)
    TreeViewDay.column("FECHA", width=200, minwidth=100)

    TreeViewDay.heading("ID", text="ID", anchor="w")
    TreeViewDay.heading("CLIENTE", text="CLIENTE", anchor="w")
    TreeViewDay.heading("TELEFONO", text="TELÉFONO", anchor="w")
    TreeViewDay.heading("DIRECCION_RECOGER", text="DIRECCIÓN A RECOGER", anchor="w")
    TreeViewDay.heading("DIRECCION_ENTREGAR", text="DIRECCIÓN A ENTREGAR", anchor="w")
    TreeViewDay.heading("MENSAJERO", text="MENSAJERO", anchor="w")
    TreeViewDay.heading("TIPOSERVICIO", text="TIPO DE SERVICIO", anchor="w")
    TreeViewDay.heading("PRECIO", text="PRECIO", anchor="w")
    TreeViewDay.heading("DESCRIPCION", text="DESCRIPCIÓN", anchor="w")
    TreeViewDay.heading("FECHA", text="FECHA", anchor="w")

    TreeViewDay.grid(column=0, row=4, columnspan=12)
    TreeViewDay.tag_configure("par", foreground="black", background="SkyBlue1")
    TreeViewDay.tag_configure("impar", foreground="black", background="SkyBlue3")
    TreeViewDay.tag_configure("check", image=img_check)
    TreeViewDay.tag_configure("uncheck", image=img_uncheck)


    def toggleCheckDay(event):

        try:

            rowid = TreeViewDay.identify_row(event.y)
            tag1 = TreeViewDay.item(rowid, "tags")[0]
            tag2 = TreeViewDay.item(rowid, "tags")[1]

            tags = list(TreeViewDay.item(rowid, "tags"))
            tags.remove(tag1)
            TreeViewDay.item(rowid, tags = tags)

            if tag1 == "check" and tag2 == "par":
                TreeViewDay.item(rowid, tags = ("uncheck", "par"))

            elif tag1 == "check" and tag2 == "impar":
                TreeViewDay.item(rowid, tags = ("uncheck", "impar"))

            elif tag1 == "uncheck" and tag2 == "par":
                TreeViewDay.item(rowid, tags = ("check", "par"))

            elif tag1 == "uncheck" and tag2 == "impar":
                TreeViewDay.item(rowid, tags = ("check", "impar"))

        except IndexError:

            pass


    def selectItemDay(a):

        try:

            curItem = TreeViewDay.focus()
            tag = TreeViewDay.item(curItem)['tags'][0]
            reg = TreeViewDay.item(curItem)['values']

            

            fsdF.estadoReg("DOMICILIOS DIARIOS",tag,reg[0], reg[9], TextPendientes, TextEntregados)

        except IndexError:

            pass

        
    R1Day = tk.Button(TableDayView, image = img_check, borderwidth=0, activebackground="gray40", command=lambda:checkUncheckTable('ENTREGADO','DOMICILIOS_DIARIOS',TextPendientes,TextEntregados,TreeViewDay))
    R1Day.config(cursor="hand2", background='gray40')
    R1Day.grid(column=0, row=0, sticky="w", padx=15, pady=15)

    R2Day = tk.Button(TableDayView, image = img_uncheck, borderwidth=0, activebackground="gray40", command=lambda:checkUncheckTable('PENDIENTE','DOMICILIOS_DIARIOS',TextPendientes,TextEntregados,TreeViewDay))
    R2Day.config(cursor="hand2", background='gray40')
    R2Day.grid(column=0, row=0, padx=15, pady=15)

    labResultadoDay=tk.Label(TableDayView, text="🔵 DOMICILIOS DIARIOS:", font=fontLabel)
    labResultadoDay.grid(column=1, row=0, pady=30)
    labResultadoDay.config(foreground="deep sky blue2", background="gray40")

    TextDomDiario=tk.StringVar()
    labRegBusquedaDay=tk.Label(TableDayView, textvariable=TextDomDiario, font=fontLabel)
    labRegBusquedaDay.grid(column=2, row=0, pady=30, sticky='w')
    labRegBusquedaDay.config(foreground="black", background="gray40")

    fsdF.MostrarTotal(TextDomDiario,"DOMICILIOS DIARIOS")


    TreeViewDay.bind("<Button 1>", toggleCheckDay)
    TreeViewDay.bind('<ButtonRelease-1>', selectItemDay)

    fsdF.MostrarTablas(TreeViewDay, "DOMICILIOS_DIARIOS")




    #--------------------------------------CHECK OR UNCHECK ALL THE TABLE-----------------------------------


    def checkUncheckTable(estado,table,textPend,textEnt,treeView):

        option = messagebox.askokcancel("",'¿Estás seguro que quieres marcar todos los registros como ' + estado + "?")

        try:

            if estado == 'ENTREGADO' and option == True:

                 for rowid in treeView.get_children():

                    tag1 = treeView.item(rowid, "tags")[0]
                    tag2 = treeView.item(rowid, "tags")[1]
                    
                    if tag1 == 'uncheck' and tag2 == "par":

                        treeView.item(rowid, tags = ("check", "par"))

                    elif tag1 == 'uncheck' and tag2 == "impar":

                        treeView.item(rowid, tags = ("check", "impar"))

            elif estado == 'PENDIENTE' and option == True:

                for rowid in treeView.get_children():

                    tag1 = treeView.item(rowid, "tags")[0]
                    tag2 = treeView.item(rowid, "tags")[1]

                    if tag1 == "check" and tag2 == "impar":

                        treeView.item(rowid, tags = ("uncheck", "impar"))

                    elif tag1 == 'check' and tag2 == "par":
                        
                        treeView.item(rowid, tags = ("uncheck", "par"))
                
            fsdF.estadoALL(table,estado,textPend,textEnt)

        except:
            
            pass

    #-----------------------------------------NOTEBOOK-------------------------------------------------------


    MyNotebook.add(FrameRegistros, text="     Registros      ")
    MyNotebook.add(FrameTablesView, text="       Buscar       ")
    MyNotebook.add(TableDayView, text="  Domicilios Diarios  ")
    MyNotebook.add(TableTotalView, text=" Domicilios Totales ")
    MyNotebook.add(FrameClients, text="      Clientes      ")
    MyNotebook.add(FrameEstadisticas, text="     Estadísticas   ")
    MyNotebook.pack()


    root.protocol("WM_DELETE_WINDOW", lambda:fsdF.SalirDeApp(root))

    root.mainloop()


App()