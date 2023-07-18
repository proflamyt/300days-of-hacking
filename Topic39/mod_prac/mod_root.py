

# mod = 29

# res = [14, 6, 11]
# for _res in res:
#     for i in range(mod):
#         if _res == (i**2)%mod:
#             print(i)
#             break



p = 29
ints = [14, 6, 11]

qr = [a for a in range(p) if pow(a,2,p) in ints]
print(qr)
print(f"flag {min(qr)}")