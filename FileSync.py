# Importa bibliotecas
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import filecmp

# Contador para controlar a abertura da janela
janela_aberta = False

# Definir a função para copiar arquivos
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    if ignore is None:
        ignore = shutil.ignore_patterns('.DS_Store')
    names = os.listdir(src)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                if not os.path.exists(dstname) or not filecmp.cmp(srcname, dstname, shallow=False):
                    shutil.copy2(srcname, dstname)
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except shutil.Error as err: # type: ignore
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        if WindowsError is not None and isinstance(why, WindowsError):
            pass
        else:
            errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)

#Comparar diretórios e ignorar arquivos ja existentes
def sincronizar():
    pasta_origem = entry_origem.get()
    pasta_destino = entry_destino.get()

    if not os.path.exists(pasta_origem) or not os.path.exists(pasta_destino):
        print("As pastas de origem ou destino não existem.")
        return

    if filecmp.cmp(pasta_origem, pasta_destino, shallow=False):
        print("As pastas de origem e destino já estão sincronizadas.")
        return

    print("Comparando diretórios e ignorando arquivos já existentes...")
    for root, dirs, files in os.walk(pasta_origem):
        rel_path = os.path.relpath(root, pasta_origem)
        src_dir = os.path.join(pasta_origem, rel_path)
        dest_dir = os.path.join(pasta_destino, rel_path)
        for file in files:
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(dest_dir, file)
            if os.path.exists(dest_file) and filecmp.cmp(src_file, dest_file, shallow=False):
                continue
            shutil.copy2(src_file, dest_file)

    print("Sincronização concluída.")

# Sincronização dentre pastas
def sincronizar_pastas(pasta_origem, pasta_destino):
    if not os.path.exists(pasta_origem) or not os.path.exists(pasta_destino):
        print("As pastas de origem ou destino não existem.")
        return
    if filecmp.cmp(pasta_origem, pasta_destino, shallow=False):
        print("As pastas de origem e destino já estão sincronizadas.")
        return
    print("Copiando arquivos...")
    copytree(pasta_origem, pasta_destino)
    print("Removendo arquivos desnecessários...")
    for root, dirs, files in os.walk(pasta_destino):
        rel_path = os.path.relpath(root, pasta_destino)
        src_dir = os.path.join(pasta_origem, rel_path)
        for file in files:
            src_file = os.path.join(src_dir, file)
            dest_file = os.path.join(root, file)
            if not os.path.exists(src_file):
                os.remove(dest_file)
    print("Sincronização concluída.")
    
# Seleção de pasta origem
def selecionar_pasta_origem():
    global janela_aberta
    if janela_aberta:
        return
    janela_aberta = True
    pasta_origem = filedialog.askdirectory()
    entry_origem.delete(0, tk.END)
    entry_origem.insert(0, pasta_origem)
    janela_aberta = False
    
# Seleção de pastas destino    
def selecionar_pasta_destino():
    global janela_aberta
    if janela_aberta:
        return
    janela_aberta = True
    pasta_destino = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, pasta_destino)
    janela_aberta = False

def sincronizar():
    
# Janela Tkinter
    global janela_aberta
    if janela_aberta:
        return
    janela_aberta = True
    pasta_origem = entry_origem.get()
    pasta_destino = entry_destino.get()
    sincronizar_pastas(pasta_origem, pasta_destino)
    janela_aberta = False

# Criando a janela principal
janela = tk.Tk()
janela.title("Sincronização de Pastas")
janela.geometry('180x180')
janela.resizable(False, False)  # Disables resizing in both x and y directions

# Criando os widgets
frame = ttk.Frame(janela, padding=10)
frame.pack()

label_origem = ttk.Label(frame, text="Pasta de Origem:")
label_origem.pack()

entry_origem = ttk.Entry(frame)
entry_origem.pack()

button_selecionar_origem = ttk.Button(frame, text="Selecionar", command=selecionar_pasta_origem)
button_selecionar_origem.pack()

label_destino = ttk.Label(frame, text="Pasta de Destino:")
label_destino.pack()

entry_destino = ttk.Entry(frame)
entry_destino.pack()

button_selecionar_destino = ttk.Button(frame, text="Selecionar", command=selecionar_pasta_destino)
button_selecionar_destino.pack()

button_sincronizar = ttk.Button(frame, text="Sincronizar", command=sincronizar)
button_sincronizar.pack()

# Iniciando o loop da janela
janela.mainloop()