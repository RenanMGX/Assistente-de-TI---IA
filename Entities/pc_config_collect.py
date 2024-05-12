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



    def __str__(self) -> str:
        return f"Processador: {self.processador}; Uso Processador: {self.processador_usando}; Memoria Ram: {self.ram_total}; Uso Memoria Ram: {self.ram_usando}; Placa de Video: {self.placa_video}; Armazenamento Total: {self.armazenamento_total}; Armazenamento Disponivel: {self.armazenamento_disponivel}; Sistema Operacional: {self.sistema_operacional}; Fabricante Placa Mãe: {self.placa_mae_fabricante}; Modelo Placa Mão: {self.placa_mae_modelo}; Ip WAN: {self.ip_wam}; Ip Lan: {self.ip_lan}; Nome do computador: {self.nome_maquina}, Lista programas em execução: {str(self.lista_programas_em_exec)}; Lista de programas instalados: {str(self.lista_programas_instalados)}"

      
if __name__ == "__main__":
    bot  = ConfigPC()
    
    print(bot)
    print(bot.nome_maquina)