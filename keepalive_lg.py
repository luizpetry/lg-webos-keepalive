"""
Mantem a tela de uma TV LG webOS acesa.

Instalar:   pip install aiowebostv
Rodar:      python keepalive_lg.py

Na primeira execucao a TV mostra um pedido de pareamento: aceite com o controle.
A chave fica salva em lg_key.txt e nao pede de novo.
"""
import asyncio
from pathlib import Path

from aiowebostv import WebOsClient

TV_IP = "192.168.0.X" # Troque o "X" pelo IP da sua TV
KEY_FILE = Path(__file__).with_name("lg_key.txt")
INTERVALO = 20  # segundos entre verificacoes

# Tecla enviada para tirar a TV do protetor de tela.
# Escolha uma que nao mexa no dashboard (teste: "DASH", "ASTERISK", "RED").
TECLA = "ASTERISK"


async def acordar_tela(client):
    # 1) Comando de ligar a tela (vale para "Screen Off")
    try:
        await client.request("com.webos.service.tvpower/power/turnOnScreen")
    except Exception as e:
        print("  turnOnScreen falhou (normal no protetor de tela):", e)

    # 2) Simula uma tecla do controle (sai do "Screen Saver")
    try:
        await client.button(TECLA)
        print(f"  Tecla {TECLA} enviada.")
    except Exception as e:
        print("  Falha ao enviar tecla:", e)


def carregar_chave():
    return KEY_FILE.read_text().strip() if KEY_FILE.exists() else None


def salvar_chave(chave):
    KEY_FILE.write_text(chave)


async def main():
    while True:
        client = WebOsClient(TV_IP, client_key=carregar_chave())
        try:
            await client.connect()
            if client.client_key:
                salvar_chave(client.client_key)
            print("Conectado na TV.")

            while True:
                estado = client.tv_state.power_state or {}
                print("Estado de energia:", estado)

                # Qualquer coisa diferente de "Active" (ex.: Screen Off,
                # Screen Saver) significa que a tela esta apagada.
                if estado.get("state") not in (None, "Active"):
                    print("Tela apagada, ligando...")
                    await acordar_tela(client)

                await asyncio.sleep(INTERVALO)

        except Exception as e:
            print("Erro/conexao perdida:", e, "- tentando de novo em 15s")
            await asyncio.sleep(15)
        finally:
            await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())