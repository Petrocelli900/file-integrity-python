# Decisões técnicas

## Uso

Crie um diretório com arquivos fictícios e execute:

    python file_integrity.py snapshot ./dados > manifest.json
    python file_integrity.py verify ./dados --manifest manifest.json

Salve o manifesto fora de dados para que ele não passe a fazer parte do próprio conjunto analisado. Snapshot escreve JSON na saída padrão. Verify retorna 0 quando igual, 1 quando há diferenças e 2 para erros.

## Integridade e custo

SHA-256 é calculado em blocos de 1 MiB, com metadados ordenados por caminho relativo. A memória do manifesto cresce com o número de arquivos, não com o conteúdo total. Diretórios vazios e permissões não fazem parte do manifesto.

Links simbólicos são rejeitados, inclusive a raiz. Metadados antes/depois detectam algumas alterações concorrentes; não garantem snapshot atômico e não defendem contra um processo adversário trocando arquivos durante a leitura. Execute sobre árvores estáveis e confiáveis.

## Limitações

Detecta diferenças de conteúdo, não comprova autenticidade: alguém que altere arquivo e manifesto pode ocultar mudanças. Sem assinatura digital, backup, restauração ou monitoramento contínuo. A validação de caminhos não abre caminhos fornecidos pelo manifesto; compara-os com uma nova varredura.
