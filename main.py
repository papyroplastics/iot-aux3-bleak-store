from bleak import BleakClient, BleakScanner
import random
import asyncio

# Variables definidas en el código de C del ejemplo
DEV_NAME = "Byte Store"
CHR_UUID = "88776655-8877-6655-8877-665588776655"

async def main():
    # Busca el dispositivo 
    device = await BleakScanner.find_device_by_name(DEV_NAME)

    if device is None:
        print(f"Dispositivo \"{DEV_NAME}\" no encontrado")
        return

    # Este bloque inicia la conección, cuando el bloque se termina la conección se cierra
    async with BleakClient(device) as client: 
        print(f"Conectado a {client.name} con dirección {client.address}")

        # Imprimir los servicios del dispositivo con sus caracteristicas
        print("\nServicios del dispositivo: ")
        for service in client.services:
            print(f"- Servicio \"{service.description}\" - {service.uuid}:")

            for char in service.characteristics:
                print(f"  - characteristica \"{char.description}\" - {char.uuid}")

            print()
        
        # Guardar y leer un número random 10 veces
        for _ in range(10):
            data_i = random.randbytes(1)
            await client.write_gatt_char(CHR_UUID, data_i)
            print(f"Se escribió el número: {data_i[0]} ", end='')

            data_f = await client.read_gatt_char(CHR_UUID)

            print(f"y se obtuvo el número: {data_f[0]}")
            await asyncio.sleep(0.5)



asyncio.run(main())
