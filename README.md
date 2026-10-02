# TV LG sempre ligada

Script em Python que impede uma TV LG com **webOS** de apagar a tela sozinha.

## Para que serve

Algumas TVs LG apagam a tela ou entram no protetor de tela depois de poucos minutos sem uso, mesmo com as opções de economia de energia e desligamento automático desativadas. Isso atrapalha quando a TV fica exibindo um painel, dashboard ou monitor de forma contínua.

O script se conecta à TV pela rede local e, a cada **20 segundos**, consulta o estado de energia. Se a tela estiver apagada (`Screen Off`) ou em protetor de tela (`Screen Saver`), ele:

1. envia o comando para ligar a tela (`turnOnScreen`);
2. simula o aperto de uma tecla do controle remoto, o que tira a TV do protetor de tela.

Se a conexão cair, ele tenta reconectar sozinho a cada 15 segundos.

## Requisitos

- TV LG com webOS na mesma rede do computador
- Python 3 (uma versão recente, compatível com a biblioteca `aiowebostv`)
- Na TV, a opção **LG Connect Apps** ou **Ligar via Wi-Fi/Mobile** ativada (o nome muda conforme o modelo)

## Instalação

```bash
git clone https://github.com/luizpetry/lg-webos-keepalive.git
cd lg-webos-keepalive
pip install aiowebostv
```

## Configuração

Abra `keepalive_lg.py` e ajuste as constantes do topo:

| Constante   | O que é                                                                  | Exemplo         |
|-------------|--------------------------------------------------------------------------|-----------------|
| `TV_IP`     | IP da TV na rede local, definido pelo seu roteador (veja em Configurações > Rede na própria TV) | `192.168.0.x` |
| `INTERVALO` | Segundos entre cada verificação. Deixe abaixo do tempo que a TV leva para apagar | `140`   |
| `TECLA`     | Tecla enviada para acordar a tela. Escolha uma que não mexa no que está na tela (`DASH`, `ASTERISK`, `RED`...) | `DASH` |

> Dica: reserve o IP da TV no roteador (DHCP fixo) para ele não mudar.

## Uso

```bash
python keepalive_lg.py
```

Na **primeira execução** a TV mostra um pedido de pareamento. Aceite com o controle remoto. A chave de acesso fica salva em `lg_key.txt` e o pedido não aparece de novo.

### Rodar ao iniciar o Windows (opcional)

Para não depender de um terminal aberto, crie uma tarefa no **Agendador de Tarefas**:

- **Disparador:** ao fazer logon
- **Ação:** iniciar o programa `pythonw.exe` com o argumento `keepalive_lg.py`
- **Iniciar em:** a pasta do projeto

O `pythonw.exe` roda o script sem abrir janela.

## Segurança

O arquivo `lg_key.txt` dá acesso de controle à sua TV. Não compartilhe-o.
