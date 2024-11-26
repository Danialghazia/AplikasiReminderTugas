import random
m = 4
n = 5
# membentuk list berisi sepanjang 4 (m) data
MA = [0] * m

print(MA)
# print(len(MA))
for baris in range(m): # mulai dari bari = 0 sampai dengan kurang dari 4
    MA[baris] = [baris+1] * n
    # print(MA)
    MA[baris] [0] = random.randrange(1,58)
    MA[baris] [1] = random.randrange(51,100)
    MA[baris] [2] = random.randrange(1,50)
    MA[baris] [3] = random.randrange(51,100)
    MA[baris] [4] = random.randrange(1,50)
    print(MA)
# print("hasil pembuatan matrik MA secara acak")
# print(MA)


m = 4
n = 5
# membentuk list berisi sepanjang 4 (m) data
MB = [0] * m

print(MB)
# print(len(MB))
for baris in range(m): # mulai dari bari = 0 sampai dengan kurang dari 4
    MB[baris] = [baris+1] * n
    # print(MB)
    MB[baris] [0] = random.randrange(1,55)
    MB[baris] [1] = random.randrange(51,150)
    MB[baris] [2] = random.randrange(1,50)
    MB[baris] [3] = random.randrange(51,150)
    MB[baris] [4] = random.randrange(1,50)
    print(MA)
# print("hasil pembuatan matrik MA secara acak")
# print(MB)

# Membuat elemen matrik menggunakan pengulangan bersarang
m = 4
n = 5
MB = [0] * m
for i in range(m):
    MB[i] = [0] * n
print(MB)

for baris in range(0, m): 
    for kolom in range(0, n): 
        MB [baris] [kolom] = random.randrange(0,20)
print (MB)


MC = []

for i in range(0,len (MA)): 
    hasiljumlah = 0
    row = []
    for j in range(0, len (ΜΑ[0])):
#         print (MatA[i][j] + MatB[i][j], end='') 
        hasiljumlah = MA[i][j] + MB[i][j] 
        row.append(hasiljumlah)
#         MATC[i][j] = hasiljumlah
    # print(row)
    MC.append(row)
    
print("Matrik A:", MA)
print("Matrik B:", MB)
print("Matrik C:", MC) 

# inisialisasi matrik 3x2 dengan nilai random 
matNA = np.matrix(np.random.rand(3, 2))

print("Tipe Objek: ", type (matNA))

# print matriks pertama 
print('Matriks pertama: \n', matNA)

# inisialisasi matrik 2x3 dengan nilai random 
matNB = np.matrix(np.random.rand(2, 3))
# print matriks kedua print('\n Matriks kedua : \n', matNB
# perkalian matrik menggunakan operator *
matNC = matNA * matNB
# print matriks hasil perkalian print('\n Matriks hasil perkalian : \n', matNC)