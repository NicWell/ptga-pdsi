"""CLI inicial — aplicação de transformações geométricas e alinhamento."""
import argparse
from pathlib import Path
import cv2
from src.rotacao import rotacionar
from src.translacao import transladar
from src.espelhamento import espelhar
from src.redimensionamento import redimensionar
from src.alinhamento import alinhar
from src.demonstracao import gerar_demonstracao


def carregar(caminho: str):
    imagem = cv2.imread(caminho, cv2.IMREAD_COLOR)
    if imagem is None:
        raise ValueError(f"Não foi possível abrir a imagem: {caminho}")
    return imagem


def main():
    parser = argparse.ArgumentParser(description="Transformações geométricas e alinhamento de imagens")
    sub = parser.add_subparsers(dest="operacao", required=True)
    demo = sub.add_parser("demonstracao", help="Gera exemplos sintéticos e comparações visuais")
    demo.add_argument("--destino", default="resultados/demonstracao")
    for nome in ("rotacao", "translacao", "espelhamento", "redimensionamento", "alinhamento"):
        p = sub.add_parser(nome)
        p.add_argument("--saida", required=True)
        if nome == "alinhamento":
            p.add_argument("--referencia", required=True)
            p.add_argument("--movel", required=True)
        else:
            p.add_argument("--entrada", required=True)
        if nome == "rotacao": p.add_argument("--angulo", type=float, required=True)
        if nome == "translacao":
            p.add_argument("--dx", type=float, required=True)
            p.add_argument("--dy", type=float, required=True)
        if nome == "espelhamento": p.add_argument("--eixo", choices=["horizontal", "vertical", "ambos"], default="horizontal")
        if nome == "redimensionamento":
            p.add_argument("--largura", type=int, required=True)
            p.add_argument("--altura", type=int, required=True)
            p.add_argument("--interpolacao", choices=["nearest", "linear", "cubic", "area"], default="linear")
    args = parser.parse_args()
    try:
        if args.operacao == "demonstracao":
            resumo = gerar_demonstracao(args.destino)
            print(f"Demonstração salva em: {args.destino}")
            print(f"MAE sintético antes/depois: {resumo['mae_antes']:.2f} / {resumo['mae_depois']:.2f}")
            print(f"Falha esperada sem textura: {resumo['falha_sem_textura']}")
            return
        if args.operacao == "alinhamento":
            resultado = alinhar(carregar(args.referencia), carregar(args.movel))
        else:
            imagem = carregar(args.entrada)
            if args.operacao == "rotacao": resultado = rotacionar(imagem, args.angulo)
            elif args.operacao == "translacao": resultado = transladar(imagem, args.dx, args.dy)
            elif args.operacao == "espelhamento": resultado = espelhar(imagem, args.eixo)
            else: resultado = redimensionar(imagem, args.largura, args.altura, args.interpolacao)
        destino = Path(args.saida)
        destino.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(destino), resultado):
            raise OSError(f"Falha ao salvar: {destino}")
        print(f"Imagem salva em: {destino}")
    except (ValueError, OSError, cv2.error) as exc:
        parser.exit(1, f"Erro: {exc}\n")


if __name__ == "__main__":
    main()
