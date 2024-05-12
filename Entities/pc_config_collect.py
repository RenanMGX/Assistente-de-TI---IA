import cpuinfo
import psutil
import wmi
import platform
import socket
import requests
import winreg


class ConfigPC:
    @property
    def processador(self) -> str:
        try:
            info = cpuinfo.get_cpu_info()
            return str(info['brand_raw'])
        except:
            return "não identificado"

    @property
    def processador_usando(self) -> str:
        try:
            cpu_usage = psutil.cpu_percent()
            return str(cpu_usage) + " %"
        except:
            return "não identificado"
    
    @property
    def ram_total(self) -> str:
        try:
            ram = psutil.virtual_memory().total
            #ram = (ram / (1024**3))
            #ram = math.ceil(ram)
            return str(ram) + " bytes"
        except:
           return "não identificado" 

    @property
    def ram_usando(self) -> str:
        try:
            ram_usage = psutil.virtual_memory().percent
            #ram = (ram / (1024**3))
            #ram = math.ceil(ram)
            return str(ram_usage) + " %"
        except:
           return "não identificado" 
    
    @property
    def placa_video(self) -> str:
        try:
            c = wmi.WMI()
            placa:str = ""
            for gpu in c.Win32_VideoController():
                placa = str(gpu.Name)
            if not placa:
                raise Exception()
            return placa
        except:
            return "não identificado"
    
    @property
    def armazenamento_total(self) -> str:
        return self.space()["total"]
    
    @property
    def armazenamento_disponivel(self) -> str:
        return self.space()["disponivel"]

    @property
    def sistema_operacional(self) -> str:
        try:
            sistema_operacional = platform.system()
            versao_sistema = str(platform.version())
            return str((sistema_operacional + " " + versao_sistema))
        except:
           return "não identificado" 

    @property
    def placa_mae_fabricante(self) -> str:
        try:
            c = wmi.WMI()
            for motherboard in c.Win32_BaseBoard():
                return str((motherboard.Manufacturer))
            raise Exception()
        except:
           return "não identificado" 
    
    @property
    def placa_mae_modelo(self) -> str:
        try:
            c = wmi.WMI()
            for motherboard in c.Win32_BaseBoard():
                return str((motherboard.Product))
            raise Exception()
        except:
           return "não identificado" 

    @property
    def ip_wam(self) -> str:
        try:
            return self.get_wan_ip()
        except:
           return "não identificado" 
 
    @property
    def ip_lan(self) -> str:
        try:
            return self.get_lan_ip()
        except:
           return "não identificado" 

    @property
    def nome_maquina(self) -> str:
        try:
            machine_name = socket.gethostname()
            return machine_name
        except:
           return "não identificado" 

    @property
    def rede_info(self) -> str:
        try:
            return self.get_network_info()
        except:
           return "não identificado" 

    @property
    def lista_programas_instalados(self) -> str|list:
        try:
            return self.get_installed_programs()
        except:
           return "não identificado" 

    @property
    def lista_programas_em_exec(self) -> list|str:
        try:
            running_processes = [proc.name() for proc in psutil.process_iter(['pid', 'name'])]
            return running_processes
        except:
           return "não identificado" 



 
    @property
    def sockete_processador(self) -> str:
        try:
            c = wmi.WMI()
            for processor in c.Win32_Processor():
                return str(processor.SocketDesignation)
            raise Exception()
        except:
           return "não identificado" 
    
    def space(self) -> dict:
        partitions = psutil.disk_partitions(all=True)
        total_space = 0
        available_space = 0
        # Itera sobre todas as partições
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                total_space += partition_usage.total
                available_space += partition_usage.free
            except PermissionError:
                # Ignora partições sem permissão
                pass

        return {
            "total" : str(round(total_space / (1024**3), 1)) + " Gigabytes",
            "disponivel" : str(round(available_space / (1024**3), 2)) + " Gigabytes"
        }
        
    def get_wan_ip(self):
        try:
            # Faz uma requisição a um serviço que retorna seu IP WAN
            response = requests.get('https://api.ipify.org')
            if response.status_code == 200:
                return response.text
            else:
                return "Erro ao obter IP WAN: Status Code {}".format(response.status_code)
        except Exception as e:
            return "Erro ao obter IP WAN: {}".format(str(e))

    def get_lan_ip(self):
        try:
            # Obtém o hostname da máquina
            hostname = socket.gethostname()
            # Obtém o IP LAN associado ao hostname
            ip = socket.gethostbyname(hostname)
            return ip
        except Exception as e:
            return "Erro ao obter IP LAN: {}".format(str(e))

    def get_installed_programs(self):
        try:
            installed_programs = []

            # Chave do registro onde as informações de programas instalados estão localizadas
            uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            
            # Abre a chave do registro
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
                # Itera pelos subchaves
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey_path = uninstall_key + "\\" + subkey_name
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                            # Tenta obter o valor do nome do programa
                            display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                            installed_programs.append(display_name)
                    except FileNotFoundError:
                        # Algumas chaves podem não ter o valor DisplayName
                        pass
            
            return installed_programs
        except Exception as e:
            return "Erro ao obter lista de programas instalados: {}".format(str(e))

    def get_network_info(self) -> str:
        network_info = {}
        
        # Obtém informações de conexão de rede
        connections = psutil.net_connections()
        network_info['connections'] = connections
        
        # Obtém estatísticas de rede
        net_io_counters = psutil.net_io_counters()
        network_info['io_counters'] = net_io_counters
        
        # Obtém informações sobre interfaces de rede
        net_interfaces = psutil.net_if_addrs()
        network_info['interfaces'] = net_interfaces
        

        return f"""
            Network Connections: {[conn for conn in network_info['connections']]};
            \nNetwork I/O Counters:
            Bytes Sent: {network_info['io_counters'].bytes_sent},
            Bytes Received: {network_info['io_counters'].bytes_recv};
            \nNetwork Interfaces: {[[f"Family: {addr.family}, Address: {addr.address}, Netmask: {addr.netmask}, Broadcast: {addr.broadcast}" for addr in interface_addresses]for interface_name, interface_addresses in network_info['interfaces'].items()]}
            """
    
    def __str__(self) -> str:
        return str(f"""
                   Processador: {self.processador};\n
                   Uso Processador: {self.processador_usando};\n
                   Memoria Ram: {self.ram_total};\n
                   Uso Memoria Ram: {self.ram_usando};\n
                   Placa de Video: {self.placa_video};\n
                   Armazenamento Total: {self.armazenamento_total};\n
                   Armazenamento Disponivel: {self.armazenamento_disponivel};\n
                   Sistema Operacional: {self.sistema_operacional};\n
                   Fabricante Placa Mãe: {self.placa_mae_fabricante};\n
                   Modelo Placa Mão: {self.placa_mae_modelo};\n
                   IP WAM: {self.ip_wam};\n
                   IP LAN: {self.ip_lan};\n
                   Nome do computador: {self.nome_maquina};\n
                   Lista programas em execução: {str(self.lista_programas_em_exec)};\n
                   Lista de programas instalados: {str(self.lista_programas_instalados)};\n
                   Informaçoes de Rede: {str(self.rede_info)}\n;
                   """)

      
if __name__ == "__main__":
    bot  = ConfigPC()
    
    print(bot)
    print(bot.ip_wam)