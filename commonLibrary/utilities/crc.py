import struct

def dow_crc(seed, poly, len, number, final_xor):
   crc = seed
   for i in range(len):
      crc = crc ^ number[i]
      for _ in range(8, 0, -1):
         if (crc & 0x80) != 0:
            crc = (crc << 1) ^ poly
         else:
            crc = (crc << 1)
   return crc & 0xFF

def tsy01_crc(n_prom_coef):
   crc = 0

   for i in range(8):
      crc = crc + ((n_prom_coef[i] >> 8) + (n_prom_coef[i] & 0xFF))
   return (crc & 0xFF == 0)

def main():
   crc = dow_crc(0xFF, 0x31, 0x02, (0xACEA).to_bytes(2, "big"), 0x00)
   print(f"CRC is: 0x{crc:02x}")

if __name__ == "__main__":
   main()
