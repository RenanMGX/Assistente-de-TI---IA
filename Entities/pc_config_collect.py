import cpuinfo
import psutil
import wmi
import platform


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
                print(partition_usage.total)
            except PermissionError:
                # Ignora partições sem permissão
                pass

        return {
            "total" : str(round(total_space / (1024**3), 2)) + "gigabytes",
            "disponivel" : str(round(available_space / (1024**3), 2)) + "gigabytes"
        }


      
if __name__ == "__main__":
    bot  = ConfigPC()
    
    print(bot.sistema_operacional)