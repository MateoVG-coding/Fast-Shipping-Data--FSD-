import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import webbrowser


def MostrarDocum():

	webbrowser.open_new("DOCUMENTACION FAST SHIPPING DATA (FSD).pdf")


def SalirDeApp(root):

	valor=messagebox.askokcancel("","¿Estás seguro que quieres salir de la aplicación?")

	if valor==True:
		root.destroy()

def EliminarTabla(table, textDay, textTotal, textClient, ListEntry,treeView, textPend='NO', textEnt='NO'):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")
	MyCursor=Myconnection.cursor()

	tablesql=table.replace(" ","_")


	valor=messagebox.askokcancel("","¿Estás seguro que quieres eliminar todos los registros de la tabla de " + table + "?")

	try:

		if valor==True:

			MyCursor.execute("DELETE FROM " + tablesql)

			Myconnection.commit()

			if tablesql=="DOMICILIOS_DIARIOS":

				MyCursor.execute("DELETE FROM sqlite_sequence WHERE name = 'DOMICILIOS_DIARIOS'")

				Myconnection.commit()

				if textPend!='NO' and textEnt!='NO':

					entregadoOrPendiente(textPend,textEnt)

				MostrarTotal(textDay,table)

				ValoresCombobox(ListEntry)

			elif tablesql=="DOMICILIOS_TOTALES":

				MostrarTotal(textClient,"DOMICILIOS TOTALES")

			else:

				MostrarTotal(textClient,"CLIENTES")

			MostrarTablas(treeView,tablesql)

			messagebox.showinfo("","Se han eliminado correctamente todos los registros de la tabla " + table + ".")

	except sqlite3.OperationalError:

		messagebox.showerror("", "La tabla de " + table + " no existe.")

	Myconnection.close()


def BorrarCampos(Strings, TextObs='NO'):

	lenght = len(Strings)

	for i in range(0,lenght):

		try:

			Strings[i].set("")

		except AttributeError:

			Strings[i].delete(0,'end')


	if TextObs!='NO':

		TextObs.delete(1.0, "end")



def MostrarLicencia():

	messagebox.showinfo("Licencia del programa FSD","Fast Shipping Data (FSD) no está bajo licencia")


def MostrarVersion():

	messagebox.showinfo("Versión del programa FSD","Fast Shipping Data (FSD) v3.0")

def MostrarContacto():

	messagebox.showinfo("","Correo electrónico: \n \nfastshippingdata@gmail.com")

def ConectarBBDD():

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")
	MyCursor=Myconnection.cursor()


	MyCursor.execute("""CREATE TABLE IF NOT EXISTS DOMICILIOS_DIARIOS(
						ID INTEGER PRIMARY KEY AUTOINCREMENT,
						CLIENTE VARCHAR(40),
						TELEFONO INTEGER,
						DIRECCION_A_RECOGER VARCHAR(40),
						DIRECCION_A_ENTREGAR VARCHAR(40),
						MENSAJERO VARCHAR(40),
						TIPO_DE_SERVICIO VARCHAR(50),
						PRECIO INTEGER,
						DESCRIPCION VARCHAR(150),
						FECHA VARCHAR(150),
						ESTADO VARCHAR(10))""")

	MyCursor.execute("""CREATE TABLE IF NOT EXISTS DOMICILIOS_TOTALES(
						ID INTEGER,
						CLIENTE VARCHAR(40),
						TELEFONO INTEGER,
						DIRECCION_A_RECOGER VARCHAR(40),
						DIRECCION_A_ENTREGAR VARCHAR(40),
						MENSAJERO VARCHAR(40),
						TIPO_DE_SERVICIO VARCHAR(40),
						PRECIO INTEGER,
						DESCRIPCION VARCHAR(150),
						FECHA VARCHAR(150),
						ESTADO VARCHAR(10))""")


	MyCursor.execute("""CREATE TABLE IF NOT EXISTS CLIENTES(
						CLIENTE VARCHAR(40),
						TELEFONO INTEGER,
						DIRECCION_A_RECOGER VARCHAR(40),
						DIRECCION_A_ENTREGAR VARCHAR(40))""")

	Myconnection.commit()

	Myconnection.close()


def	InsertarTabla(textDay,textTotal,ListEntry,TreeViewDay,TreeViewTab,textPend,textEnt):

	valor=messagebox.askokcancel("Inserción de registros","¿Estás seguro que quieres introducir los registros de la tabla de DOMICILIOS DIARIOS en DOMICILIOS TOTALES?")

	try: 

		if valor==True:

			Myconnection=sqlite3.connect("(FSD) BBDD Servicios")
			MyCursor=Myconnection.cursor()

			MyCursor.execute("""INSERT INTO DOMICILIOS_TOTALES (ID, CLIENTE, TELEFONO, DIRECCION_A_RECOGER, DIRECCION_A_ENTREGAR, MENSAJERO, TIPO_DE_SERVICIO, PRECIO, DESCRIPCION, FECHA, ESTADO)
						SELECT ID,CLIENTE, TELEFONO, DIRECCION_A_RECOGER, DIRECCION_A_ENTREGAR, MENSAJERO, TIPO_DE_SERVICIO, PRECIO, DESCRIPCION, FECHA, ESTADO FROM DOMICILIOS_DIARIOS""")

			MyCursor.execute("DELETE FROM DOMICILIOS_DIARIOS")

			MyCursor.execute("DELETE FROM sqlite_sequence WHERE name = 'DOMICILIOS_DIARIOS'")

			Myconnection.commit()

			ValoresCombobox(ListEntry)

			MostrarTablas(TreeViewDay, 'DOMICILIOS_DIARIOS')

			MostrarTablas(TreeViewTab, 'DOMICILIOS_TOTALES')

			MostrarTotal(textDay,"DOMICILIOS DIARIOS")

			MostrarTotal(textTotal,"DOMICILIOS TOTALES")

			entregadoOrPendiente(textPend,textEnt)


			Myconnection.close()

			messagebox.showinfo("Inserción exitosa","Se han insertado correctamente los registros de la tabla de DOMICILIOS DIARIOS.")


	except sqlite3.OperationalError:

		messagebox.showerror("Error inserción tabla","La tabla domicilios totales no existe.")




def CrearRegistro(listText,listEntry,TextObs, textDay, treeView, textPend, textEnt):

	global precioFijado

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	DatosRegistro=[]


	for a in listText[1:7]:

		DatosRegistro.append((a.get()).upper())
	
	try:

		DatosRegistro.append(listText[7].get())

		DatosRegistro.append(TextObs.get(1.0,"end"))

		if DatosRegistro!=['', '', '', '', '', '', 0.0, '\n']:

			try:

				MyCursor.executemany("INSERT INTO DOMICILIOS_DIARIOS VALUES(NULL,?,?,?,?,?,?,?,?,DATETIME(strftime('%Y-%m-%dT%H:%M:%S','now', 'localtime')),'PENDIENTE')",[DatosRegistro])

				try:
					listText[7].set(precioFijado)

				except NameError:
					listText[7].set(0.0)

				TextObs.delete(1.0, "end")
				TextObs.insert(1.0, "")

				listText[0].set("-----------------------------")

				for a in listText[1:7]:
					a.set("")

				Myconnection.commit()

				MostrarTablas(treeView,"DOMICILIOS_DIARIOS")

				MostrarTotal(textDay,"DOMICILIOS DIARIOS")

				ValoresCombobox(listEntry)

				entregadoOrPendiente(textPend,textEnt)

			except sqlite3.OperationalError:

				messagebox.showerror("Error base de datos","La base de datos no existe.")


		else:

			messagebox.showerror("Campos vacíos", "Todos los campos a ingresar en la base de datos están vacíos.")

	except tk.TclError:

	 	messagebox.showerror("Precio no válido", "El precio que has ingresado no es válido.")

	Myconnection.close()


def ValoresCombobox(ListEntry):

	"""Estos bucles funcionan para pasar valores constantemente a los combobox, para que estos muestren en orden alfabético los últimos datos
	de la tabla DOMICILIOS_DIARIOS"""

	try:

		Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

		MyCursor=Myconnection.cursor()

		MyCursor.execute("""SELECT ID FROM DOMICILIOS_DIARIOS ORDER BY ID DESC LIMIT 20""")
		rowsID=MyCursor.fetchall()

		ListrowsID=([i for (i,) in rowsID])
		ListEntry[0]["values"]=ListrowsID


		MyCursor.execute("""SELECT CLIENTE FROM DOMICILIOS_DIARIOS GROUP BY ID ORDER BY ID DESC LIMIT 20""")

		rowsCLIENTE=MyCursor.fetchall()
		ListrowsCLIENTE=sorted(set(([i for (i,) in rowsCLIENTE if i!=''])))

		ListEntry[1]["values"]=ListrowsCLIENTE


		MyCursor.execute("""SELECT TELEFONO FROM DOMICILIOS_DIARIOS GROUP BY ID ORDER BY ID DESC LIMIT 20""")

		rowsTELEFONO=MyCursor.fetchall()

		ListrowsTELEFONO=sorted(set(([str(i) for (i,) in rowsTELEFONO if i!=''])))

		ListEntry[2]["values"]=ListrowsTELEFONO


		MyCursor.execute("""SELECT DIRECCION_A_RECOGER FROM DOMICILIOS_DIARIOS GROUP BY ID ORDER BY ID DESC LIMIT 20""")

		rowsDIRECCIONRECOGER=MyCursor.fetchall()
		ListrowsDIRECCIONRECOGER=sorted(set(([i for (i,) in rowsDIRECCIONRECOGER if i!=''])))

		ListEntry[3]["values"]=ListrowsDIRECCIONRECOGER


		MyCursor.execute("""SELECT DIRECCION_A_ENTREGAR FROM DOMICILIOS_DIARIOS GROUP BY ID ORDER BY ID DESC LIMIT 20""")

		rowsDIRECCIONENTREGAR=MyCursor.fetchall()
		ListrowsDIRECCIONENTREGAR=sorted(set(([i for (i,) in rowsDIRECCIONENTREGAR if i!=''])))

		ListEntry[4]["values"]=ListrowsDIRECCIONENTREGAR


		MyCursor.execute("""SELECT MENSAJERO FROM DOMICILIOS_DIARIOS GROUP BY ID ORDER BY ID DESC LIMIT 20""")

		rowsMENSAJERO=MyCursor.fetchall()
		ListrowsMENSAJERO=sorted(set(([i for (i,) in rowsMENSAJERO if i!=''])))

		ListEntry[5]["values"]=ListrowsMENSAJERO

	except sqlite3.OperationalError:

		pass



def LeerRegistro(listText,TextObs):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	NumberID=listText[0].get().strip()


	if NumberID.isdigit()==True:

		try:

			MyCursor.execute("""SELECT CLIENTE, TELEFONO, DIRECCION_A_RECOGER, DIRECCION_A_ENTREGAR, MENSAJERO, TIPO_DE_SERVICIO, PRECIO, DESCRIPCION 
						FROM DOMICILIOS_DIARIOS WHERE ID=""" + NumberID)

			LecturaDeID=MyCursor.fetchall()
		
			if LecturaDeID!=[]:

				for RegistroLeido in LecturaDeID:

					listText[1].set(RegistroLeido[0])
					listText[2].set(RegistroLeido[1])
					listText[3].set(RegistroLeido[2])
					listText[4].set(RegistroLeido[3])
					listText[5].set(RegistroLeido[4])
					listText[6].set(RegistroLeido[5])
					listText[7].set(RegistroLeido[6])
					TextObs.delete(1.0, "end")
					TextObs.insert(1.0, RegistroLeido[7])

			else:

				messagebox.showerror("ID inexistente","El ID " + NumberID + " no existe en la base de datos.")


		except sqlite3.OperationalError:

			messagebox.showerror("Error base de datos","La base de datos no existe.")


	else:

		messagebox.showerror("Campo ID no válido","ID no válido, debes introducir un ID de tipo numérico.")


	Myconnection.commit()

	Myconnection.close()


def ActualizarRegistro(ListEntry,TextObs,listText,treeView):

	global precioFijado
	
	NumberID=ListEntry[0].get().strip()

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()


	if NumberID.isdigit()==True:

		valor=messagebox.askokcancel("","¿Estás seguro que quieres actualizar el registro con el ID " + NumberID + "?")


		if valor==True:

			try:

				MyCursor.execute("SELECT ID FROM DOMICILIOS_DIARIOS WHERE ID=" + NumberID)

				LecturaDeID=MyCursor.fetchall()


				if LecturaDeID!=[]:

					MyCursor.execute("UPDATE DOMICILIOS_DIARIOS SET CLIENTE='" + ListEntry[1].get().upper() + 
						"',TELEFONO='" + ListEntry[2].get().upper() +
						"',DIRECCION_A_RECOGER='" + ListEntry[3].get().upper() +
						"',DIRECCION_A_ENTREGAR='" + ListEntry[4].get().upper() +
						"',MENSAJERO='" + ListEntry[5].get().upper() +
						"',TIPO_DE_SERVICIO='" + ListEntry[6].get().upper() +
						"',PRECIO='" + ListEntry[7].get().upper() +
						"',DESCRIPCION='" + TextObs.get(1.0,"end") +
						"' WHERE ID=" + NumberID)

					for i in range(1,7):

						listText[i].set("")

					try:
						listText[7].set(precioFijado)

					except NameError:
						listText[7].set(0.0)

					TextObs.delete(1.0, "end")

					listText[0].set("-----------------------------")

					messagebox.showinfo("","Se ha actualizado correctamente el registro con ID " + NumberID + ".")

					Myconnection.commit()

					MostrarTablas(treeView,'DOMICILIOS_DIARIOS')


				else:

					messagebox.showerror("ID inexistente","El ID " + NumberID + " no existe en la base de datos.")


			except sqlite3.OperationalError:

				messagebox.showerror("Error base de datos","La base de datos no existe.")


	else:

		messagebox.showerror("Campo ID no válido","ID no válido, debes introducir un ID de tipo numérico.")


	Myconnection.close()


def EliminarRegistro(TextID, textDay, listText, TextObs, ListEntry, treeView, textPend, textEnt):

	global precioFijado

	NumberID=TextID.get().strip()

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()


	if NumberID.isdigit()==True:

		valor=messagebox.askokcancel("","¿Estás seguro que quieres eliminar el registro con el ID " + NumberID + "?")


		if valor==True:

			try:

				MyCursor.execute("SELECT ID FROM DOMICILIOS_DIARIOS WHERE ID=" + NumberID)

				LecturaDeID=MyCursor.fetchall()


				if LecturaDeID!=[]:

					MyCursor.execute("DELETE FROM DOMICILIOS_DIARIOS WHERE ID=" + NumberID)


					Myconnection.commit()

					MostrarTotal(textDay,'DOMICILIOS DIARIOS')

					MostrarTablas(treeView,'DOMICILIOS_DIARIOS')

					entregadoOrPendiente(textPend,textEnt)

					for i in range(1,7):

						listText[i].set("")

					
					try:
						listText[7].set(precioFijado)

					except NameError:
						listText[7].set(0.0)

					TextObs.delete(1.0, "end")

					listText[0].set("-----------------------------")

					ValoresCombobox(ListEntry)

					messagebox.showinfo("","Se ha eliminado correctamente el registro con ID " + NumberID + ".")

				else:

					messagebox.showerror("ID inexistente","El ID " + NumberID + " no existe en la base de datos.")

			
			except sqlite3.OperationalError:

				messagebox.showerror("Error base de datos","La base de datos no existe.")


	else: 
		
		messagebox.showerror("Campo ID no válido","ID no válido, debes introducir un ID de tipo numérico.")


	Myconnection.close()


def FijarPrecio(price):

	global precioFijado

	try:

		precioFijado=price.get()

		price.set(precioFijado)

		messagebox.showinfo("","El precio se ha fijado correctamente.")

	except tk.TclError:

	 	messagebox.showerror("Precio no válido", "El precio que has querido fijar no es válido.")


def MostrarBusquedad(ListEntryTab, y, m, d, h, yFin, mFin, dFin, hFin,fontLabel):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	options=[]

	dateInic=f"{y.get()}-{m.get()}-{d.get()} {h.get()}:00"

	dateFin=f"{yFin.get()}-{mFin.get()}-{dFin.get()} {hFin.get()}:00"

	y.set("YYYY")
	m.set("MM")
	d.set("DD")
	h.set("HH")
	yFin.set("YYYY")
	mFin.set("MM")
	dFin.set("DD")
	hFin.set("HH")

	for a in range(0,10):

		options.append((ListEntryTab[a].get()).strip().upper())


	options[9]=options[9].replace(" ","_")

	if options[9]!="":
		
		try:

			CLIENTE = f"CLIENTE='{options[0]}'"
			TELEFONO = f"TELEFONO='{options[1]}'"
			DIRECCION_A_RECOGER = f"DIRECCION_A_RECOGER='{options[2]}'" 
			DIRECCION_A_ENTREGAR = f"DIRECCION_A_ENTREGAR='{options[3]}'"
			MENSAJERO = f"MENSAJERO='{options[4]}'"
			TIPO_DE_SERVICIO = f"TIPO_DE_SERVICIO='{options[5]}'"
			PRECIO = f"PRECIO='{options[6]}'"
			ID = f"ID='{options[7]}'"
			ESTADO = f"ESTADO='{options[8]}'"

			columns=[CLIENTE,TELEFONO,DIRECCION_A_RECOGER,DIRECCION_A_ENTREGAR,MENSAJERO,TIPO_DE_SERVICIO,PRECIO,ID,ESTADO]
			list=[]
			
			#DETERMINA EN QUE CAMPOS SE DARA LA CONSULTA

			for b in range(0,9):

				if options[b]!="":

					list.append(columns[b]+" AND ")


			list[-1]=list[-1].rstrip(" AND ")

			searchCondition="".join(list)


			if dateInic=="YYYY-MM-DD HH:00" and dateFin=="YYYY-MM-DD HH:00":

				sql=f'SELECT * FROM {options[9]} WHERE {searchCondition}'

				sql=sql.replace("WHERE ESTADO='TODOS'",'')

				sql=sql.replace("AND ESTADO='TODOS'",'')


			else:

				sql=f"SELECT * FROM {options[9]} WHERE {searchCondition} AND FECHA BETWEEN '{dateInic}' AND '{dateFin}'"

				sql=sql.replace("ESTADO='TODOS' AND",'')
				
			
			MyCursor.execute(sql)

			resultado=MyCursor.fetchall()

			totalReg=len(resultado)


			if resultado!=[]:

				TreeViewSearch(resultado,options[9],totalReg, fontLabel)						

			else:

				messagebox.showinfo("Registro inexistente","El registro que has querido buscar no existe en la base de datos.")
				



		except sqlite3.OperationalError:

			messagebox.showerror("Error base de datos","La base de datos no existe.")

	else:

		messagebox.showerror("Campo tabla vacío", "No se ha seleccionado ninguna tabla para buscar.")

	Myconnection.commit()

	Myconnection.close()


def MostrarTablas(treeView, table):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	try:

		MyCursor.execute("SELECT * FROM " + table)

		tabla=MyCursor.fetchall()

		treeView.delete(*treeView.get_children())

		if tabla!=[]:
			
			try:

				for a in tabla[:]:

					if tabla.index(a)%2==0 and a[10] == 'ENTREGADO':

						treeView.insert("","end",
							values=a, tags=("check","par"))

					elif tabla.index(a)%2==0 and a[10] == 'PENDIENTE':

						treeView.insert("","end",
							values=a, tags=("uncheck","par"))

					elif tabla.index(a)%2!=0 and a[10] == 'ENTREGADO':

						treeView.insert("","end",
							values=a, tags=("check","impar"))
					
					elif tabla.index(a)%2!=0 and a[10] == 'PENDIENTE':

						treeView.insert("","end",
							values=a, tags=("uncheck","impar"))

			except IndexError:

				for i in tabla:

					if tabla.index(i)%2==0:

						treeView.insert("","end",
									values=i, tags=("par",))

					else:

						treeView.insert("","end",
									values=i, tags=("impar",))
								
	except sqlite3.OperationalError:
			
			pass

	Myconnection.close()



def AgregarCliente(Clients, treeView, textClient):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")
	MyCursor=Myconnection.cursor()

	values=[]

	for i in Clients:

		values.append((i.get()).strip().upper())


	if values[0]!='':

		try: 

			sql = f"SELECT CLIENTE FROM CLIENTES WHERE CLIENTE = '{values[0]}'"

			MyCursor.execute(sql)

			existo=MyCursor.fetchall()

			if existo==[]:

				MyCursor.executemany("INSERT INTO CLIENTES VALUES(?,?,?,?)",[values])

				Myconnection.commit()

				MostrarTablas(treeView, "CLIENTES")

				MostrarTotal(textClient,"CLIENTES")

				for i in Clients:

					i.delete(0, "end")

				messagebox.showinfo("","Se ha insertado correctamente el cliente " + values[0] + ".")

			else:

				messagebox.showerror('Cliente repetido','El cliente '  + values[0] + ' ya existe.')


		except sqlite3.OperationalError:

			messagebox.showerror("Error base de datos","La base de datos no existe.")


	else:

		messagebox.showerror("Campo cliente vacío","El campo cliente se encuentra vacío.")

	Myconnection.close()



def EliminarCliente(treeView, client, textClient):

	value=(client.get()).strip().upper()

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	if value!="":

		try:

			sql=f"SELECT * FROM CLIENTES WHERE CLIENTE='{value}'"

			MyCursor.execute(sql)

			exist = MyCursor.fetchall()

			if exist != []:

				opcionOk=messagebox.askokcancel("","¿Estás seguro que quieres eliminar el cliente " + value + "?")

				if opcionOk==True:

					sql=f"DELETE FROM CLIENTES WHERE CLIENTE='{value}'"

					MyCursor.execute(sql)

					Myconnection.commit()

					MostrarTotal(textClient,"CLIENTES")

					MostrarTablas(treeView, "CLIENTES")

					messagebox.showinfo("","Se ha eliminado correctamente el cliente " + value + ".")

			else:

				messagebox.showerror("Cliente inexistente","El cliente " + value + " no existe.")

		except:

			messagebox.showerror("Error base de datos","La base de datos no existe.")

	else: 

		messagebox.showerror("Campo cliente vacío","El campo cliente se encuentra vacío.")

	Myconnection.close()



def BuscarClient(Client, treeView):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	Client=(Client.get()).strip().upper()

	if Client!='':

		try:

			sql=f"SELECT * FROM CLIENTES WHERE CLIENTE='{Client}'"

			MyCursor.execute(sql)

			resultado=MyCursor.fetchall()

			Myconnection.commit()

			if resultado!=[]:

				treeView.delete(*treeView.get_children())

				for a in resultado[:]:

					treeView.insert("","end",
					values=a, tags=("par"))

			else:

				messagebox.showerror("Cliente inexistente","El cliente " + Client + " no existe.")


		except sqlite3.OperationalError:

			messagebox.showerror("Error base de datos","La base de datos no existe.")
	
	else:

		messagebox.showerror("Campo cliente vacío","El campo cliente se encuentra vacío.")

	
	Myconnection.close()


def ClienteReg(Client, listEntry):

	value=(Client.get()).strip().upper()

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	if value!="":

		try:
			sql=f"SELECT * FROM CLIENTES WHERE CLIENTE='{value}'"

			MyCursor.execute(sql)

			registro=MyCursor.fetchone()

			for i in range(0,4):

				listEntry[i+1].set(registro[i])

		except:

			messagebox.showerror("Cliente inexistente","El cliente " + value + " no existe.")

	else: 

		messagebox.showerror("Campo cliente vacío","El campo cliente se encuentra vacío.")

	
	Myconnection.commit()
	Myconnection.close()




def MostrarTotal(text,table):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	try:

		if table=="CLIENTES":

			MyCursor.execute("SELECT COUNT(CLIENTE) FROM CLIENTES")

			text.set(MyCursor.fetchone())

		elif table=="DOMICILIOS DIARIOS":

			MyCursor.execute("SELECT COUNT(CLIENTE) FROM DOMICILIOS_DIARIOS")

			text.set(MyCursor.fetchone())

		else: 

			MyCursor.execute("SELECT COUNT(CLIENTE) FROM DOMICILIOS_TOTALES")

			text.set(MyCursor.fetchone())

	except sqlite3.OperationalError:

		pass
	
	Myconnection.close()



def estadoReg(table,tag,id,date,textPend,textEnt):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	try:

		if tag == "check" and table == "DOMICILIOS DIARIOS":

			sql = f"UPDATE DOMICILIOS_DIARIOS SET ESTADO = 'ENTREGADO' WHERE ID = '{id}' AND FECHA = '{date}'"

			MyCursor.execute(sql)

		elif tag == "uncheck" and table == "DOMICILIOS DIARIOS":

			sql = f"UPDATE DOMICILIOS_DIARIOS SET ESTADO = 'PENDIENTE' WHERE ID = '{id}' AND FECHA = '{date}'"

			MyCursor.execute(sql)

		elif tag == "check" and table == "DOMICILIOS TOTALES":

			sql = f"UPDATE DOMICILIOS_TOTALES SET ESTADO = 'ENTREGADO' WHERE ID = '{id}' AND FECHA = '{date}'"

			MyCursor.execute(sql)

		elif tag == "uncheck" and table == "DOMICILIOS TOTALES":

			sql = f"UPDATE DOMICILIOS_TOTALES SET ESTADO = 'PENDIENTE' WHERE ID = '{id}' AND FECHA = '{date}'"

			MyCursor.execute(sql)

		Myconnection.commit()

		entregadoOrPendiente(textPend,textEnt)

	except sqlite3.OperationalError:

		pass

	Myconnection.close()


def estadoALL(table,estado,textPend,textEnt):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	try:

		if estado=='PENDIENTE':

			sql = f"UPDATE {table} SET ESTADO = 'PENDIENTE'"

			MyCursor.execute(sql)


		else:

			sql = f"UPDATE {table} SET ESTADO = 'ENTREGADO'"
			MyCursor.execute(sql)

		Myconnection.commit()
		Myconnection.close()
		entregadoOrPendiente(textPend,textEnt)
	

	except sqlite3.OperationalError:

		pass

def entregadoOrPendiente(textPend, textEnt):

	Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

	MyCursor=Myconnection.cursor()

	try:
	
		sql = "SELECT COUNT(ID) FROM DOMICILIOS_DIARIOS WHERE ESTADO = 'PENDIENTE'"

		MyCursor.execute(sql)

		result = MyCursor.fetchone()

		textPend.set(result)


		sql = "SELECT COUNT(ID) FROM DOMICILIOS_DIARIOS WHERE ESTADO = 'ENTREGADO'"

		MyCursor.execute(sql)

		result = MyCursor.fetchone()

		textEnt.set(result)


	except sqlite3.OperationalError:

		pass


def TreeViewPend(fontLabel, textPend, textEnt, TreeViewDay):

	try:

		sql = "SELECT * FROM DOMICILIOS_DIARIOS WHERE ESTADO = 'PENDIENTE'"

		MyCursor.execute(sql)

		resultPend = MyCursor.fetchall()


	except sqlite3.OperationalError:

		resultPend = []

	if resultPend!=[]:

		rootTable=tk.Toplevel()
		rootTable.state("zoomed")
		rootTable.title("Fast Shipping Data (FSD)")
		rootTable.iconbitmap("ICON_FSD.ico")
		rootTable.config(bg="gray40", relief="groove")

		TablesView=tk.Frame(rootTable)
		TablesView.config(bg="gray40", relief="groove")
		TablesView.columnconfigure((0,1,2,3,4), weight=2)
		TablesView.pack()

		img_check = ImageTk.PhotoImage(Image.open('icons/checkbox.png'))

		img_uncheck = ImageTk.PhotoImage(Image.open('icons/uncheckbox.png'))

		TreeViewPend=ttk.Treeview(TablesView, height=12) 
		TreeViewPend["columns"]=("ID","CLIENTE","TELEFONO","DIRECCION_RECOGER","DIRECCION_ENTREGAR",
		"MENSAJERO","TIPOSERVICIO","PRECIO","DESCRIPCION","FECHA")

		tv=ttk.Style(TreeViewPend)
		tv.configure("Treeview", rowheight=55)

		scrollVertTreeV=tk.Scrollbar(TablesView, orient="vertical")
		scrollVertTreeV.config(command=TreeViewPend.yview)
		scrollVertTreeV.grid(column=5, row=3, rowspan=3, sticky="ns")

		scrollHorTreeV=tk.Scrollbar(TablesView, orient="horizontal")
		scrollHorTreeV.config(command=TreeViewPend.xview)
		scrollHorTreeV.grid(column=0, row=5, columnspan=6, sticky="we")

		TreeViewPend.config(yscrollcommand=scrollVertTreeV.set, xscrollcommand=scrollHorTreeV.set)

		TreeViewPend.column("ID", width=50, minwidth=25)
		TreeViewPend.column("CLIENTE", width=300, minwidth=150)
		TreeViewPend.column("TELEFONO", width=300, minwidth=150)
		TreeViewPend.column("DIRECCION_RECOGER", width=500, minwidth=250)
		TreeViewPend.column("DIRECCION_ENTREGAR", width=500, minwidth=250)
		TreeViewPend.column("MENSAJERO", width=200, minwidth=100)
		TreeViewPend.column("TIPOSERVICIO", width=300, minwidth=150)
		TreeViewPend.column("PRECIO", width=200, minwidth=100)
		TreeViewPend.column("DESCRIPCION", width=500, minwidth=150)
		TreeViewPend.column("FECHA", width=200, minwidth=100)

		TreeViewPend.heading("ID", text="ID", anchor="w")
		TreeViewPend.heading("CLIENTE", text="CLIENTE", anchor="w")
		TreeViewPend.heading("TELEFONO", text="TELÉFONO", anchor="w")
		TreeViewPend.heading("DIRECCION_RECOGER", text="DIRECCIÓN A RECOGER", anchor="w")
		TreeViewPend.heading("DIRECCION_ENTREGAR", text="DIRECCIÓN A ENTREGAR", anchor="w")
		TreeViewPend.heading("MENSAJERO", text="MENSAJERO", anchor="w")
		TreeViewPend.heading("TIPOSERVICIO", text="TIPO DE SERVICIO", anchor="w")
		TreeViewPend.heading("PRECIO", text="PRECIO", anchor="w")
		TreeViewPend.heading("DESCRIPCION", text="DESCRIPCIÓN", anchor="w")
		TreeViewPend.heading("FECHA", text="FECHA", anchor="w")

		TreeViewPend.grid(column=0, row=4, columnspan=12)
		TreeViewPend.tag_configure("par", foreground="black", background="SkyBlue1")
		TreeViewPend.tag_configure("impar", foreground="black", background="SkyBlue3")
		TreeViewPend.tag_configure("check", image=img_check)
		TreeViewPend.tag_configure("uncheck", image=img_uncheck)

		for a in resultPend[:]:

			if resultPend.index(a)%2==0:

				TreeViewPend.insert("","end",
					values=a, tags=("uncheck","par",))

			else:

				TreeViewPend.insert("","end",
					values=a, tags=("uncheck","impar"))
		



		labResultado=tk.Label(TablesView, text="🔵 DOMICILIOS PENDIENTES:", font=fontLabel)
		labResultado.grid(column=0, row=0, pady=35)
		labResultado.config(foreground="deep sky blue2", background="gray40")

		TextTotal = tk.StringVar()
		labRegBusqueda=tk.Label(TablesView, textvariable=TextTotal, font=fontLabel)
		labRegBusqueda.grid(column=1, row=0, pady=35, sticky='w')
		labRegBusqueda.config(foreground="black", background="gray40")

		labRegTable=tk.Label(TablesView, text="DOMICILIOS DIARIOS", font=fontLabel)
		labRegTable.grid(column=2, row=0, pady=35)
		labRegTable.config(foreground="black", background="gray40")

		botonResetPend=ttk.Button(TablesView, text="↻", width=2, padding=2.5, command=lambda:resetDomPend(TreeViewPend,textPend,textEnt,rootTable))
		botonResetPend.grid(column=3, row=0)
		botonResetPend.config(cursor="hand2")


		def selectItemTotal(a):

			try:

				curItem = TreeViewPend.focus()
				tag = TreeViewPend.item(curItem)['tags'][0]
				reg = TreeViewPend.item(curItem)['values']


				estadoReg("DOMICILIOS DIARIOS",tag,reg[0], reg[9],textPend,textEnt)
				MostrarTablas(TreeViewDay,'DOMICILIOS_DIARIOS')

			except IndexError:

				pass

		

		def toggleCheckTotal(event):

			try:

				rowid = TreeViewPend.identify_row(event.y)
				tag1 = TreeViewPend.item(rowid, "tags")[0]
				tag2 = TreeViewPend.item(rowid, "tags")[1]

				tags = list(TreeViewPend.item(rowid, "tags"))
				tags.remove(tag1)
				TreeViewPend.item(rowid, tags = tags)


				if tag1 == "check" and tag2 == "par":
					TreeViewPend.item(rowid, tags = ("uncheck", "par"))

				elif tag1 == "check" and tag2 == "impar":
					TreeViewPend.item(rowid, tags = ("uncheck", "impar"))

				elif tag1 == "uncheck" and tag2 == "par":
					TreeViewPend.item(rowid, tags = ("check", "par"))

				elif tag1 == "uncheck" and tag2 == "impar":
					TreeViewPend.item(rowid, tags = ("check", "impar"))

			except IndexError:

				pass

			
		TreeViewPend.bind('<ButtonRelease-1>', selectItemTotal)

		TreeViewPend.bind("<Button 1>", toggleCheckTotal)


		rootTable.mainloop()

	else:

		messagebox.showinfo('','No hay ningún domicilio pendiente.')


def resetDomPend(treeView, textPend, textEnt, root):

	try:

		sql = "SELECT * FROM DOMICILIOS_DIARIOS WHERE ESTADO = 'PENDIENTE'"

		MyCursor.execute(sql)

		resultPend = MyCursor.fetchall()

	except sqlite3.OperationalError:

		resultPend = []

	
	if resultPend != []:

		treeView.delete(*treeView.get_children())

		for a in resultPend[:]:

			if resultPend.index(a)%2==0:

				treeView.insert("","end",
					values=a, tags=("uncheck","par",))

			else:

				treeView.insert("","end",
					values=a, tags=("uncheck","impar"))

	else:

		root.destroy()
		
		messagebox.showinfo('','No hay ningún domicilio pendiente.')
	



def TreeViewSearch(resultado, table, textRegTotal, fontLabel):

	rootTable=tk.Toplevel()
	rootTable.state("zoomed")
	rootTable.title("Fast Shipping Data (FSD)")
	rootTable.iconbitmap("ICON_FSD.ico")
	rootTable.config(bg="gray40", relief="groove")

	TablesView=tk.Frame(rootTable)
	TablesView.config(bg="gray40", relief="groove")
	TablesView.columnconfigure((0,1,2,3,4), weight=2)
	TablesView.pack()

	img_check = ImageTk.PhotoImage(Image.open('icons/checkbox.png'))

	img_uncheck = ImageTk.PhotoImage(Image.open('icons/uncheckbox.png'))

	TreeViewTab=ttk.Treeview(TablesView, height=12) 
	TreeViewTab["columns"]=("ID","CLIENTE","TELEFONO","DIRECCION_RECOGER","DIRECCION_ENTREGAR",
	"MENSAJERO","TIPOSERVICIO","PRECIO","DESCRIPCION","FECHA")

	tv=ttk.Style(TreeViewTab)
	tv.configure("Treeview", rowheight=55)

	scrollVertTreeV=tk.Scrollbar(TablesView, orient="vertical")
	scrollVertTreeV.config(command=TreeViewTab.yview)
	scrollVertTreeV.grid(column=5, row=3, rowspan=3, sticky="ns")

	scrollHorTreeV=tk.Scrollbar(TablesView, orient="horizontal")
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

	for a in resultado[:]:

		if resultado.index(a)%2==0 and a[10] == 'ENTREGADO':

			TreeViewTab.insert("","end",
				values=a, tags=("check","par"))

		elif resultado.index(a)%2==0 and a[10] == 'PENDIENTE':

			TreeViewTab.insert("","end",
				values=a, tags=("uncheck","par"))

		elif resultado.index(a)%2!=0 and a[10] == 'ENTREGADO':

			TreeViewTab.insert("","end",
				values=a, tags=("check","impar"))
		
		elif resultado.index(a)%2!=0 and a[10] == 'PENDIENTE':

			TreeViewTab.insert("","end",
				values=a, tags=("uncheck","impar"))


	labResultado=tk.Label(TablesView, text="🔵 REGISTROS TOTALES:", font=fontLabel)
	labResultado.grid(column=0, row=0, pady=35)
	labResultado.config(foreground="deep sky blue2", background="gray40")

	labRegBusqueda=tk.Label(TablesView, text=textRegTotal, font=fontLabel)
	labRegBusqueda.grid(column=1, row=0, pady=35, sticky='w')
	labRegBusqueda.config(foreground="black", background="gray40")

	table = table.replace("_"," ")
	
	labRegTable=tk.Label(TablesView, text=table, font=fontLabel)
	labRegTable.grid(column=2, row=0, pady=35)
	labRegTable.config(foreground="black", background="gray40")



	rootTable.mainloop()

Myconnection=sqlite3.connect("(FSD) BBDD Servicios")

MyCursor=Myconnection.cursor()