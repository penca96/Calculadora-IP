import ipaddress

# 🔹 Determinar clase de red
def obtener_clase_ip(ip):
    primer_octeto = int(ip.split(".")[0])
    
    if 1 <= primer_octeto <= 126:
        return "Clase A"
    elif 128 <= primer_octeto <= 191:
        return "Clase B"
    elif 192 <= primer_octeto <= 223:
        return "Clase C"
    elif 224 <= primer_octeto <= 239:
        return "Clase D (Multicast)"
    elif 240 <= primer_octeto <= 255:
        return "Clase E (Experimental)"
    else:
        return "No válida"


# 🔹 Calcular info de red
def calcular_info_red(red, mascara):
    if "/" in mascara:
        red_completa = f"{red}{mascara}"
    else:
        red_completa = f"{red}/{mascara}"
    
    network = ipaddress.ip_network(red_completa, strict=False)
    
    hosts = list(network.hosts())
    
    info = {
        "red": str(network.network_address),
        "mascara": str(network.netmask),
        "broadcast": str(network.broadcast_address),
        "primera_ip": str(hosts[0]) if hosts else None,
        "ultima_ip": str(hosts[-1]) if hosts else None,
        "hosts": len(hosts),
        "clase": obtener_clase_ip(str(network.network_address))
    }
    
    return network, info


# 🔹 Calcular subredes
def calcular_subredes(network):
    subredes = []
    
    for subred in network.subnets():
        hosts = list(subred.hosts())
        
        subredes.append({
            "red": str(subred.network_address),
            "broadcast": str(subred.broadcast_address),
            "primera_ip": str(hosts[0]) if hosts else None,
            "ultima_ip": str(hosts[-1]) if hosts else None,
            "hosts": len(hosts)
        })
    
    return subredes


# 🔹 Función principal (fácil de reutilizar en GUI)
def analizar_red():
    red = input("Introduce la dirección de red: ")
    mascara = input("Introduce la máscara (ej: 255.255.255.192 o /26): ")
    
    try:
        network, info = calcular_info_red(red, mascara)
        
        print("\n=== INFORMACIÓN DE RED ===")
        for clave, valor in info.items():
            print(f"{clave.capitalize()}: {valor}")
        
        print("\n=== SUBREDES ===")
        subredes = calcular_subredes(network)
        
        for i, sub in enumerate(subredes, 1):
            print(f"\nSubred {i}:")
            for k, v in sub.items():
                print(f"  {k}: {v}")
    
    except ValueError as e:
        print(f"Error: {e}")


# 🔹 Ejecutar
if __name__ == "__main__":
    analizar_red()