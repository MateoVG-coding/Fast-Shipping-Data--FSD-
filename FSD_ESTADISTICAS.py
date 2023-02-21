import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import sqlite3
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tkinter import messagebox


def Graf(table, option, registro, grafic, y, m, d, months):

	table=table.get()
	option=option.get()
	registro=registro.get().strip().upper()
	grafic=grafic.get()
	y=y.get()
	m=m.get() 
	d=d.get()
	months=months.get()[0:2]

	MyConnection=sqlite3.connect("(FSD) BBDD Servicios")

	Mycursor=MyConnection.cursor()

	tablesql=table.replace(" ","_")
	optionsql=option.replace(" ","_")

	try:
		
		fechaInic=datetime.strptime(f"{y}-{m}-{d}", '%Y-%m-%d')
		fechaFin=fechaInic + relativedelta(months=int(months[0:1]))

		try:

			if option=="SERVICIOS" and grafic=="LINEAL" and registro=="TODOS" and fechaInic!=[] and fechaFin!=[]:

				sql=f"SELECT FECHA FROM {tablesql} WHERE FECHA BETWEEN '{fechaInic}' AND '{fechaFin}';"

				Mycursor.execute(sql)

				fechas={}

				for i in Mycursor.fetchall():

					fecha = i[0][:10]
					fechas[fecha] = fechas.get(fecha, 0) + 1

				y=fechas.values()
	
				if fechas!={}:

					x = np.arange(len(y))

					width = 0.35

					fig, ax = plt.subplots(figsize=(13,5))
					rects1 = ax.plot_date(x,y,'o-', color="blue", linewidth=1.5)

					ax.set_ylabel("REGISTROS", color="blue")
					ax.set_xlabel("FECHA", color="blue")

					ax.set_title(("GRÁFICA DE {} SEGÚN {}").format(table, option), 
							      fontdict={'family': 'DejaVu Sans', 
							                    'color' : 'blue',
							                    'weight': 'bold',
							                    'size': 12}, loc="right")

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					ax.set_xticks(x)
					ax.set_xticklabels(fechas.keys(), rotation=20)

					ax.yaxis.set_major_locator(MaxNLocator(integer=True))

					fig.tight_layout()

					plt.grid()

					plt.plot([] ,color="blue", label=f"{str(fechaInic)[0:10]} hasta {str(fechaFin)[0:10]}")

					plt.plot([], color="black", label=f"{registro}")

					plt.legend()

					plt.show()

						
				else:

					messagebox.showinfo("Estadísticas vacías","Las estadísticas que has querido especificar se encuentran vacías.")	



				
			elif option!="SERVICIOS" and grafic=="LINEAL" and registro!="TODOS" and registro!="MÁS REPETIDOS" and fechaInic!=[] and fechaFin!=[]:

				sql=f"SELECT {optionsql}, FECHA FROM {tablesql} WHERE {optionsql}='{registro}' AND FECHA BETWEEN '{fechaInic}' AND '{fechaFin}' GROUP BY FECHA;" 

				Mycursor.execute(sql)

				x=[]

				y=[]

				for i in Mycursor.fetchall():

					if i[0]!='':

						x.append(i[1][0:10])

				for i in x:

					y.append(x.count(i))

				if x!=[] and y!=[]:

					width = 0.35

					fig, ax = plt.subplots(figsize=(13,5))
					rects1 = ax.plot_date(x,y,'o-', color="blue", linewidth=1.5)

					ax.set_ylabel("REGISTROS", color="blue")
					ax.set_xlabel("FECHA", color="blue")

					ax.set_title(("GRÁFICA DE {} SEGÚN {}").format(table, option), 
							      fontdict={'family': 'DejaVu Sans', 
							                    'color' : 'blue',
							                    'weight': 'bold',
							                    'size': 12}, loc="right")

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					ax.set_xticks(x)
					ax.set_xticklabels(x, rotation=20)

					ax.yaxis.set_major_locator(MaxNLocator(integer=True))

					fig.tight_layout()

					plt.grid()

					plt.plot([] ,color="blue", label=f"{str(fechaInic)[0:10]} hasta {str(fechaFin)[0:10]}")

					plt.plot([], color="black", label=f"{registro}")

					plt.legend()

					plt.show()


				else:

					messagebox.showinfo("Estadísticas vacías","Las estadísticas que has querido especificar se encuentran vacías.")




			elif option=="SERVICIOS" and grafic=="BARRAS" and registro=="TODOS" and fechaInic!=[] and fechaFin!=[]:
		 			
				sql=f"SELECT FECHA FROM {tablesql} WHERE FECHA BETWEEN '{fechaInic}' AND '{fechaFin}';"

				Mycursor.execute(sql) 

				fechas={}

				for i in Mycursor.fetchall():

					fecha = i[0][:10]
					fechas[fecha] = fechas.get(fecha, 0) + 1

				y=fechas.values()
	
				if fechas!={}:

					x = np.arange(len(y))

					width = 0.35

					fig, ax = plt.subplots(figsize=(13,5))
					rects1 = ax.bar(x, y, width, color=["dodgerblue","grey"], edgecolor="black", linewidth=1.5)

					ax.set_ylabel("REGISTROS", color="blue")
					ax.set_xlabel(option, color="blue")

					ax.set_title(("GRÁFICA DE {} SEGÚN {}").format(table, option), 
							      fontdict={'family': 'DejaVu Sans', 
							                    'color' : 'blue',
							                    'weight': 'bold',
							                    'size': 12}, loc="right")

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					ax.set_xticks(x)
					ax.set_xticklabels(fechas.keys(), rotation=20)

					ax.yaxis.set_major_locator(MaxNLocator(integer=True))

					def autolabel(rects):
						for rect in rects:
						    height = rect.get_height()
						    ax.annotate('{}'.format(height),
						                    xy=(rect.get_x() + rect.get_width() / 2, height),
						                    xytext=(0, 3),
						                    textcoords="offset points",
						                    ha='center', va='bottom')


					autolabel(rects1)

					fig.tight_layout()

					plt.plot([] ,color="blue", label=f"{str(fechaInic)[0:10]} hasta {str(fechaFin)[0:10]}")

					plt.plot([], color="black", label="TODOS")

					plt.legend()

					plt.show()

				else:

					messagebox.showinfo("Estadísticas vacías","Las estadísticas que has querido especificar se encuentran vacías.")




			elif option!="SERVICIOS" and grafic=="BARRAS" and registro!="TODOS" and fechaInic!=[] and fechaFin!=[]:

				if registro!="MÁS REPETIDOS":

					sql=f"SELECT {optionsql}, FECHA FROM {tablesql} WHERE {optionsql}='{registro}' AND FECHA BETWEEN '{fechaInic}' AND '{fechaFin}' GROUP BY FECHA;"

					Mycursor.execute(sql)

					fechas = {}

					for i in Mycursor.fetchall():

						if i[0]!='':

							fecha = i[1][:10]
							fechas[fecha] = fechas.get(fecha, 0) + 1

								
					y=fechas.values()

					if fechas!={}:

						x = np.arange(len(y))

						width = 0.35

						fig, ax = plt.subplots(figsize=[12,6])
						rects1 = ax.bar(x, y, width, color=["dodgerblue","grey"], edgecolor="black", linewidth=1.5)

						ax.set_ylabel("REGISTROS", color="blue")
						ax.set_xlabel(option, color="blue")

						ax.set_title(("GRÁFICA DE {} SEGÚN {}").format(table, option), 
						          fontdict={'family': 'DejaVu Sans', 
						                    'color' : 'blue',
						                    'weight': 'bold',
						                    'size': 12}, loc="right")

						ax.spines['right'].set_visible(False)
						ax.spines['top'].set_visible(False)

						ax.set_xticks(x)
						ax.set_xticklabels(fechas.keys(), rotation=20)

						ax.yaxis.set_major_locator(MaxNLocator(integer=True))

						def autolabel(rects):
							for rect in rects:
							    height = rect.get_height()
							    ax.annotate('{}'.format(height),
							                    xy=(rect.get_x() + rect.get_width() / 2, height),
							                    xytext=(0, 3),
							                    textcoords="offset points",
							                    ha='center', va='bottom')


						autolabel(rects1)

						fig.tight_layout()

						plt.plot([] ,color="blue", label=f"{str(fechaInic)[0:10]} hasta {str(fechaFin)[0:10]}")

						plt.plot([], color="black", label=f"{option}: {registro}")

						plt.legend()

						plt.show()

					else:

						messagebox.showinfo("Estadísticas vacías","Las estadísticas que has querido especificar se encuentran vacías.")


				else:

					sql=f"SELECT {optionsql}, COUNT({optionsql}) AS TOTAL FROM {tablesql} WHERE FECHA BETWEEN '{fechaInic}' AND '{fechaFin}' GROUP BY {optionsql} ORDER BY TOTAL DESC LIMIT 7;" 

					Mycursor.execute(sql) 

					values=[]

					names=[]

					for datos in Mycursor.fetchall():

						if datos[0]!='':

							values.append(datos[1])

							names.append(str(datos[0]))

					if values!=[] and names!=['']:

						x = np.arange(len(names))

						width = 0.35

						fig, ax = plt.subplots(figsize=(13,5))
						rects1 = ax.bar(x, values, width, color=["dodgerblue","grey"], edgecolor="black", linewidth=1.5)

						ax.set_ylabel("REGISTROS", color="blue")
						ax.set_xlabel(option, color="blue")

						ax.set_title(("GRÁFICA DE {} SEGÚN {}").format(table, option), 
						          fontdict={'family': 'DejaVu Sans', 
						                    'color' : 'blue',
						                    'weight': 'bold',
						                    'size': 12}, loc="right")

						ax.spines['right'].set_visible(False)
						ax.spines['top'].set_visible(False)

						ax.set_xticks(x)
						ax.set_xticklabels(names, rotation=20)

						ax.yaxis.set_major_locator(MaxNLocator(integer=True))

						def autolabel(rects):
							for rect in rects:
							    height = rect.get_height()
							    ax.annotate('{}'.format(height),
							                    xy=(rect.get_x() + rect.get_width() / 2, height),
							                    xytext=(0, 3),
							                    textcoords="offset points",
							                    ha='center', va='bottom')


						autolabel(rects1)

						fig.tight_layout()

						plt.plot([] ,color="blue", label=f"{str(fechaInic)[0:10]} hasta {str(fechaFin)[0:10]}")

						plt.plot([], color="black", label="MÁS REPETIDOS")

						plt.legend()

						plt.show()

					else:

						messagebox.showinfo("Estadísticas vacías","Las estadísticas que has querido especificar se encuentran vacías.")
					
			else:
				
				messagebox.showerror("Específicaciones no válidas","No se pueden realizar estadísticas con esas específicaciones.")

		except sqlite3.OperationalError:

				messagebox.showerror("Tabla inexistente","La tabla " + table + " no existe." )

	except ValueError:

		if 	table!='' and option!='' and registro!='' and  grafic!='' and months!='':

			messagebox.showerror("Fecha no válida","La fecha que has introducido no es válida.")

		else: 

			messagebox.showerror("Campos vacíos", "Los campos a buscar se encuentran vacíos.")


	MyConnection.commit()

	MyConnection.close()