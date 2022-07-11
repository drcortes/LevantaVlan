#Script para levantar VLAN
#ejecucion python LevantamientoVlan.py

###################Librerias###################
from datetime import *
import os
###################Variables################
Fecha = date.today()
date = datetime.strptime(str(Fecha), "%Y-%m-%d")
dia=date.day
mes=date.month
if mes < 10:
	mes='0'+str(mes)
if dia < 10:
	dia='0'+str(dia)
anio=date.year
Directorio='/Respaldos/RouterySwitch/'+str(anio)+'/'+str(mes)+'/'+str(dia)+''
DbDistribucion='/Respaldos/SCRIPT/DbDistribuciones'
ListaArchivos = os.listdir(Directorio)
ExisteVlan=0
##################SCRIPT#####################
print('Levantamiento de VLAN en equipos Core')
CurrentDirectory=os.getcwd()+"/LevantamientoVlan_"+str(anio)+"_"+str(mes)+"_"+str(dia)+".csv"
ArchivoSalida=open(CurrentDirectory,"w")
ArchivoSalida.write("Distribucion,Hostname,Vlan,IP,Mascara,Descripcion")
ArchivoSalida.write("\n")
ArchivoSalida.close()
for archivo in ListaArchivos:
	descripcion="Sin Informacion"
	file=open(Directorio+'/'+archivo,'r')
	lineaArchivo=file.readlines()
	for linea in lineaArchivo:
		if 'hostname' in linea:
			hostname=linea.rstrip('\n')
			hostname=hostname.split(" ")
			hostname=str(hostname[1])
			hostname=hostname.rstrip('\r')
			db=open(DbDistribucion,'r')
			dblinea=db.readlines()
			for entry in dblinea:
				if hostname in entry:
					distribucion=entry.rstrip('\n')
					distribucion=distribucion.rsplit('\t')
					distribucion=distribucion[0]
					distribucion=distribucion.rstrip('\r')
			db.close()
	#########Busca Vlan################
		if ExisteVlan == 0:
			if 'interface Vlan' in linea:
				if '-' in linea:
					ExisteVlan=0
				else:
					vlan=linea.rstrip('\n')
					vlan=vlan.replace('interface ','')
					vlan=vlan.rstrip('\r')
					ExisteVlan=1
			if 'interface GigabitEthernet' in linea:
                                if '-' in linea:
                                        ExisteVlan=0
                                else:
                                        vlan=linea.rstrip('\n')
                                        vlan=vlan.replace('interface ','')
                                        vlan=vlan.rstrip('\r')
                                        ExisteVlan=1
		elif ExisteVlan == 1:
			if 'interface' in linea:
				ExisteVlan=0
			elif 'description' in linea:
				descripcion=linea.rstrip('\n')
				descripcion=descripcion.rstrip('\r')
				descripcion=descripcion.strip()
				#print(descripcion)
			elif 'ip address' in linea:
				IP=linea.rstrip('\n')
				if 'no' in linea:
					A=1
				else:
					ip=IP.split("ip address")
					ip=ip[1].replace("secondary","")
					ip=ip.strip()
					if "/" in ip:
						ip=ip.split("/")
						mask=ip[1]
						ip=ip[0]
					else:
						ip=ip.split(" ")
                                                mask=ip[1]
                                                ip=ip[0]
					Salida=distribucion+","+hostname+","+vlan+","+ip+","+mask+","+descripcion
					ArchivoSalida=open(CurrentDirectory,"a")
					ArchivoSalida.write(Salida)
					ArchivoSalida.write("\n")
					ArchivoSalida.close()
				ExisteVlan=0
			
	file.close()
ArchivoSalida.close()
print("Fin del Script, se crea el archivo /LevantamientoVlan_"+str(anio)+"_"+str(mes)+"_"+str(dia)+".csv")


