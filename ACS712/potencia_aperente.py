from machine import Pin, ADC, deepsleep
from time import ticks_ms
import math

###########DEFINICION DE FUNCIONES###########

def calculo_offset(adc, ventana_tiempo):
    # Inicializa las variables para el cálculo del promedio
    sum_of_values = 0
    muestras_recopiladas = 0
    # Obtiene el tiempo actual en milisegundos
    start_time = ticks_ms()

    while True:
        # Obtiene el valor del sensor
        val1 = adc.read()
        val2 = 3.3 * val1 / 4095
        #voltajes.append(val2)
        
        # Acumula los valores
        sum_of_values += val2
        
        
        muestras_recopiladas += 1
        
        # Verifica si ha pasado la ventana de tiempo
        current_time = ticks_ms()
        if current_time - start_time >= ventana_tiempo:
            
            # Calcula el promedio
            promedio = sum_of_values / muestras_recopiladas

            # Imprime el voltaje promedio
            #print('Voltaje promedio:', promedio)
            
            return promedio

def calculo_Potencia_aparente(adc, promedio, sensibilidad, ventana_tiempo):
    start_time = ticks_ms()
    sumatoria = 0
    muestras_recopiladas = 0

    while True:
        val1 = adc.read()
        val2 = 3.3 * val1 / 4095
        #voltajes.append(val2)
            
        sumatoria += (val2 - promedio)**2
        
        current_time = ticks_ms()
        
        muestras_recopiladas += 1
        
        if current_time - start_time >= ventana_tiempo:
       
            # Calcular la corriente RMS 
            corriente_rms = (1 / sensibilidad) * (sumatoria / muestras_recopiladas)**0.5
            voltaje_rms = 120
            Papp = corriente_rms*voltaje_rms
        
            return Papp

#######LOGICA#####################################################################################

# Configura el pin del sensor y la resolución del ADC
pin = Pin(34)
adc = ADC(pin)
adc.atten(ADC.ATTN_11DB)

# Configura el pin del botón
button_pin = Pin(0, Pin.IN)

# Define la ventana de tiempo (en milisegundos)
ventana_tiempo = 200

# Datos del sensor
sensibilidad = 0.185  # Sensibilidad del sensor en A/V
    
promedio = calculo_offset(adc, ventana_tiempo)

print("El voltaje promedio es:", promedio, "V")
   
Papp = calculo_Potencia_aparente(adc, promedio, sensibilidad, ventana_tiempo)
    
print("La Potencia Aparente es:", Papp, "VA")
        

# Comprueba si se ha presionado el botón para entrar en el modo de sueño profundo
if button_pin.value() == 1:
    deepsleep(1000)
