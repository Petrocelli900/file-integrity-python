# file-integrity-python

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Verification](https://github.com/Petrocelli900/file-integrity-python/actions/workflows/verify.yml/badge.svg)

Manifestos SHA-256 para comparar arquivos adicionados, removidos e alterados, com CLI e leitura em blocos.

Projeto de portfólio com biblioteca padrão, execução local e testes automatizados. Não exige chave de API nem instalação de dependências.

## Executar

```bash
git clone https://github.com/Petrocelli900/file-integrity-python.git
cd file-integrity-python
python -m unittest discover -s tests -v
python file_integrity.py --help
```

Use python3 se esse for o comando do seu ambiente. Requer Python 3.11 ou superior.

## Estrutura

- file_integrity.py: implementação e interface de linha de comando.
- tests/test_app.py: testes de comportamento e falhas.
- docs/decisions.md: escopo, decisões e limitações.
- .github/workflows/verify.yml: verificação em Python 3.11.

## Escopo

Consulte [as decisões técnicas](docs/decisions.md) antes de adaptar para outros usos. Demonstração de portfólio com limitações explícitas.

Implementação inicial criada com assistência de IA. Exemplos utilizam dados fictícios.

[Perfil do autor](https://github.com/Petrocelli900)
