import customtkinter as ctk

class Utils:
    def center_window(self, largura_janela, altura_janela):
        largura_janela = largura_janela
        altura_janela = altura_janela

        # 1. Obtenha a largura e altura da tela
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        # 3. Calcule as coordenadas para centralizar
        x = (largura_tela / 2) - (largura_janela / 2)
        y = (altura_tela / 2) - (altura_janela / 2)

        # 4. Aplique a geometria
        self.geometry(f"{largura_janela}x{altura_janela}+{int(x)}+{int(y)}")