# Nama : M. Umar Faiz Alfa Rizqy
# NIM : H1D024010
# Shift baru : E
# Shift lama : H

# Import library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# variabel input
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')           #range suhu = 0–40 °C
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')  #range kelembapan = 0–100 %

# variabel output
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')    #range kecepatan = 0–100

# Suhu: dingin, normal, panas
suhu['dingin'] = fuzz.trapmf(suhu.universe, [0, 0, 10, 20]) #grafik suhu dingin = bentuk grafik trapesium, dengan titik-titik (0,0), (0,1), (10,1), (20,0)
suhu['normal'] = fuzz.trimf(suhu.universe, [15, 22, 30]) #grafik suhu normal = bentuk grafik segitiga, dengan titik-titik (15,0), (22,1), (30,0)
suhu['panas'] = fuzz.trapmf(suhu.universe, [25, 30, 40, 40]) #grafik suhu panas = bentuk grafik trapesium, dengan titik-titik (25,0), (30,1), (40,1), (40,0)

# Kelembapan: kering, normal, lembab
kelembapan['kering'] = fuzz.trapmf(kelembapan.universe, [0, 0, 20, 40]) #grafik kelembapan kering = bentuk grafik trapesium, dengan titik-titik (0,0), (0,1), (20,1), (40,0)
kelembapan['normal'] = fuzz.trimf(kelembapan.universe, [30, 50, 70]) #grafik kelembapan normal = bentuk grafik segitiga, dengan titik-titik (30,0), (50,1), (70,0)
kelembapan['lembab'] = fuzz.trapmf(kelembapan.universe, [60, 80, 100, 100]) #grafik kelembapan lembab = bentuk grafik trapesium, dengan titik-titik (60,0), (80,1), (100,1), (100,0)

# Kecepatan kipas: lambat, sedang, cepat
kecepatan['lambat'] = fuzz.trapmf(kecepatan.universe, [0, 0, 20, 40]) #grafik kecepatan lambat = bentuk grafik trapesium, dengan titik-titik (0,0), (0,1), (20,1), (40,0)
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [30, 50, 70]) #grafik kecepatan sedang = bentuk grafik segitiga, dengan titik-titik (30,0), (50,1), (70,0)
kecepatan['cepat'] = fuzz.trapmf(kecepatan.universe, [60, 80, 100, 100]) #grafik kecepatan cepat = bentuk grafik trapesium, dengan titik-titik (60,0), (80,1), (100,1), (100,0)

# Aturan Fuzzy
# 1) Jika suhu panas ATAU kelembapan lembab maka kecepatan cepat
aturan1 = ctrl.Rule(suhu['panas'] | kelembapan['lembab'], kecepatan['cepat'])
# 2) Jika suhu normal DAN kelembapan normal maka kecepatan sedang
aturan2 = ctrl.Rule(suhu['normal'] & kelembapan['normal'], kecepatan['sedang'])
# 3) Jika suhu dingin DAN kelembapan kering maka kecepatan lambat
aturan3 = ctrl.Rule(suhu['dingin'] & kelembapan['kering'], kecepatan['lambat'])

kipas_ctrl = ctrl.ControlSystem([aturan1, aturan2, aturan3]) #membuat mesin inferensi dengan memasukkan aturan-aturan yang telah dibuat
kipas_sim = ctrl.ControlSystemSimulation(kipas_ctrl) #membuat simulasi dengan memasukkan mesin inferensi yang telah dibuat

kipas_sim.input['suhu'] = 30        # input suhu (derajat Celcius)
kipas_sim.input['kelembapan'] = 70  # input kelembapan (persen)

kipas_sim.compute() #menghitung output

print("Kecepatan kipas =", kipas_sim.output['kecepatan']) #menampilkan output kecepatan kipas
kecepatan.view(sim=kipas_sim) #menampilkan grafik kecepatan kipas dengan input yang telah diberikan

input("Tekan ENTER untuk keluar...") #exit program setelah menampilkan hasil dan grafik